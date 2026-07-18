## What I built
- Airflow DAG: `dags/taxi_pipeline.py` (schedule, `ingest_taxi_month → dbt_run → dbt_test`, partition from logical date, retries)
- Week 10 dbt project dropped into `include/dbt_project/`
- Backfill + idempotency evidence (Task 5)
- Operational notes: `RUNBOOK.md`
- Assignment report: `ASSIGNMENT_REPORT.md`
- (Target tier) namespaced DAG deployed to the shared class Airflow
- AI usage: `AI_ASSIST.md`

## How to review
- DAG: read `dags/taxi_pipeline.py` (schedule, task order, `catchup=False`, retries, partition date).
- Evidence: backfill / idempotency notes in `ASSIGNMENT_REPORT.md`; operations in `RUNBOOK.md`.
- AI usage: `AI_ASSIST.md`.

## How to run
From a clean clone, with the Astro CLI installed:

```bash
astro dev start
astro dev pytest tests/test_dag_integrity.py --args "-v"
```

Then open the UI URL, add the `azure_pg` connection (Admin → Connections), unpause `taxi_pipeline`, and trigger a run for a real month (e.g. `2024-01-01`).

Prerequisite: your Week 10 dbt project in `include/dbt_project/` and the `azure_pg` connection to the shared Postgres.

## What reviewers should see (expected results)
Fill in what your run actually produces:
- `test_dag_integrity.py` result: <e.g. all pass>
- Task order in the Graph view: <e.g. ingest → dbt_run → dbt_test>
- Backfill: <e.g. 7 runs green, re-run is idempotent (same row count)>
- Deployed DAG name (Target tier): <e.g. taxi_pipeline_<name>>

## Known limitations / out of scope
- <e.g. Target-tier deploy not attempted; retries set to 2>
- Write "none" if everything in the assignment is done and working.

## Self-check
- [ ] `bash .hyf/test.sh` passes
- [ ] `astro dev pytest tests/test_dag_integrity.py` passes
- [ ] `catchup=False` and retries are set
- [ ] No credentials committed (connections added in the UI, not in code)
- [ ] Backfill / idempotency evidence is in `ASSIGNMENT_REPORT.md`
