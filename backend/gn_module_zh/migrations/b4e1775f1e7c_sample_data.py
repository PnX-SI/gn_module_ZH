"""sample data

Revision ID: b4e1775f1e7c
Revises: 01cb1aaa2062
Create Date: 2023-03-27 13:32:22.741263

"""
import importlib

from alembic import op
from sqlalchemy import func
from sqlalchemy.sql import text




# revision identifiers, used by Alembic.
revision = 'b4e1775f1e7c'
down_revision = None
branch_labels = ("zh-sample-data",)
depends_on = (
    "01cb1aaa2062",
)


def upgrade():
    data = text(
        importlib.resources.read_text("gn_module_zh.migrations.data", "insert_into_fake_data.sql")
    )
    op.get_bind().execute(data)



def downgrade():
    pass
