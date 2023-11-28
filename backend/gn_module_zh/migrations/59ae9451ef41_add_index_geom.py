"""add index geom

Revision ID: 59ae9451ef41
Revises: 335377e24a52
Create Date: 2023-11-27 11:58:28.934602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "59ae9451ef41"
down_revision = "510677623a13"
branch_labels = None
depends_on = None

SCHEMA = "pr_zh"


def upgrade():
    op.create_index(
        "index_t_zh_geom",
        table_name="t_zh",
        columns=["geom"],
        schema=SCHEMA,
        postgresql_using="gist",
    )

    op.create_index(
        "index_t_river_basin_geom",
        table_name="t_river_basin",
        columns=["geom"],
        schema=SCHEMA,
        postgresql_using="gist",
    )

    op.create_index(
        "index_t_fct_area_geom",
        table_name="t_fct_area",
        columns=["geom"],
        schema=SCHEMA,
        postgresql_using="gist",
    )

    op.create_index(
        "index_t_hydro_area_geom",
        table_name="t_hydro_area",
        columns=["geom"],
        schema=SCHEMA,
        postgresql_using="gist",
    )


def downgrade():
    op.drop_index(
        "index_t_zh_geom",
        table_name="t_zh",
        schema=SCHEMA,
    )

    op.drop_index(
        "index_t_river_basin_geom",
        table_name="t_river_basin",
        schema=SCHEMA,
    )

    op.drop_index(
        "index_t_fct_area_geom",
        table_name="t_fct_area",
        schema=SCHEMA,
    )

    op.drop_index(
        "index_t_hydro_area_geom",
        table_name="t_hydro_area",
        schema=SCHEMA,
    )
