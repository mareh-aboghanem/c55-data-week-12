# Put your dbt project here

Your `dbt_run` / `dbt_test` tasks run dbt against a project mounted at
`include/dbt_project/`. Astro mounts this folder into the container at
`/usr/local/airflow/include/dbt_project`.

Use **one** of these:

1. **Your own Week 10 project.** Copy your `nyc-taxi-dbt` models, `dbt_project.yml`,
   and `profiles.yml` into this directory.
2. **The class reference project** (if your Week 10 project is not runnable):

   ```bash
   git clone https://github.com/lassebenni/nyc-taxi-airflow-reference /tmp/class-ref
   cp -r /tmp/class-ref/include/dbt_project/. include/dbt_project/
   ```

Document which one you used in `ASSIGNMENT_REPORT.md`.

> The dbt tasks call dbt through `uvx --python 3.11`, so you do **not** put
> `dbt-core` in `requirements.txt`. See Chapter 4 for the exact command.
