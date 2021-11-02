# FastAPI Users Starter

This is a template repo to get you started with FastAPI + FastAPI Users.

When you develop your [FastAPI](https://fastapi.tiangolo.com/) project, at some point you will need auth and users. 
[FastAPI Users](https://fastapi-users.github.io/fastapi-users/) 
provides *"Ready-to-use and customizable users management for FastAPI"*.
There are several examples like [this](https://github.com/tiangolo/full-stack-fastapi-postgresql) 
and [this](https://testdriven.io/blog/developing-a-single-page-app-with-fasta) to get you started with full stack FastAPI. 
But to get grip on the very basics of FastAPI Users I found this blogpost:

https://harrisonmorgan.dev/2021/02/15/getting-started-with-fastapi-users-and-alembic/

Credits here to https://harrisonmorgan.dev ! And off course also 
to [FastAPI Users Devs](https://github.com/fastapi-users/fastapi-users) and [FastAPI Devs](https://fastapi.tiangolo.com/)!

Above Blogpost is from feb 2021. In the meantime FastAPI version and deps increased, so had to make some adaptations.
These are described below. 

Great about the original example: all in one file [main.py](myapi/main.py). So to understand
the key workings of FastAPI+FastAPI-Users+SQLAlchemy[sqlite] together without jumping through
multiple files. 

This GitHub starter project has done most of the steps for Poetry and Alembic from the blogpost, as to
give you a super quick start! But for complete understanding be sure to go through the blogpost.

## Quickstart

Make sure you have a virtual env. I use [pyenv](https://github.com/pyenv/pyenv) via Homebrew 
on Mac OSX. Example uses [poetry](https://python-poetry.org/) which was new to me.
NB if you want to use regular Python `venv` and `pip` then just do the following:

```bash

# Suppose we work from this dir, or better create new repo from Template in GitHub
git clone https://github.com/justb4/fastapi-users-starter.git fastapi-users-starter
cd fastapi-users-starter

python -m venv virtenv
. virtenv/bin/activate

pip install -r requirements.txt
alembic upgrade head
python -m myapi.main

# now continue below at the line
"# Open this URL in browser"


```
 
Below is the full `pyenv` and Poetry-based version as from the blogpost:


```bash

# Virtual Env for Python 3.8.9
pyenv virtualenv 3.8.9 fastapi-3.8.9
pyenv activate fastapi-3.8.9

# https://python-poetry.org/
pip install poetry

# Suppose we work from this dir, or better create new repo from Template in GitHub
git clone https://github.com/justb4/fastapi-users-starter.git fastapi-users-starter
cd fastapi-users-starter

# poetry init is not required as we already have the pyproject.toml file

# Install all packages/dependencies ala pip
poetry install

# Create initial DB by running Alembic Upgrade
poetry run alembic upgrade head

# You should see
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 787703593e67, Create FastAPI-Users user table

# Run
poetry run uvicorn myapi.main:app

# You should see
INFO:     Started server process [84094]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

# Open this URL in browser
http://127.0.0.1:8000/docs

# register yourself as user: browse to 
http://127.0.0.1:8000/docs#/auth/register_auth_register_post

# fill in email + password, output should print like
INFO:     127.0.0.1:62127 - "GET /openapi.json HTTP/1.1" 200 OK
User cca66e0b-4480-41c6-a95e-... has registered.
INFO:     127.0.0.1:62269 - "POST /auth/register HTTP/1.1" 201 Created

# Logging in with JWT

# first try gives 401 unauthorized
http://127.0.0.1:8000/docs#/users/me_users_me_get
 INFO:     127.0.0.1:62956 - "GET /users/me HTTP/1.1" 401 Unauthorized
 
# login with username/password, JWT cookie will be set in browser
http://127.0.0.1:8000/docs#/auth/login_auth_jwt_login_post
 INFO:     127.0.0.1:63100 - "POST /auth/jwt/login HTTP/1.1" 200 OK

# try again, now ok
http://127.0.0.1:8000/docs#/users/me_users_me_get
 INFO:     127.0.0.1:63234 - "GET /users/me HTTP/1.1" 200 OK


```


## Full Install 

These are some of the steps I followed from the original blogpost with my own changes. 
This is for reference as the Quickstart above will cover initial setup.

Make sure you have a virtual env. I use [pyenv](https://github.com/pyenv/pyenv) via Homebrew 
on Mac OSX. Example uses [poetry](https://python-poetry.org/) which was new to me.

```bash

# Virtual Env for Python 3.8.9
pyenv virtualenv 3.8.9 fastapi-3.8.9
pyenv activate fastapi-3.8.9

# https://python-poetry.org/
pip install poetry

cd ~/research/fastapi/fastapi-users-starter
poetry init
# skip interactive package adding

poetry add fastapi==0.70.0
poetry add fastapi-users[sqlalchemy]==8.1.1
poetry add databases[sqlite]
poetry add alembic==1.7.4

# had to add 
poetry add uvicorn==0.15.0
```

## Changes from Blogpost
 
These are the changes I made.

### Upgrade versions:

* fastapi==0.70.0
* fastapi-users[sqlalchemy]==8.1.1
* databases[sqlite]
* alembic==1.7.4

```bash
# had to add 
poetry add uvicorn==0.15.0

# Full entry in pyproject.toml
[tool.poetry.dependencies]
python = "^3.8"
fastapi = "0.70.0"
fastapi-users = {version = "8.1.1", extras = ["sqlalchemy"]}
databases = {extras = ["sqlite"], version = "^0.5.3"}
alembic = "1.7.4"
uvicorn = "0.15.0"

```
 
### Changes to main.py
 
These are my changes to [main.py](myapi/main.py)

```python


# See https://fastapi-users.github.io/fastapi-users/configuration/databases/sqlalchemy/
# user_db = users_db.SQLAlchemyUserDatabase(UserDB, database, users)
def user_db():
    yield users_db.SQLAlchemyUserDatabase(UserDB, database, users)

# user_db must be a callable

# See https://fastapi-users.github.io/fastapi-users/configuration/routers/reset/
# app.include_router(
#     fastapi_users.get_reset_password_router(SECRET), prefix="/auth", tags=["auth"],
# )
app.include_router(
    fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"],
)

# In Alembic Migration script (and Blog text)
# from fastapi_users.db.sqlalchemy import GUID
from fastapi_users_db_sqlalchemy import GUID

```
New constructor of `FastAPIUsers`.

```

class UserManager(BaseUserManager[UserCreate, UserDB]):
  user_db_model = UserDB
  reset_password_token_secret = SECRET
  verification_token_secret = SECRET

def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
  yield UserManager(user_db)


# fastapi_users = FastAPIUsers(
#     user_db, [cookie_authentication], User, UserCreate, UserUpdate, UserDB,
# )


fastapi_users = FastAPIUsers(
    get_user_manager,
    [cookie_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

# Added to run in debugger as well
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

```