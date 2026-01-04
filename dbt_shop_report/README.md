# Sales Data Project

# Resources:

- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices


# Config

dbt_project.yml is where you define your configurations. You can also do it inside block of sql or properties.yml in the folder models. The priority of config is : **block > properties > dbt_project.yml**

# Models

Your sql models have to be create in `models` folder. You can set there all your sql transformation

# Run models

Run all the models :  
`dbt run`

## Run **node selection**

Run specific model :  
`dbt run --select <model_name>`    
Run multiple specific model :  
`dbt run --select "<model_name_1> <model_name_2>"`    
Run model folder :  
`dbt run --select "model/folder"`  

# Tests

command :  
`dbt test`

## Generic tests

### [Data tests](https://docs.getdbt.com/docs/build/data-tests)

- unique
- not_null
- accepted_values
- relationship

You can add a warning instead of failure by adding `severity: warn` in your column data_tests.

### Singular tests

When you want to test a logic or KPI. You can specify in tests folder **sql query that search for invalid rows**.

## Custom generic tests

Go to tests/generic and create a .sql file that test a column_name in a model. Like singular tests, you have to **find invalid results in test sql**

# [Seeds](https://docs.getdbt.com/docs/build/seeds)

For lookup table and mapping files from **csv file** in your desired schema and desired Catalog.  
Do not forget to add 'seeds' dbt_project.yml file.  
Run using `dbt seed`

# Analyses

It's for exploration, analysises and tests

# [Jinja macros](https://docs.getdbt.com/docs/build/jinja-macros)

In dbt, you can combine SQL with Jinja, a templating language.

Using Jinja turns your dbt project into a programming environment for SQL, giving you the ability to do things that aren't normally possible in SQL. It's important to note that Jinja itself isn't a programming language; instead, it acts as a tool to enhance and extend the capabilities of SQL within your dbt projects.  
You can define your generated schema and many more.

_Note:_ When creating jinja macros, use `{% ... %}` for control statements, and `{%- ... -%}` to avoid empty lines in compiled SQL. If your content contains double quotes, use proper escaping within Jinja.
Jinja can be used in .sql file to explore and also to create macro in /macros folder.

# [Snapshots](https://docs.getdbt.com/docs/build/snapshots)

Here we will create a slowly changing dimension type 2 (SCD 2) table. In order to do that, we will create a yaml file in the snapshots folder.  
The two main config are :

- unique_key : the primary key of the table
- strategy : The snapshot strategy to use. Valid values: timestamp or check

```yml
snapshots:
  - name: <snapshot_name>
    relation: source(<schema_name>, <source_table_name>) # use relation: ref(<model_name>) to snapshot a model
    config:
      unique_key: id # or [id1, id2,...] for composite key
      strategy: timestamp
```

Run using `dbt snapshot`

# Build all

Do not forget to go to your working project using cd command. Then run :  
`dbt build`  
By default, this command run target object in dev with all sources, from prod.  
use `--target <target_name>` to run in another target defined in profiles.yml.  
E.g. `dbt build --target prod`

A clearer beginner-friendly README can introduce dbt concepts, show where to put code, then give copy‑pasteable commands and links to go deeper.
***

## Sales Data Project

This project uses **dbt** (data build tool) to transform raw sales data into clean, analytics‑ready tables in your data warehouse.

### Learning resources

- Learn dbt concepts in the official docs: https://docs.getdbt.com/docs/introduction
- Ask questions or search issues on the dbt Community Discourse: https://discourse.getdbt.com
- Read articles on best practices on the dbt blog: https://blog.getdbt.com
- Follow a hands‑on quickstart (recommended for beginners): https://docs.getdbt.com/docs/get-started-dbt

***

## Project configuration

dbt configurations control how models are built (as tables/views, schema, tags, etc.).

- Global project‑level config: `dbt_project.yml` at the root of the repo.
- Model or folder config in YAML: `models/**/schema.yml` or `properties.yml` for model‑specific settings and tests.
- Inline config in a model: Jinja `{{ config(...) }}` block at the top of a `.sql` file.

**Config precedence (highest to lowest):**

1. Inline config block in the model file
2. YAML properties (e.g. `schema.yml`)
3. `dbt_project.yml`

So the effective priority is: **inline config > properties YAML > dbt_project.yml**.

***

## Models and how to run them

In dbt, a **model** is a `.sql` file containing a single `select` statement.

### Where models live

- Put all transformation SQL in the `models/` folder.
- Each `.sql` file = one model; the file name becomes the relation name in the warehouse (unless overridden by config).
- You can use subfolders (for example: `models/staging/`, `models/marts/`).

Example:

```sql
-- models/stg_orders.sql
select
  id,
  customer_id,
  order_date,
  total_amount
from {{ source('raw', 'orders') }}
```


### Running models

From the project root (where `dbt_project.yml` lives):

- Run **all** models:

```bash
dbt run
```

- Run **one** model:

```bash
dbt run --select <model_name>
```

- Run **multiple** models:

```bash
dbt run --select "<model_name_1> <model_name_2>"
```

- Run all models in a **folder**:

```bash
dbt run --select models/<folder_name>
```


