"""change fk_cor_zh_area_id_area ondelete="CASCADE"

Revision ID: 39aada275204
Revises: 1a2b3c4d5e6f
Create Date: 2026-08-26 16:17:50.837018

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "39aada275204"
down_revision = "1a2b3c4d5e6f"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("fk_cor_zh_area_id_area", table_name="cor_zh_area", schema="pr_zh")
    op.create_foreign_key(
        "fk_cor_zh_area_id_area",
        source_schema="pr_zh",
        source_table="cor_zh_area",
        local_cols=["id_area"],
        referent_schema="ref_geo",
        referent_table="l_areas",
        remote_cols=["id_area"],
        onupdate="CASCADE",
        ondelete="CASCADE",  # the modified value
    )


def downgrade():
    op.drop_constraint("fk_cor_zh_area_id_area", table_name="cor_zh_area", schema="pr_zh")
    op.create_foreign_key(
        "fk_cor_zh_area_id_area",
        source_schema="pr_zh",
        source_table="cor_zh_area",
        local_cols=["id_area"],
        referent_schema="ref_geo",
        referent_table="l_areas",
        remote_cols=["id_area"],
        onupdate="CASCADE",
        ondelete="NO ACTION",
    )
