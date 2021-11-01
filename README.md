# FastAPI-Users Example

Based on blogpost:

https://harrisonmorgan.dev/2021/02/15/getting-started-with-fastapi-users-and-alembic/

Above Blogpost is from feb 2021. In the meantime FastAPI version and deps increased, so had to make some adaptations.
These are described below. 

Nice about the original example: all in one file [main.py](myapi/main.py). So to understand
the key workings of FastAPI+FastAPI-Users+SQLAlchemy[sqlite] together without jumping through
multiple files. 

## Install 

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