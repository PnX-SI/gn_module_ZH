"""add_main_id_rb_column

Revision ID: 58ab8aba8512
Revises: 76e89c793961
Create Date: 2024-09-11 15:14:12.546662

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer


# revision identifiers, used by Alembic.
revision = "58ab8aba8512"
down_revision = "76e89c793961"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        schema="pr_zh",
        table_name="t_zh",
        column=Column(
            "main_id_rb",
            Integer,
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column(
        schema="pr_zh",
        table_name="t_zh",
        column_name="main_id_rb",
    )
