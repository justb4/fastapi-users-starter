import uvicorn
from typing import Optional

import databases
from fastapi import FastAPI
from fastapi_users import models as user_models
from fastapi_users import db as users_db
from fastapi_users.authentication import CookieAuthentication
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase

import sqlalchemy as sa
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

DATABASE_URL = 'sqlite:///./test.db'
SECRET = 'SECRET'  # CHANGE THIS!!


class User(user_models.BaseUser):
    pass


class UserCreate(user_models.BaseUserCreate):
    pass


class UserUpdate(User, user_models.BaseUserUpdate):
    pass


class UserDB(User, user_models.BaseUserDB):
    pass


database = databases.Database(DATABASE_URL)

Base: DeclarativeMeta = declarative_base()


class UserTable(Base, users_db.SQLAlchemyBaseUserTable):
    pass


engine = sa.create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

users = UserTable.__table__


# OLD: user_db = users_db.SQLAlchemyUserDatabase(UserDB, database, users)
def get_user_db():
    yield users_db.SQLAlchemyUserDatabase(UserDB, database, users)


cookie_authentication = CookieAuthentication(secret=SECRET, lifetime_seconds=3600)

app = FastAPI()


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    # added: defaultcallback actions, just a print().
    async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
        print(f'User {user.id} has registered.')

    async def on_after_forgot_password(self, user: UserDB, token: str, request: Optional[Request] = None):
        print(f'User {user.id} has forgot their password. Reset token: {token}')

    async def on_after_request_verify(self, user: UserDB, token: str, request: Optional[Request] = None):
        print(f'Verification requested for user {user.id}. Verification token: {token}')


def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


# OLD: jwt_authentication = JWTAuthentication(
#     secret=SECRET, lifetime_seconds=3600, tokenUrl='auth/jwt/login'
# )

# OLD: fastapi_users = FastAPIUsers(
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


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


app.include_router(
    fastapi_users.get_auth_router(cookie_authentication),
    prefix='/auth/jwt',
    tags=['auth'],
)
# See https://fastapi-users.github.io/fastapi-users/configuration/routers/reset/
app.include_router(
    fastapi_users.get_register_router(), prefix='/auth', tags=['auth']
)
# OLD: app.include_router(
#     fastapi_users.get_reset_password_router(SECRET), prefix='/auth', tags=['auth'],
# )
app.include_router(
    fastapi_users.get_reset_password_router(), prefix='/auth', tags=['auth'],
)
app.include_router(fastapi_users.get_users_router(), prefix='/users', tags=['users'])

# ADDED:
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
