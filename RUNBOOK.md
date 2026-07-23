# RUNBOOK

<!-- Replace every TODO with real content. Another student should be able to
     operate your DAG from this file alone, without reading your Python. -->

## How to trigger the DAG manually
Open Airflow in your web browser (http://localhost:8080).

Find taxi_pipeline in the list and make sure the toggle switch is turned ON.

Click on taxi_pipeline.

Click the Trigger button at the top right corner.

Click Trigger DAG to start running it immediately.
## How to run a backfill

To process data for past months (for example, all months in 2024), open your terminal and run this command:

astro dev run backfill create --dag-id taxi_pipeline --from-date 2024-01-01 --to-date 2024-07-31 --max-active-runs 1

Note: --max-active-runs 1 forces Airflow to run one month at a time so it doesn't overload your computer or database.

## How to inspect task logs

Go to the taxi_pipeline page in Airflow.

Click on the Grid tab.

Click on the square box for the task you want to check (like ingest_taxi_month or dbt_run).

On the right side panel that pops up, click Logs.

Scroll down to the bottom of the text to see what went wrong.

## Top 3 likely failures and first response

1. Database Password / Connection Error

Problem: Task turns red with a password authentication failed error message.

What to check: Check your .env file to see if your password or username is wrong.

How to fix: Fix your credentials in .env, run astro dev stop then astro dev start, and click Clear on the red task in Airflow to try again.

2. Data Download Error

Problem: ingest_taxi_month fails because it cannot fetch the dataset online.

What to check: Check if your internet is working or if the file for that specific month actually exists.

How to fix: Make sure you are connected to the internet, then click Clear on the task to rerun it.

3. dbt Transformation Error

Problem: dbt_run or dbt_test fails after the data was already downloaded.

What to check: Open the task logs for dbt_run and look for SQL error messages at the bottom.

How to fix: Fix the SQL code or test rules in your dbt project, save your files, and click Clear on the task in Airflow to test it again.


