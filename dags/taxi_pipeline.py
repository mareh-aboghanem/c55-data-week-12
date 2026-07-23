import io
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag, task , get_current_context

# Your per-student schema. AIRFLOW_STUDENT is set in .env for local Astro dev;
# on the shared VM it falls back to the dags/<name>/ directory name.
STUDENT = os.environ.get("AIRFLOW_STUDENT") or Path(__file__).parent.name
SCHEMA = f"airflow_{STUDENT}"
TLC_BASE = "https://d37ci6vzurychx.cloudfront.net/trip-data"

dbt = "uvx --python 3.11 --from 'dbt-core==1.10.*' --with 'dbt-postgres==1.10.*' dbt"
DBT_ENV = {
    "PG_HOST": "{{ conn.azure_pg.host }}", 
    "PG_USER": "{{ conn.azure_pg.login }}",}


def parquet_url_for(ds: str) -> str:
    """Return the TLC green-taxi parquet URL for a logical date."""
    year_month = ds[:7]  # "2024-01-01" -> "2024-01"
    return f"{TLC_BASE}/green_tripdata_{year_month}.parquet"


def _ds_from_context() -> str:
    """Return the logical-date string for the current task run."""
    ctx = get_current_context()
    dr = ctx["dag_run"]
    dt = dr.logical_date or dr.run_after
    return dt.strftime("%Y-%m-%d")


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
    dag_id=f"taxi_pipeline_{STUDENT}",
    schedule="@monthly",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": 60,  # seconds
    },
    tags=["week12", "taxi_pipeline", f"student:{STUDENT}"],
)
def taxi_pipeline():
    @task
    def ingest_taxi_month() -> int:
        ds = _ds_from_context()
        year_month= ds[:7]
        resp=requests.get(parquet_url_for(ds),timeout=60)
        resp.raise_for_status()
        df=pd.read_parquet(io.BytesIO(resp.content))
        hook = PostgresHook(postgres_conn_id="azure_pg")
        engine = hook.get_sqlalchemy_engine()
        with hook.get_conn() as conn, conn.cursor() as cur:
            cur.execute(f'CREATE SCHEMA IF NOT EXISTS "{SCHEMA}"')

        df.head(0).to_sql(
            "raw_trips", engine, schema=SCHEMA, if_exists="append", index=False
        )
        with hook.get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                f'DELETE FROM "{SCHEMA}".raw_trips '
                "WHERE to_char(lpep_pickup_datetime, 'YYYY-MM') = %s",
                (year_month,),
            )
        df.to_sql(
            "raw_trips",
            engine,
            schema=SCHEMA,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000,
        )
        return len(df)

    dbt_run = BashOperator(
        task_id = "dbt_run",
        bash_command=(
        f"{dbt} deps --project-dir {DBT_DIR} --profiles-dir {DBT_DIR} && "
        f"{dbt} run --project-dir {DBT_DIR} --profiles-dir {DBT_DIR}"
    ),
    env=DBT_ENV,
    append_env=True,)
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"{dbt} test --project-dir {DBT_DIR} --profiles-dir {DBT_DIR}",
        env=DBT_ENV,
        append_env=True,)
    ingest_taxi_month() >> dbt_run >> dbt_test

taxi_pipeline()
