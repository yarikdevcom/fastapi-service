## Bootstrap env
- install `pyenv` first to able to use `pyenv install 3.10.1`
- then use `pyenv use 3.10.1` and `pip install poetry`
- `poetry install` to init your env
- `poetry run pre-commit install` to autoformat your code

## Project commands [inside `app/bin.py`]
- `poetry run test` -> runs docker compose containers and then runs tests
- `poetry run server` -> runs docker compose and starts dev server with auto reload
- `poetry run remigrate` -> recreates initial migration, we can use this when service not deployed
- `poetry run migrate {description}` -> create migration for db
- `poetry run upgrade` -> upgrades to heads migration

## Manage packages
- use `poetry add {name}` to add package
- use `poetry add -D {name}` to add package only for development

## Code styleguide
- for first level module variables use `UPPER_CASE = 1`
- db tables always lower case `some_table_name`

## Helpful urls
- `REST` https://devhints.io/rest-api
