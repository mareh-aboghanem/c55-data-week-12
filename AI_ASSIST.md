# AI assistance log

<!-- Document at least one point where you used an LLM on this assignment.
     Never paste connection strings, passwords, or real data. Replace TODO. -->

## Use 1

**Prompt I sent:** "The dbt_run task failed with FATAL: password authentication failed for user. How do I fix this connection error in my Astro/Airflow project?"


**What the model answered:** The model explained that dbt reads database credentials from environment variables mapped in profiles.yml. It provided instructions to check the .env file for missing PostgreSQL variables (PG_USER, PG_PASSWORD, PG_SCHEMA) and suggested restarting the Astro environment (astro dev stop && astro dev start) before clearing the task in the Airflow UI.

**What I kept, changed, or discarded, and why:** Kept: The steps to add the missing PG_* variables into the .env file and restart Astro.

Changed: Kept sensitive information (like my actual password and username) local without saving them in shared code files.

Why: This directly solved the credential mismatch between Airflow and dbt while maintaining proper security practices for database credentials.