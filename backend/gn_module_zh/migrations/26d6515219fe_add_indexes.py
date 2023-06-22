"""add indexes

Revision ID: 26d6515219fe
Revises: 22b14fc3abe0
Create Date: 2023-06-05 12:07:39.416188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "26d6515219fe"
down_revision = "22b14fc3abe0"
branch_labels = None
depends_on = None

SCHEMA = "pr_zh"


def upgrade():
    op.create_index("index_t_zh_id_sdage", table_name="t_zh", columns=["id_sdage"], schema=SCHEMA)
    op.create_index(
        "index_t_zh_id_thread", table_name="t_zh", columns=["id_thread"], schema=SCHEMA
    )
    op.create_index(
        "index_t_zh_id_diag_bio", table_name="t_zh", columns=["id_diag_bio"], schema=SCHEMA
    )
    op.create_index(
        "index_t_zh_id_diag_hydro", table_name="t_zh", columns=["id_diag_hydro"], schema=SCHEMA
    )
    op.create_index(
        "index_t_zh_id_lim_list", table_name="t_zh", columns=["id_lim_list"], schema=SCHEMA
    )
    op.create_index("index_t_zh_id_zh_uuid", table_name="t_zh", columns=["zh_uuid"], schema=SCHEMA)
    op.create_index(
        "index_cor_zh_rb_id_zh", table_name="cor_zh_rb", columns=["id_zh"], schema=SCHEMA
    )
    op.create_index(
        "index_cor_lim_list_id_lim_list",
        table_name="cor_lim_list",
        columns=["id_lim_list"],
        schema=SCHEMA,
    )
    op.create_index(
        "index_cor_zh_area_id_zh", table_name="cor_zh_area", columns=["id_zh"], schema=SCHEMA
    )
    op.create_index(
        "index_cor_zh_area_id_area", table_name="cor_zh_area", columns=["id_area"], schema=SCHEMA
    )


def downgrade():
    op.drop_index(
        "index_t_zh_id_sdage",
        table_name="t_zh",
        schema=SCHEMA,
    )
    op.drop_index(
        "index_t_zh_id_thread",
        table_name="t_zh",
        schema=SCHEMA,
    )
    op.drop_index(
        "index_t_zh_id_diag_bio",
        table_name="t_zh",
        schema=SCHEMA,
    )
    op.drop_index(
        "index_t_zh_id_diag_hydro",
        table_name="t_zh",
        schema=SCHEMA,
    )
    op.drop_index(
        "index_t_zh_id_lim_list",
        table_name="t_zh",
        schema=SCHEMA,
    )
    op.drop_index(
        "index_t_zh_id_zh_uuid",
        table_name="t_zh",
        schema=SCHEMA,
    )
    op.drop_index(
        "index_cor_zh_rb_id_zh",
        table_name="cor_zh_rb",
        schema=SCHEMA,
    )
    op.drop_index(
        "index_cor_lim_list_id_lim_list",
        table_name="cor_lim_list",
        schema=SCHEMA,
    )
    op.drop_index(
        "index_cor_zh_area_id_zh",
        table_name="cor_zh_area",
        schema=SCHEMA,
    )
    op.drop_index(
        "index_cor_zh_area_id_area",
        table_name="cor_zh_area",
        schema=SCHEMA,
    )
