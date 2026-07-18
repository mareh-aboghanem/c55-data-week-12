# Data Track — Week 12 assignment: Orchestrated Pipeline

Turn the pipeline you built in earlier weeks into one that runs itself:
scheduled, in the right order, with retries, backfills, and failure
visibility. You build a production-style Airflow DAG on the Astro CLI and
(at Target tier) deploy it to the shared class Airflow.

> The full assignment brief, tiers, and deliverables live in the curriculum:
> **Week 12 → Assignment: Orchestrated Pipeline**. This repo is the starter
> you build in. Read the chapter for the why; use this README for the how.

## Why there are no `task-N/` folders

This is a real Astro project layout, not a folder-per-task worksheet. You
work in `dags/taxi_pipeline.py` and fill in the supporting docs. That mirrors
how you would actually ship an orchestration change on the job.

## Where to start

| Step | File | Chapter task | What to do |
|------|------|--------------|-----------|
| 1 | `dags/taxi_pipeline.py` (`@dag`) | Task 1 | schedule, `start_date`, `catchup=False`, a tag |
| 2 | `dags/taxi_pipeline.py` (tasks) | Task 2 | `ingest_taxi_month → dbt_run → dbt_test`, dbt via `uvx` |
| 3 | `dags/taxi_pipeline.py` (`_partition_date`) | Task 3 | drive the partition from the logical date |
| 4 | `dags/taxi_pipeline.py` (`default_args`) | Task 4 | `retries` + `retry_delay` |
| 5 | (run it) | Task 5 | 7-run backfill + idempotency evidence |
| 6 | `RUNBOOK.md` | Task 6 | operational notes |
| 7 | shared repo | Task 7 (Target) | deploy your namespaced DAG |
| 8 | `AI_ASSIST.md` | Task 8 | document one LLM use |

## Repository layout

```text
.
├── dags/
│   └── taxi_pipeline.py     # STARTER — the DAG you implement
├── include/
│   └── dbt_project/         # drop your Week 10 dbt project here (see its README)
├── tests/
│   └── test_dag_integrity.py  # provided; keep it passing (all tiers)
├── Dockerfile               # Astro Runtime 3.3
├── requirements.txt         # Airflow providers — do NOT add dbt (uvx handles it)
├── RUNBOOK.md               # fill in
├── ASSIGNMENT_REPORT.md     # fill in
├── AI_ASSIST.md             # fill in
└── .hyf/                    # autograder (do not edit)
```

## Run it locally

```bash
astro dev start                         # boots Airflow; prints a UI URL
astro dev pytest tests/test_dag_integrity.py --args "-v"
```

Open the UI URL, add the `azure_pg` connection (Admin → Connections), unpause
`taxi_pipeline`, and trigger a run for a real month (e.g. `2024-01-01`).

## Check your score locally

```bash
bash .hyf/test.sh
cat .hyf/score.json
```

The grader is **static**: it checks your DAG code and docs, not a live run.
The green run, backfill idempotency, and shared-Airflow deploy are Target-tier
items a teacher reviews by hand, so a high static score is necessary but not
sufficient for Target.

## Scoring ladder (100 pts, pass = 60)

| Points | What the grader checks |
|--------|------------------------|
| 20 | All required files exist |
| 15 | DAG is implemented (no `NotImplementedError`; has `@dag` + tasks) |
| 20 | Three tasks `ingest → dbt_run → dbt_test`, chained with `>>` |
| 20 | dbt runs via `uvx`; `retries` configured |
| 15 | Partition from the logical date (`{{ ds }}` / `logical_date`); `catchup=False` |
| 10 | `RUNBOOK.md` and `AI_ASSIST.md` filled in (no leftover `TODO`) |

## Submitting

Open a pull request against `main` with your implementation and the filled-in
docs. The autograder runs automatically and posts your score.

---

### For track maintainers

This repo is a template. The starter ships with `raise NotImplementedError`
stubs in `dags/taxi_pipeline.py` so a fresh clone scores only the "files exist"
level (20/100, fail). A complete solution scores 100/100. The autograder in
`.hyf/test.sh` is static (bash + sed + grep, no Airflow install), so it runs in
the shared HYF auto-grade CI without a Docker/Astro stack.
