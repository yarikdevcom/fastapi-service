## Bootstrap env
- install `pyenv` first to able to use `pyenv install 3.10.3`
- then use `pyenv shell 3.10.3` and `pip install poetry`
- `poetry install` to init your env
- `poetry run pre-commit run -a` to autoformat your code

## Project commands [inside `app/bin.py`]
- `poetry run test` -> runs docker compose containers and then runs tests
- `poetry run server` -> runs docker compose and starts dev server with auto reload
- `poetry run recreatemigrations` -> recreates initial migration, we can use this when service not deployed
- `poetry run makemigration {description}` -> create migration for db
- `poetry run migrate` -> upgrades to heads migration

## Manage packages
- use `poetry add {name}` to add package
- use `poetry add -D {name}` to add package only for development

## Code styleguide
- for first level module variables use `UPPER_CASE = 1` `API` etc.
- all new features should be placed at `features` module
- db tables always lower case `some_table_name`, values upper case, for example `CONTENT_TABLE = 'content', not 'contents'

## Helpful urls
- `REST` https://devhints.io/rest-api


## TODO:
- branch management:
    -> production branch (last production version with tag of latest release) -> auto commit creates a tag (not pushed into prod, only manually from github workflow -> workflow creates pull request into main rebase)
    -> hotfix/someshing needs to be fixed
    -> main branch (all stuff goes here)
    -> (feature or bugfix)/example-button branch from develop branch (service will create feautre-env -> all from develop + service for feature, all other services auto updated) -> could be fast forward
- add pipeline (python build with deps -> gitlab ci runner + cache)
- init `git branch production`

## Feature development
- New features located at `app.features` module -> to create new feature you can use command `poetry run feature <name>`
- This will create new folder with stub `API` and wired module inside app/__init__.py
- Feature structure:
    - `__init__.py` - includes global instances that could not be initialized by container, like `API` of `FastAPI` `APIRouter` instance
    - `models.py` - defines pydantic models for endpoints, DB objects and general object validation
    - `tables.py` - defines DB tables with keys, relations, indexes etc.
    - `services.py` - defines incapsulated part of reused or isolated part of logic
    - `managers.py` - defines aggregated flows using `services,resources` into business logic
    - `containers.py` - defines construction of all dependencies (services, managers, tables, etc.)
    - `api.py` - defines endpoints with injected container dependencies

- We need coverage report, mypylint
