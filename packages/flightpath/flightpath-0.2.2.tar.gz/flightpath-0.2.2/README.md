[![PyPI version](https://badge.fury.io/py/flightpath.svg)](https://badge.fury.io/py/flightpath)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)

# Flightpath

A command-line tool for analyzing critical paths in Apache Airflow DAGs.

## Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Details](#details)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Overview

Flightpath identifies bottlenecks in your Airflow DAGs using critical path
analysis. Simply point Flightpath at any DAG run, and it will trace backward
through your dependencies to identify performance bottlenecks. With this
insight, you can focus your optimization efforts where they matter most and
significantly reduce your overall execution times.


## Quick Start
If you have `uv` installed, you can already use `flightpath` without any installation steps:
```bash
# View help
uvx flightpath --help

# Trace a critical path in your DAG
uvx flightpath trace \
  -u admin -p admin \
  --baseurl http://localhost:8080 \
  --end-task-id end \
  --end-dag-id your_dag_id \
  --dag-run-id your_dag_run_id
```


## Details
Central to flighpath is the concept of a **Critical Path**. To formally define 
the **Critical Path** of a dag run, we'll first introduce some prerequisite terms 
related to tasks and dag runs.
- **Task Running Time**: The duration a task instance takes to execute. If a task 
instance runs for multiple tries, we take the start time of the first try and 
the end time of the last try.
- **Task Ready Time**: The duration between a task instance's upstream dependencies 
completing and a task instance starting. This includes the task instance's None 
state _after_
 all dependencies are satisfied, as well as the Queued state and 
Scheduled state. The ready time captures the period when upstreams are satisfied 
but the task instance is not running, typically due to scheduler delays or pool 
constraints.
- **Task Total Time**: **Ready Time** + **Running Time**
- **Dependency Path**: Any sequence of task dependencies which joins a sequence 
of task instances. The duration of a **Dependency Path** is the sum of **Total Time** 
for all task instances on the path.

With these definitions in place, we can define the **Critical Path** as 
**_the slowest dependency path in a dag run_**. It is impossible for a dag run 
to complete in less time than it's slowest dependency path. Therefore, the dag 
run's duration equals the critical path duration.

To find the critical path, the `flightpath` tracing algorithm traverses a DAG
backwards, following upstream dependencies. The algorithm starts with a
user-provided "end" task, finds the upstream dependency that completed last (the
"blocking upstream") and then repeats the process from blocking upstream. By
default, `flightpath`'s tracing algorithm will only trace a critical path within
the dag it started in. Adding the `--external` flag instructs `flightpath` to
trace through any `ExternalTaskSensor`s that it encounters, allowing it to trace
through many other DAGs.

Importantly, the critical path may change between dag runs. This is because 
task instance durations are non-deterministic, and so the slowest dependency 
path in the dag is also non-deterministic. For this reason, it is helpful to 
compare critical path trends across many dag runs. Tasks that frequently appear on 
the critical path across multiple dag runs are prime targets for optimization.


## Installation

We always recommend using [uv](https://docs.astral.sh/uv/getting-started/installation/) 
to directly run `flightpath` without any installation steps, as shown above in Quick Start.


If you prefer, you can also install flightpath using either `uv` or `pip`
```
# install with uv
uv tool install flightpath

# install with pip
pip install flightpath

# check installation
flightpath --help
```


## Usage

Basic usage of `flightpath` is illustrated below. Using `flightpath trace` we can 
trace the critical path of the `diamond2` DAG (see DAG definition at  
`tests/airflow_example/dags/diamond2.py`):

```bash
# Using command line arguments
uvx flightpath trace \
  -u admin -p admin \
  --baseurl http://localhost:8080 \
  --end-task-id end \
  --end-dag-id diamond2 \
  --dag-run-id scheduled__2025-03-10T20:50:00+00:00
```

This command produces the following output.
```
2025-03-10 16:16:04,553 - INFO - Tracing from diamond2:end
2025-03-10 16:16:04,553 - INFO -   Extracting all dependencies for dag diamond2 from endpoint: http://localhost:8080/api/v1/dags/diamond2/tasks
2025-03-10 16:16:07,945 - INFO - Found previous task diamond2:task_2
2025-03-10 16:16:10,134 - INFO - Found previous task diamond2:slow_path_17
2025-03-10 16:16:10,233 - INFO - Found previous task diamond2:task_1
2025-03-10 16:16:10,330 - INFO - Found previous task diamond2:wait_for_diamond1
2025-03-10 16:16:10,330 - INFO -   Retrieving upstream information for ExternalTaskSensor task wait_for_diamond1 in dag diamond2
2025-03-10 16:16:10,523 - INFO - Halting trace because --external was not specified andthe previous task diamond1:end is not in the same DAG as the end task diamond2:end.
DAG ID   | Path Index | Task ID           | Pool         | Priority Weight | Ready Date          | Start Date          | End Date            | Ready (Seconds) | Running (Seconds) | Total (Seconds) | Link
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
diamond2 | 0          | wait_for_diamond1 | default_pool | 25              | -                   | 2025-03-10 21:05:15 | 2025-03-10 21:13:32 | 0.0             | 0.0               | 0.0             | LINK
diamond2 | 1          | task_1            | default_pool | 24              | 2025-03-10 21:13:32 | 2025-03-10 21:13:32 | 2025-03-10 21:13:32 | 0.0             | 0.0               | 0.0             | LINK
diamond2 | 2          | slow_path_17      | default_pool | 3               | 2025-03-10 21:13:32 | 2025-03-10 21:13:55 | 2025-03-10 21:14:06 | 23.0            | 10.3              | 33.4            | LINK
diamond2 | 3          | task_2            | default_pool | 2               | 2025-03-10 21:14:06 | 2025-03-10 21:14:06 | 2025-03-10 21:14:06 | 0.7             | 0.0               | 0.7             | LINK
diamond2 | 4          | end               | default_pool | 1               | 2025-03-10 21:14:06 | 2025-03-10 21:14:07 | 2025-03-10 21:14:07 | 0.1             | 0.0               | 0.1             | LINK

-- Statistics --
Ready Time:     23.9 Seconds
Running Time:   10.3 Seconds
Total Time:     34.2 Seconds
Longest Task:   diamond2:slow_path_17 (33.4 Seconds, 97.5% of total time)

-- Parameters --
Run Id:         scheduled__2025-03-10T20:50:00+00:00
End Dag:        diamond2
End Task:       end
```

Each row in the output table represents a task instance that appeared on the
critial path. In the above example, the total length of the critical path was
five. The path began at `wait_for_dimond1` and ended at `end`. The `end` task
was provided as an input by the user, and `flightpath` traced backwards from
this task by following blocking upstreams. The main bottleneck on this critical
path was the `slow_path_17` task, which accounted for 33.4 seconds of the dag
run's total 34.2 seconds (97.5% of total time). If we had included `--external`,
flightpath would have continued tracing through the `wait_for_diamond1`
`ExternalTaskSensor` and into the upstream DAG `diamond1`.

## Configuration

You can store default authentication settings in a configuration file at `~/.config/flightpath/config.json`. This eliminates the need to provide these values via command line arguments each time you run flightpath.

Example configuration file:
```json
{
    "username": "admin",
    "password": "admin",
    "baseurl": "http://localhost:8080"
}
```

Command line arguments take precedence over values in the configuration file. If any required authentication parameters are missing from both the command line and configuration file, flightpath will display an error message.
