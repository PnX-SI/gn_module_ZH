"""init zh

Revision ID: 01cb1aaa2062
Revises: 9e9218653d6c
Create Date: 2023-03-27 11:54:34.602380

"""
import importlib

from alembic import op
from sqlalchemy import func
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = "01cb1aaa2062"
down_revision = None
branch_labels = ("zones_humides",)
depends_on = None


def upgrade():
    local_srid = op.get_bind().execute(func.Find_SRID("ref_geo", "l_areas", "geom")).scalar()
    sql_structure = text(
        importlib.resources.read_text("gn_module_zh.migrations.data", "script_create_tables.sql")
    )
    nomenclatures_data = text(
        importlib.resources.read_text(
            "gn_module_zh.migrations.data", "insert_into_ref_nomenclatures_schema.sql"
        )
    )
    ref_geo_data = text(
        importlib.resources.read_text(
            "gn_module_zh.migrations.data", "insert_into_ref_geo_schema.sql"
        )
    )
    gn_commons_data = text(
        importlib.resources.read_text(
            "gn_module_zh.migrations.data", "insert_into_gn_commons_schema.sql"
        )
    )
    mandatory_data = text(
        importlib.resources.read_text(
            "gn_module_zh.migrations.data", "insert_into_pr_zh_schema.sql"
        )
    )

    atlas = text(
        importlib.resources.read_text("gn_module_zh.migrations.data", "insert_into_atlas_vm.sql")
    )

    op.get_bind().execute(sql_structure)
    op.get_bind().execute(nomenclatures_data)
    op.get_bind().execute(ref_geo_data)
    op.get_bind().execute(gn_commons_data)
    op.get_bind().execute(mandatory_data)
    op.get_bind().execute(atlas)


def downgrade():
    op.execute(
        """
        DROP SCHEMA IF EXISTS pr_zh CASCADE;
        DELETE FROM gn_commons.t_medias where id_table_location = (SELECT id_table_location FROM gn_commons.bib_tables_location WHERE table_desc = 'Liste des zones humides');

        DELETE FROM gn_commons.bib_tables_location WHERE table_desc = 'Liste des zones humides';

        DROP TABLE ref_geo.insee_regions;

        DELETE FROM ref_nomenclatures.defaults_nomenclatures_value WHERE mnemonique_type IN ('CRIT_DEF_ESP_FCT', 'EVAL_GLOB_MENACES', 'PERMANENCE_ENTREE', 'PERMANENCE_SORTIE', 'SUBMERSION_FREQ', 'SUBMERSION_ETENDUE', 'FONCTIONNALITE_HYDRO', 'FONCTIONNALITE_BIO', 'FONCTIONS_QUALIF', 'FONCTIONS_CONNAISSANCE', 'ETAT_CONSERVATION', 'STATUT_PROPRIETE', 'STATUT_PROTECTION', 'STRAT_GESTION');

        DELETE FROM ref_nomenclatures.t_nomenclatures WHERE source IN ('ZONES_HUMIDES', 'BASSINS_VERSANTS');

        DELETE FROM ref_nomenclatures.bib_nomenclatures_types WHERE source IN ('ZONES_HUMIDES', 'BASSINS_VERSANTS');

        """
    )