Node selection is very powerful; see more patterns in the docs.

***

## Tests and data quality

dbt tests help you ensure your models and columns behave as expected.

### Running tests

- Run all tests defined in the project:

```bash
dbt test
```

- Run tests for a specific model:

```bash
dbt test --select <model_name>
```


### Generic (schema) tests

Generic tests are configured in YAML (for example in `schema.yml`) and applied to columns.
Common built‑in tests:

- **unique**
- **not_null**
- **accepted_values**
- **relationships**

Example:

```yml
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - not_null
          - unique
      - name: status
        tests:
          - accepted_values:
              values: ['pending', 'completed', 'cancelled']
```

Turn a test **warning** instead of failure:

```yml
      - name: status
        tests:
          - accepted_values:
              values: ['pending', 'completed', 'cancelled']
              severity: warn
```


### Singular tests

Use a singular test when you want to express a custom rule as a query that returns **invalid rows**.

- Create a `.sql` file in `tests/` (for example, `tests/no_negative_order_amounts.sql`).
- The query must return rows that violate the expectation.

```sql
-- tests/no_negative_order_amounts.sql
select *
from {{ ref('fct_orders') }}
where total_amount < 0
```

If this query returns any rows, the test fails.

### Custom generic tests

Custom generic tests let you reuse test logic across multiple models.

- Create a `.sql` file under `tests/generic/` (for example, `tests/generic/not_null_non_zero.sql`).
- The SQL defines a macro‑style test that checks a column and returns invalid rows.
- Then reference that test by name in your YAML tests.

See “Writing custom generic tests” in the dbt docs for exact macro syntax.

***

## Seeds (static CSV data)

Seeds are version‑controlled CSV files in your project that dbt can load into your warehouse as tables.

Typical use cases:

- Lookup and mapping tables (for example, country code → country name).
- Small, relatively static reference data.


### How to use seeds

1. Place CSV files under the `seeds/` directory (for example: `seeds/country_codes.csv`).
2. Ensure you have a `seeds:` section in `dbt_project.yml` if you need custom configs (schema, quoting, delimiters, etc.).
3. Load all seeds:

```bash
dbt seed
```

4. Reference a seed in a model using `ref()` just like any other model:
```sql
select
  o.*,
  c.country_name
from {{ ref('fct_orders') }} o
left join {{ ref('country_codes') }} c
  on o.country_code = c.country_code
```

Official seeds docs: https://docs.getdbt.com/docs/build/seeds

***

## Analyses

The `analyses/` directory is for ad‑hoc queries you want to keep under version control but **not** materialize as models.

- Useful for explorations, experiments, and one‑off reports.
- Analyses are not built by `dbt run`; you can open or run them via dbt’s UI or your warehouse directly.

***

## Jinja and macros

dbt lets you combine SQL and **Jinja** templating to write reusable, DRY logic.

### Using Jinja in SQL

You can embed Jinja in `.sql` models for:

- Control flow (`{% if %}`, `{% for %}`)
- Reusable macros (`{{ my_macro(...) }}`)
- Dynamic schemas, table names, or filters

Example:

```sql
{% set recent_days = 30 %}

select *
from {{ ref('fct_orders') }}
where order_date >= current_date - interval '{{ recent_days }} day'
```

Guidance:

- Use `{% ... %}` for control structures and `{{ ... }}` for expressions.
- Use `{%- ... -%}` to trim whitespace and avoid empty lines in the compiled SQL.
- Put shared macros in the `macros/` directory so they can be reused across models.

Macro docs: https://docs.getdbt.com/docs/build/jinja-macros

***

## Snapshots (history over time)

Snapshots let you track changes to mutable records and implement SCD Type 2 dimensions.

### When to use snapshots

- Source tables get updated in place and don’t keep history.
- You need a historical view of customers, products, or other slowly changing dimensions.


### How to define a snapshot

1. Create a `.sql` snapshot file under `snapshots/` (for example, `snapshots/customers.sql`).
2. Use the `snapshot` Jinja block and configure `unique_key`, `strategy`, and strategy‑specific fields.

Example (timestamp strategy):

```sql
{% snapshot customers_snapshot %}

{{
  config(
    target_schema='snapshots',
    unique_key='id',
    strategy='timestamp',
    updated_at='updated_at'
  )
}}

select *
from {{ source('raw', 'customers') }}

{% endsnapshot %}
```

Key configs:

- **unique_key**: business key or primary key (can be composite).
- **strategy**: `timestamp` or `check`, depending on how you detect changes.

Run the snapshot process:

```bash
dbt snapshot
```

Official snapshots docs: https://docs.getdbt.com/docs/build/snapshots

***

## Building the full project

`dbt build` runs models, tests, and (optionally) snapshots in one command.

Typical workflow from the project root:

```bash
# Build everything (models + tests + snapshots + seeds)
dbt build
```

Notes:

- Ensure you are in the project directory (where `dbt_project.yml` is) before running commands.
- By default, dbt uses the target defined in `profiles.yml` (often `dev`). Use another target with:

```bash
dbt build --target <target_name>
```

Example for production:

```bash
dbt build --target prod
```
