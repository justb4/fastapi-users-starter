"""Create FastAPI-Users user table

Revision ID: 787703593e67
Revises: 
Create Date: 2021-10-18 16:21:27.469806

"""
from alembic import op
import sqlalchemy as sa
# from fastapi_users.db.sqlalchemy import GUID
from fastapi_users_db_sqlalchemy import GUID


# revision identifiers, used by Alembic.
revision = '787703593e67'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table( # This tells Alembic that, when upgrading, a table needs to be created.
        "user", # The name of the table.
        sa.Column("id", GUID, primary_key=True), # The column "id" uses the custom type imported earlier.
        sa.Column(
            "email", sa.String(length=320), unique=True, index=True, nullable=False
        ),
        sa.Column("hashed_password", sa.String(length=72), nullable=False),
        sa.Column("is_active", sa.Boolean, default=True, nullable=False),
        sa.Column("is_superuser", sa.Boolean, default=False, nullable=False),
        sa.Column("is_verified", sa.Boolean, default=False, nullable=False),
    )


def downgrade():
    op.drop_table("user") # If we need to downgrade the database--in this case, that means restoring the database to being empty.
