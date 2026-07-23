# Assignment Report

## Schedule Choice and Reason

I chose a monthly schedule (`0 0 1 * *`) for the `taxi_pipeline` DAG. The dataset updates once a month, so running the pipeline on the first of every month keeps the data up to date without wasting resources.

## Task Dependency Graph

The pipeline runs in a strict 3-step order:
`ingest_taxi_month` $\rightarrow$ `dbt_run` $\rightarrow$ `dbt_test`.

* **`ingest_taxi_month`** downloads the raw data into PostgreSQL first.
* **`dbt_run`** transforms that raw data into clean dbt models.
* **`dbt_test`** checks the cleaned data for quality errors.

Order matters because dbt cannot transform or test data before it is ingested into the database.

## dbt Project Used

I used the class reference dbt project, set up to build models inside my personal database schema.

## Debugging Case Resolved

* **Problem:** The ingestion and dbt tasks failed with a database password authentication error.
* **Diagnosis:** I checked the Airflow task logs and found that PostgreSQL rejected the connection due to incorrect credentials in the environment variables.
* **Fix:** I updated `.env` with the correct database credentials and schema, restarted Astro, and cleared the failed tasks in the Airflow UI to rerun them successfully.

## Backfill Notes

* **Dynamic Dates:** The DAG uses the `{{ ds }}` parameter to automatically pick the correct date range for each run.
* **Backfill Command:** I ran the backfill for 2024 using:
```bash
astro dev run backfill create --dag-id taxi_pipeline --from-date 2024-01-01 --to-date 2024-07-31 --max-active-runs 1

```
* **Performance Note:** The backfill takes a long time to complete because `--max-active-runs 1` forces Airflow to process each month sequentially (one at a time) to avoid overloading the server.