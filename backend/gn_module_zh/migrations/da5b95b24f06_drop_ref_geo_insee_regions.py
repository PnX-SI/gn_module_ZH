"""drop ref_geo.insee_regions

Revision ID: da5b95b24f06
Revises: 72a8378567pa
Create Date: 2024-12-13 16:16:43.446953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "da5b95b24f06"
down_revision = "72a8378567pa"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table(table_name="insee_regions", schema="ref_geo")


def downgrade():
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS ref_geo.insee_regions (
            insee_reg varchar(2) NOT NULL, 
            region_name varchar(50) NOT NULL,
            CONSTRAINT pk_insee_regions_insee_code PRIMARY KEY ( insee_reg ),
            CONSTRAINT unq_insee_region_name UNIQUE ( region_name ) 
        );

        INSERT INTO ref_geo.insee_regions(insee_reg,region_name) VALUES
            ('01','Guadeloupe'),
            ('02','Martinique'),
            ('03','Guyane'),
            ('04','La Réunion'),
            ('06','Mayotte'),
            ('11','Île-de-France'),
            ('24','Centre-Val de Loire'),
            ('27','Bourgogne-Franche-Comté'),
            ('28','Normandie'),
            ('32','Hauts-de-France'),
            ('44','Grand Est'),
            ('52','Pays de la Loire'),
            ('53','Bretagne'),
            ('75','Nouvelle-Aquitaine'),
            ('76','Occitanie'),
            ('84','Auvergne-Rhône-Alpes'),
            ('93','Provence-Alpes-Côte d''Azur'),
            ('94','Corse')
            ON CONFLICT (insee_reg) DO NOTHING
        ;
        """
    )
