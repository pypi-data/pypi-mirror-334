import abc
from collections import defaultdict
import dataclasses
import datetime
import functools
import logging
import requests
import time
import urllib.parse
from typing import Collection, Literal, Mapping
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

import flightpath.config

logger = logging.getLogger("flightpath")


@dataclasses.dataclass(frozen=True)
class Task:
    dag_id: str
    task_id: str


class TaskInstance(abc.ABC):
    def __init__(
        self,
        dag_id: str,
        task_id: str,
        dag_run_id: str,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ):
        self.dag_id = dag_id
        self.task_id = task_id
        self.dag_run_id = dag_run_id
        self.start_date = start_date
        self.end_date = end_date

        self.prev = None
        self.next = None
        self._path_index = None

    @property
    def ready_seconds(self) -> float:
        if not self.prev:
            return 0.0
        else:
            return (self.start_date - self.prev.end_date).total_seconds()

    @property
    def running_seconds(self) -> float:
        return (self.end_date - self.start_date).total_seconds()

    @property
    def total_seconds(self) -> float:
        return self.running_seconds + self.ready_seconds

    def __str__(self):
        return f"TaskInstance({self.dag_id}.{self.task_id})"

    @property
    def path_index(self):
        if not self._path_index:
            if not self.prev:
                self._path_index = 0
            else:
                self._path_index = self.prev.path_index + 1

        return self._path_index

    def task(self) -> Task:
        return Task(self.dag_id, self.task_id)

    @abc.abstractmethod
    def get_upstream_task_instances(self) -> Collection["TaskInstance"]:
        pass

    @abc.abstractmethod
    def get_url(self) -> str:
        pass


class AirflowTaskInstance(TaskInstance):
    def __init__(
        self,
        airflow_client: "AirflowClient",
        pool: str,
        priority_weight: int,
        execution_date: str,
        *args,
        **kwargs,
    ):
        self.airflow_client = airflow_client
        self.pool = pool
        self.priority_weight = priority_weight
        self.execution_date = execution_date
        super().__init__(*args, **kwargs)

    def get_url(self) -> str:
        return f"{self.airflow_client.base_url}/task?dag_id={self.dag_id}&task_id={self.task_id}&execution_date={urllib.parse.quote(self.execution_date)}"

    def get_upstream_task_instances(self) -> Collection["TaskInstance"]:
        dependencies = self.airflow_client.get_all_task_dependencies_for_dag(
            dag_id=self.dag_id, dag_run_id=self.dag_run_id
        )

        if self.task() in dependencies:
            upstream_tasks = dependencies[Task(self.dag_id, self.task_id)]

            upstream_task_instances = [
                self.airflow_client.get_task_instance(
                    dag_id=t.dag_id, task_id=t.task_id, dag_run_id=self.dag_run_id
                )
                for t in upstream_tasks
            ]

            return upstream_task_instances
        else:
            return []

    def __eq__(self, other):
        return (
            self.dag_id == other.dag_id
            and self.task_id == other.task_id
            and self.dag_run_id == other.dag_run_id
        )


class AirflowExternalTaskSensor(AirflowTaskInstance):
    @property
    def ready_seconds(self) -> float:
        return 0.0

    @property
    def running_seconds(self) -> float:
        if not self.prev:
            return 0.0
        else:
            return (self.end_date - self.prev.end_date).total_seconds()

    def get_upstream_task_instances(self) -> Collection["TaskInstance"]:
        logger.info(
            f"  Retrieving upstream information for ExternalTaskSensor task {self.task_id} in dag {self.dag_id}"
        )
        task_instance_endpoint = f"{self.airflow_client.base_url}/api/v1/dags/{self.dag_id}/dagRuns/{self.dag_run_id}/taskInstances/{self.task_id}"

        logger.debug(
            f"Extracting upstream information for ExternalTaskSensor task {self.task_id} from endpoint: {task_instance_endpoint}"
        )
        response = self.airflow_client.session.get(
            task_instance_endpoint, auth=self.airflow_client.auth
        )
        task_info = response.json()

        if (
            "rendered_fields" in task_info
            and "external_dag_id" in task_info["rendered_fields"]
            and "external_task_id" in task_info["rendered_fields"]
        ):
            external_dag_id = task_info["rendered_fields"]["external_dag_id"]
            external_task_id = task_info["rendered_fields"]["external_task_id"]

            return [
                self.airflow_client.get_task_instance(
                    dag_id=external_dag_id,
                    task_id=external_task_id,
                    dag_run_id=self.dag_run_id,
                )
            ]
        else:
            logger.warning(
                f"Could not find upstream information for ExternalTaskSensor task {self.task_id} from endpoint: {task_instance_endpoint} for dag_run_id {self.dag_run_id}"
            )

            return []


class Client(abc.ABC):
    @abc.abstractmethod
    def get_task_instance(
        self, dag_id: str, task_id: str, dag_run_id: str
    ) -> TaskInstance:
        pass


