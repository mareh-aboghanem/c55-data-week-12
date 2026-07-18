"""Week 12 assignment starter.

Turn this into a scheduled, parameterized, retryable pipeline. The task
list, the file-by-file map, and the point breakdown are in README.md; the
full brief is in the Week 12 "Assignment: Orchestrated Pipeline" chapter.

This starter parses, so `astro dev start` shows the DAG in the UI, but every
task body raises NotImplementedError and the decorator is not configured yet.
Replace the stubs, wire the tasks together, and fill in the decorator. The
autograder fails while any NotImplementedError remains.
"""

import os
from datetime import datetime
from pathlib import Path

from airflow.sdk import dag, task

# Your per-student schema. AIRFLOW_STUDENT is set in .env for local Astro dev;
# on the shared VM it falls back to the dags/<name>/ directory name.
STUDENT = os.environ.get("AIRFLOW_STUDENT") or Path(__file__).parent.name
SCHEMA = f"airflow_{STUDENT}"
TLC_BASE = "https://d37ci6vzurychx.cloudfront.net/trip-data"


def find_dbt_dir() -> str:
    """Return the mounted dbt project path (Astro vs shared-VM install root)."""
    for candidate in (
        "/usr/local/airflow/include/dbt_project",  # Astro CLI
        "/opt/airflow/include/dbt_project",        # shared VM docker-compose
    ):
        if Path(candidate).is_dir():
            return candidate
    return "/usr/local/airflow/include/dbt_project"


DBT_DIR = find_dbt_dir()


@dag(
    # TODO Task 1 (see README): configure the decorator.
    start_date=datetime(2024, 1, 1),
)
def taxi_pipeline():
    @task
    def ingest_taxi_month() -> int:
        """Download one month of TLC green-taxi data and load it into
        ``{SCHEMA}.raw_trips`` idempotently. Return the number of rows.

        TODO Task 2 and Task 3 (see README).
        """
        raise NotImplementedError

    # TODO Task 2 (see README): add the two transform tasks, wire the full
    # chain, and run the transform through the Chapter 4 command so it works
    # on the image's Python. TODO Task 4: add retry behaviour.

    ingest_taxi_month()


taxi_pipeline()
