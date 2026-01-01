# Intallation :
- PyCharm
- Install git
- Create databricks free edition account
- Python 3.9 (Don't forget to add python.exe to PATH during installation)
- uv
# Initialization
## Init uv
After creating a new project in PyCharm from .venv python 3.9, run :
```PowerShell
uv init
uv sync
```
## Install dbt-core and databricks adapter
```PowerShell
uv add dbt-core dbt-databricks
```
Note: if you want to have the current required packages txt file, run : `uv pip freeze > requirements.txt` 
## Init dbt
```PowerShell
dbt init
```
- Give it an explicit name.
- Here we are using [1] databricks, so enter 1.
- Past your host : databricks UI > compute > SQL warehouse > [click on compute name you want to use] > Connection details > [Copy and past the Server hostname]
- Same as previous step for http_path
- Enter 1 and create access token : settings > developer > Access Token > manage > [Generate access token] > Paste it using ctrl+V ,**it will show nothing, it's normal, but the token is there don't worry** > [click on enter]
- Enter 1 to use unity Catalog and provide catalog name and schema name you want to use  

**Test the connection:**  
```PowerShell
cd <project_name>
dbt debug
```
You will notice that there is an error : ` dbt_project.yml file [ERROR not found]`.  
Just go to the right directory using `cd <project_name>` command to resolve it.  

If you have other error like invalid access token, rerun `dbt init` **inside the project you want to overwrite** and try again.

Sometimes Windows is blocking the activation script for your virtual environment because of PowerShell’s execution policy. You need either to relax the policy (ideally just for your user or the current shell) or use an alternative shell. In that case, you will have an error when activate you virtual environment. To fix this, run :
```PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
. C:\Users\<your_user>\<full_path_directory_to_your_project>\.venv\Scripts\Activate.ps1
```
Then restart terminal