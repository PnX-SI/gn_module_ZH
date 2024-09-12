"""add_main_id_rb_column

Revision ID: 72a8378567pa
Revises: 58ab8aba8512
Create Date: 2024-09-11 17:18:21.165324

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "72a8378567pa"
down_revision = "58ab8aba8512"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        UPDATE pr_zh.t_zh tzh 
        SET main_id_rb = 
        (
            SELECT id_rb 
            FROM (
                SELECT
                    czr.id_rb AS id_rb, 
                    ST_Area(ST_Intersection(
                        ST_GeomFromText(ST_AsText((SELECT geom FROM pr_zh.t_zh WHERE id_zh = tzh.id_zh ))),
                        ST_GeomFromText(ST_AsText(trb.geom))
                    )) AS areas									
                FROM pr_zh.cor_zh_rb czr
                LEFT JOIN pr_zh.t_river_basin trb ON trb.id_rb = czr.id_rb
                WHERE czr.id_zh = tzh.id_zh 
                ORDER BY areas DESC
                LIMIT 1
            ) AS a
        )
        """
    )


def downgrade():
    op.execute(
        """
        UPDATE pr_zh.t_zh tzh 
        SET main_id_rb = null
        """
    )
