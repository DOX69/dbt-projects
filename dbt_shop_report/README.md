# Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices

# Build
Do not forget to go to your working project using cd command.  
## Config
dbt_project.yml is where you define your configurations. You can also do it inside block of sql or properties.yml in the folder models. The priority of config is : ***block > properties > dbt_project.yml**
## Models
Your sql models have to be create in `models` folder. You can set there all your sql transformation
## Macros
You can define your generated schema and may more.

# Run
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

_Note:_ When creating jinja macros, use {%%} when you have double quote "". And '-' {%-...-%} to avoid empty line in compile.  
Jinja can be used in .sql file to explore and also to create macro in /macros folder.