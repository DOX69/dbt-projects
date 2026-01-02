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
`dbt run --select "model\folder"`

# Tests
## Generic tests
### [Data tests](https://docs.getdbt.com/docs/build/data-tests)
- unique
- not_null
- accepted_values
- relationship