class AirflowClient(Client):
    def __init__(self, user: str, password: str, base_url: str, verbose: bool = False):
        self.user = user
        self.password = password
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self.verbose = verbose

        self._auth = None
        self._session = None

    @property
    def session(self) -> requests.Session:
        if not self._session:
            retry_strategy = Retry(
                total=3,  # number of retries
                backoff_factor=1,  # wait 1, 2, 4 seconds between retries
                status_forcelist=[
                    429,
                    500,
                    502,
                    503,
                    504,
                ],  # HTTP status codes to retry on
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)

            self._session = requests.Session()
            self._session.auth = self.auth
            self._session.mount("http://", adapter)
            self._session.mount("https://", adapter)

        return self._session

    @property
    def auth(self) -> requests.auth.HTTPBasicAuth:
        if not self._auth:
            self._auth = requests.auth.HTTPBasicAuth(self.user, self.password)
        return self._auth

    def get_task_instance(
        self, dag_id: str, task_id: str, dag_run_id: str
    ) -> TaskInstance:
        endpoint = f"{self.base_url}/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}"
        logger.debug(
            f"Fetching task {task_id} in dag {dag_id} for run id {dag_run_id} from: {endpoint}"
        )
        response = self.session.get(endpoint)

        if response.status_code == 404:
            raise ValueError(
                f"Task instance not found: dag_id={dag_id}, task_id={task_id}, dag_run_id={dag_run_id}. HINT: The specified dag_run_id may not exist for this dag_id/task_id combination. This was the url that I checked: {endpoint}"
            )
        else:
            response.raise_for_status()

        data = response.json()

        if data["operator"] == "ExternalTaskSensor":
            return AirflowExternalTaskSensor(
                airflow_client=self,
                dag_id=dag_id,
                task_id=task_id,
                dag_run_id=dag_run_id,
                start_date=datetime.datetime.fromisoformat(data["start_date"]),
                end_date=datetime.datetime.fromisoformat(data["end_date"]),
                pool=data["pool"],
                priority_weight=data["priority_weight"],
                execution_date=data["execution_date"],
            )

        else:
            return AirflowTaskInstance(
                airflow_client=self,
                dag_id=data["dag_id"],
                task_id=data["task_id"],
                dag_run_id=data["dag_run_id"],
                start_date=datetime.datetime.fromisoformat(data["start_date"]),
                end_date=datetime.datetime.fromisoformat(data["end_date"]),
                pool=data["pool"],
                priority_weight=data["priority_weight"],
                execution_date=data["execution_date"],
            )

    @functools.lru_cache(maxsize=1000)
    def get_all_task_dependencies_for_dag(
        self, dag_id: str, dag_run_id: str
    ) -> Mapping[Task, Collection[Task]]:
        endpoint = f"{self.base_url}/api/v1/dags/{dag_id}/tasks"
        logger.info(
            f"  Extracting all dependencies for dag {dag_id} from endpoint: {endpoint}"
        )

        # Make request for all tasks
        response = self.session.get(endpoint)

        logger.debug(f"Response status code: {response.status_code}")
        response.raise_for_status()

        tasks = response.json()["tasks"]
        logger.debug(f"Found {len(tasks)} tasks for dependency analysis")

        dependencies = defaultdict(lambda: set())

        for task in tasks:
            for downstream_task_id in task["downstream_task_ids"]:
                dependencies[Task(dag_id, downstream_task_id)].add(
                    Task(dag_id, task["task_id"])
                )

        logger.debug("Sleeping to throttle requests...")
        time.sleep(flightpath.config.THROTTLE_DURATION_SECONDS)

        return dict(dependencies)


