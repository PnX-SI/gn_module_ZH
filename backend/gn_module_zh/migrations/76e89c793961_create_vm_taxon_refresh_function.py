"""create_vm_taxon_refresh_function

Revision ID: 76e89c793961
Revises: c0c4748a597a
Create Date: 2024-04-16 08:12:41.346540

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "76e89c793961"
down_revision = "c0c4748a597a"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
            CREATE OR REPLACE FUNCTION pr_zh.refresh_taxon_materialized_views()
                RETURNS void
                LANGUAGE plpgsql
            AS $function$
            BEGIN
                REFRESH MATERIALIZED VIEW pr_zh.vm_vertebrates;
                REFRESH MATERIALIZED VIEW pr_zh.vm_invertebrates;
                REFRESH MATERIALIZED VIEW pr_zh.vm_flora;
            END;
            $function$
            ;
        """
    )


def downgrade():
    op.execute(
        """
            DROP FUNCTION pr_zh.refresh_taxon_materialized_views();
        """
    )
