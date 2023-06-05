"""add atlas view

Revision ID: 643743e807f6
Revises: 26d6515219fe
Create Date: 2023-06-05 12:20:36.897280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "643743e807f6"
down_revision = "26d6515219fe"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE OR REPLACE FUNCTION pr_zh.slugify("value" TEXT)
        RETURNS TEXT AS $$
        -- removes accents (diacritic signs) from a given string --
        WITH "unaccented" AS (
            SELECT unaccent("value") AS "value"
        ),
        -- lowercases the string
        "lowercase" AS (
            SELECT lower("value") AS "value"
            FROM "unaccented"
        ),
        -- replaces anything that's not a letter, number, hyphen('-'), or underscore('_') with a hyphen('-')
        "hyphenated" AS (
            SELECT regexp_replace("value", '[^a-z0-9\\-_]+', '-', 'gi') AS "value"
            FROM "lowercase"
        ),
        -- trims hyphens('-') if they exist on the head or tail of the string
        "trimmed" AS (
            SELECT regexp_replace(regexp_replace("value", '\\-+$', ''), '^\\-', '') AS "value"
            FROM "hyphenated"
        )
        SELECT "value" FROM "trimmed";
        $$ LANGUAGE SQL STRICT IMMUTABLE;
    """
    )
    op.execute(
        """
        CREATE OR REPLACE VIEW pr_zh.atlas_app
            AS SELECT tzh.id_zh AS id,
                tzh.main_name AS nom,
                ( SELECT pr_zh.slugify(tzh.main_name::text) AS slugify) AS slug,
                tzh.code,
                tzh.create_date AS date,
                tzh.geom AS polygon_4326,
                ( SELECT st_area(st_transform(st_setsrid(tzh.geom, 4326), 2154)) AS st_area) AS superficie,
                bo.nom_organisme AS operateur,
                sdage.cd_nomenclature AS type_code,
                sdage.mnemonique AS type,
                thread.mnemonique AS menaces,
                diag_bio.mnemonique AS diagnostic_bio,
                diag_hydro.mnemonique AS diagnostic_hydro,
                ( SELECT array_agg(DISTINCT tn.mnemonique) AS array_agg) AS criteres_delim,
                ( SELECT array_agg(DISTINCT la.area_name) AS array_agg) AS communes,
                ( SELECT array_agg(DISTINCT trb.name) AS array_agg) AS bassin_versant,
                ( SELECT COALESCE(json_agg(t.*), '[]'::json) AS "coalesce"
                    FROM ( SELECT t_medias.title_fr AS label,
                                t_medias.media_path AS url
                            FROM gn_commons.t_medias
                            WHERE t_medias.uuid_attached_row = tzh.zh_uuid) t) AS images
            FROM pr_zh.t_zh tzh
                LEFT JOIN pr_zh.cor_lim_list cll ON tzh.id_lim_list = cll.id_lim_list
                LEFT JOIN ref_nomenclatures.t_nomenclatures tn ON cll.id_lim = tn.id_nomenclature
                LEFT JOIN pr_zh.cor_zh_area cza ON tzh.id_zh = cza.id_zh
                LEFT JOIN ref_geo.l_areas la ON cza.id_area = la.id_area
                LEFT JOIN pr_zh.cor_zh_rb czr ON tzh.id_zh = czr.id_zh
                LEFT JOIN pr_zh.t_river_basin trb ON czr.id_rb = trb.id_rb
                LEFT JOIN gn_commons.t_medias med ON med.uuid_attached_row = tzh.zh_uuid
                LEFT JOIN utilisateurs.t_roles tr ON tr.id_role = tzh.create_author
                LEFT JOIN utilisateurs.bib_organismes bo ON bo.id_organisme = tr.id_organisme
                LEFT JOIN ref_nomenclatures.t_nomenclatures sdage ON sdage.id_nomenclature = tzh.id_sdage
                LEFT JOIN ref_nomenclatures.t_nomenclatures thread ON thread.id_nomenclature = tzh.id_thread
                LEFT JOIN ref_nomenclatures.t_nomenclatures diag_bio ON diag_bio.id_nomenclature = tzh.id_diag_bio
                LEFT JOIN ref_nomenclatures.t_nomenclatures diag_hydro ON diag_hydro.id_nomenclature = tzh.id_diag_hydro
            WHERE cza.cover IS NOT NULL
            GROUP BY tzh.id_zh, bo.nom_organisme, sdage.cd_nomenclature, sdage.mnemonique, thread.mnemonique, diag_bio.mnemonique, diag_hydro.mnemonique
            ORDER BY tzh.id_zh;
        """
    )


def downgrade():
    op.execute("DROP VIEW pr_zh.atlas_app")
    op.execute("DROP FUNCTION pr_zh.slugify")