class CriticalPathTracer:
    def __init__(self, client: Client, verbose: bool = False):
        self.client = client
        self.verbose = verbose

    def trace(
        self, end_dag_id: str, end_task_id: str, dag_run_id: str, external: bool = False
    ) -> TaskInstance:
        logger.debug(
            f"Tracing critical path starting from dag {end_dag_id} task {end_task_id} for run id {dag_run_id}"
        )
        current_ti = self.client.get_task_instance(end_dag_id, end_task_id, dag_run_id)
        logger.info(f"Tracing from {end_dag_id}:{end_task_id}")

        path = [current_ti]

        while True:
            try:
                previous_ti = self.find_previous(current_ti)
            except Exception as e:
                logger.error(
                    f"Halting trace due to error finding previous task for current_ti {str(current_ti)}: {e}"
                )
                break

            if not previous_ti:
                logger.info("No previous task found. Ending trace.")
                break

            if not external and previous_ti.dag_id != end_dag_id:
                logger.info(
                    f"Halting trace because --external was not specified andthe previous task {previous_ti.dag_id}:{previous_ti.task_id} is not in the same DAG as the end task {end_dag_id}:{end_task_id}."
                )
                break

            if any(previous_ti == t for t in path):
                logger.info(
                    f"Halting trace because I found a cycle in the path at task {previous_ti.dag_id}:{previous_ti.task_id}. This can happen when using ExternalTaskSensor with an execution_delta to wait on a previous DAG run."
                )
                break

            logger.info(
                f"Found previous task {previous_ti.dag_id}:{previous_ti.task_id}"
            )
            path.append(previous_ti)

            current_ti.prev = previous_ti
            previous_ti.next = current_ti

            current_ti = previous_ti

        return current_ti

    def find_previous(self, ti: TaskInstance) -> TaskInstance:
        upstream_task_instances = ti.get_upstream_task_instances()

        if not upstream_task_instances:
            return None

        return max(upstream_task_instances, key=lambda t: t.end_date)

    @staticmethod
    def print_critical_path(
        root_ti: TaskInstance,
        print_url: bool,
        output_format: Literal["table", "json"] = "table",
    ):
        results = []

        current_ti = root_ti
        while current_ti:
            results.append(current_ti)
            current_ti = current_ti.next

        # Prepare data for printing
        headers = [
            "DAG ID",
            "Path Index",
            "Task ID",
            "Pool",
            "Priority Weight",
            "Ready Date",
            "Start Date",
            "End Date",
            "Ready (Seconds)",
            "Running (Seconds)",
            "Total (Seconds)",
            "Link",
        ]

        # Convert task instances to rows of data
        data = []
        for ti in results:
            data.append(
                [
                    ti.dag_id,
                    str(ti.path_index),
                    ti.task_id,
                    ti.pool,
                    ti.priority_weight,
                    ti.prev.end_date.strftime("%Y-%m-%d %H:%M:%S") if ti.prev else "-",
                    ti.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                    ti.end_date.strftime("%Y-%m-%d %H:%M:%S"),
                    f"{ti.ready_seconds:.1f}",
                    f"{ti.running_seconds:.1f}",
                    f"{ti.total_seconds:.1f}",
                    ti.get_url()
                    if print_url
                    else f"\033]8;;{ti.get_url()}\033\\LINK\033]8;;\033\\",
                ]
            )

        # Calculate summary statistics
        total_ready = sum(ti.ready_seconds or 0 for ti in results)
        total_running = sum(ti.running_seconds or 0 for ti in results)
        total_time = total_ready + total_running

        longest_task = max(results, key=lambda ti: ti.total_seconds or 0)
        longest_time = longest_task.total_seconds
        longest_percent = (longest_time / total_time * 100) if total_time > 0 else 0

        # Handle different output formats
        if output_format == "json":
            import json

            # Prepare critical path data for JSON
            critical_path = []
            for i, row in enumerate(data):
                critical_path.append(
                    {
                        "dag_id": row[0],
                        "path_index": int(row[1]),
                        "task_id": row[2],
                        "pool": row[3],
                        "priority_weight": row[4],
                        "ready_date": row[5] if row[5] != "-" else None,
                        "start_date": row[6],
                        "end_date": row[7],
                        "ready_seconds": float(row[8]),
                        "running_seconds": float(row[9]),
                        "total_seconds": float(row[10]),
                        "url": row[11] if print_url else results[i].get_url(),
                    }
                )

            # Prepare statistics for JSON
            statistics = {
                "ready_time_seconds": round(total_ready, 1),
                "running_time_seconds": round(total_running, 1),
                "total_time_seconds": round(total_time, 1),
                "longest_task": {
                    "dag_id": longest_task.dag_id,
                    "task_id": longest_task.task_id,
                    "total_seconds": round(longest_time, 1),
                    "percent_of_total": round(longest_percent, 1),
                },
                "parameters": {
                    "run_id": results[-1].dag_run_id,
                    "end_dag": results[-1].dag_id,
                    "end_task": results[-1].task_id,
                },
            }

            # Output JSON
            output = {"critical_path": critical_path, "statistics": statistics}
            print(json.dumps(output, indent=2))
        else:
            # Calculate column widths based on data and headers
            all_rows = [headers] + data
            col_widths = [
                max(len(str(row[i])) for row in all_rows) for i in range(len(headers))
            ]

            if not print_url:
                col_widths[-1] = 6

            # Create format string for consistent column widths
            format_string = " | ".join("{:<" + str(width) + "}" for width in col_widths)

            # Print table
            print(format_string.format(*headers))
            print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
            for row in data:
                print(format_string.format(*row))

            print("\n-- Statistics --")
            print(f"Ready Time:\t{total_ready:.1f} Seconds")
            print(f"Running Time:\t{total_running:.1f} Seconds")
            print(f"Total Time:\t{total_time:.1f} Seconds")
            print(
                f"Longest Task:\t{longest_task.dag_id}:{longest_task.task_id} ({longest_time:.1f} Seconds, {longest_percent:.1f}% of total time)"
            )

            print("\n-- Parameters --")
            print(f"Run Id:\t\t{results[-1].dag_run_id}")
            print(f"End Dag:\t{results[-1].dag_id}")
            print(f"End Task:\t{results[-1].task_id}")
