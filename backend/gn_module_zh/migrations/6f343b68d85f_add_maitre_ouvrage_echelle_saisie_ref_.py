"""Ajout des champs product_owner, input_scale, input_ref_geo à t_zh et ajout du champ is_product_owner dans bib_organismes

Revision ID: 6f343b68d85f
Revises: ea0eefb3744a
Create Date: 2025-07-28 15:44:17.558807

"""

from alembic import op
from sqlalchemy import Column, Integer, UnicodeText, Boolean


# revision identifiers, used by Alembic.
revision = "6f343b68d85f"
down_revision = "ea0eefb3744a"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        schema="pr_zh",
        table_name="t_zh",
        column=Column(
            "product_owner",
            UnicodeText,
            nullable=True,
        ),
    )
    op.add_column(
        schema="pr_zh",
        table_name="t_zh",
        column=Column(
            "input_scale",
            Integer,
            nullable=True,
        ),
    )
    op.add_column(
        schema="pr_zh",
        table_name="t_zh",
        column=Column(
            "input_ref_geo",
            UnicodeText,
            nullable=True,
        ),
    )
    op.add_column(
        schema="pr_zh",
        table_name="bib_organismes",
        column=Column(
            "is_product_owner",
            Boolean,
            default=True,
            nullable=True,
        ),
    )
    op.execute("UPDATE pr_zh.bib_organismes SET is_product_owner = true")
    op.alter_column(
        schema="pr_zh", table_name="bib_organismes", column_name="is_product_owner", nullable=False
    )

    # Add nommenclature type
    op.execute(
        """
        INSERT INTO
            ref_nomenclatures.bib_nomenclatures_types
        (
            mnemonique,
            label_default,
            definition_default,
            label_fr,
            definition_fr,
            source,
            statut
        )
        VALUES
            (
                'INPUT_SCALE',
                'Echelle de saisie',
                'Echelle de saisie',
                'Echelle de saisie',
                'Echelle de saisie',
                'ZONES_HUMIDES',
                'Non validé'
            ),
            (
                'INPUT_REF_GEO',
                'Référentiel de saisie',
                'Référentiel de saisie',
                'Référentiel de saisie',
                'Référentiel de saisie',
                'ZONES_HUMIDES',
                'Non validé'
            )
        """
    )

    # Add nommenclature
    op.execute(
        """
        INSERT INTO
            ref_nomenclatures.t_nomenclatures
        (
            id_type,
            cd_nomenclature,
            mnemonique,
            label_default,
            definition_default,
            label_fr,
            definition_fr,
            source,
            statut,
            active
        )
        VALUES
            (
                (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'INPUT_SCALE'),
                '2500',
                '2500',
                'Echelle de saisie 1/2500ème',
                'Echelle de saisie 1/2500ème',
                'Echelle de saisie 1/2500ème',
                'Echelle de saisie 1/2500ème',
                'ZONES_HUMIDES',
                'Non validé',
                true
            ),
            (
                (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'INPUT_SCALE'),
                '5000',
                '5000',
                'Echelle de saisie 1/5000ème',
                'Echelle de saisie 1/5000ème',
                'Echelle de saisie 1/5000ème',
                'Echelle de saisie 1/5000ème',
                'ZONES_HUMIDES',
                'Non validé',
                true
            ),
            (
                (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'INPUT_SCALE'),
                '10000',
                '10000',
                'Echelle de saisie 1/10000ème',
                'Echelle de saisie 1/10000ème',
                'Echelle de saisie 1/10000ème',
                'Echelle de saisie 1/10000ème',
                'ZONES_HUMIDES',
                'Non validé',
                true
            ),
            (
                (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'INPUT_SCALE'),
                '25000',
                '25000',
                'Echelle de saisie 1/25000ème',
                'Echelle de saisie 1/25000ème',
                'Echelle de saisie 1/25000ème',
                'Echelle de saisie 1/25000ème',
                'ZONES_HUMIDES',
                'Non validé',
                true
            )

        """
    )

    op.execute(
        """
        INSERT INTO
            ref_nomenclatures.t_nomenclatures
        (
            id_type,
            cd_nomenclature,
            mnemonique,
            label_default,
            definition_default,
            label_fr,
            definition_fr,
            source,
            statut,
            active
        )
        VALUES
            (
                (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'INPUT_REF_GEO'),
                'BD ORTHO®',
                'BD ORTHO®',
                'BD ORTHO®',
                'BD ORTHO®',
                'BD ORTHO®',
                'BD ORTHO®',
                'ZONES_HUMIDES',
                'Non validé',
                true
            ),
            (
                (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'INPUT_REF_GEO'),
                'SCAN 25®',
                'SCAN 25®',
                'SCAN 25®',
                'SCAN 25®',
                'SCAN 25®',
                'SCAN 25®',
                'ZONES_HUMIDES',
                'Non validé',
                true
            ),
            (
                (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'INPUT_REF_GEO'),
                'SCAN 100®',
                'SCAN 100®',
                'SCAN 100®',
                'SCAN 100®',
                'SCAN 100®',
                'SCAN 100®',
                'ZONES_HUMIDES',
                'Non validé',
                true
            ),
            (
                (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'INPUT_REF_GEO'),
                'OpenStreetMap',
                'OpenStreetMap',
                'OpenStreetMap',
                'OpenStreetMap',
                'OpenStreetMap',
                'OpenStreetMap',
                'ZONES_HUMIDES',
                'Non validé',
                true
            ),
            (
                (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'INPUT_REF_GEO'),
                'OpenTopoMap',
                'OpenTopoMap',
                'OpenTopoMap',
                'OpenTopoMap',
                'OpenTopoMap',
                'OpenTopoMap',
                'ZONES_HUMIDES',
                'Non validé',
                true
            )

        """
    )

    # Update atlas_app view
    op.execute("DROP VIEW IF EXISTS pr_zh.atlas_app")
    op.execute(
        """
        CREATE OR REPLACE VIEW pr_zh.atlas_app
            AS SELECT tzh.id_zh AS id,
                      tzh.main_name AS nom,
                      ( SELECT pr_zh.slugify(tzh.main_name::text) AS slugify) AS slug,
                      tzh.code,
                      tzh.create_date AS date,
                tzh.geom AS polygon_4326,
                tzh.product_owner,
                tzh.input_scale,
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

    # Rollback atlas_app view
    op.execute("DROP VIEW IF EXISTS pr_zh.atlas_app")
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

    op.execute(
        """
        DELETE FROM ref_nomenclatures.t_nomenclatures
        WHERE mnemonique IN ('2500', '5000', '10000', '25000', 'BD ORTHO®', 'SCAN 25®', 'SCAN 100®', 'OpenStreetMap', 'OpenTopoMap');
        """
    )
    op.execute(
        """
        DELETE FROM ref_nomenclatures.bib_nomenclatures_types
        WHERE mnemonique IN ('INPUT_REF_GEO', 'INPUT_SCALE');
        """
    )

    op.drop_column(
        schema="pr_zh",
        table_name="t_zh",
        column_name="product_owner",
    )
    op.drop_column(
        schema="pr_zh",
        table_name="t_zh",
        column_name="input_scale",
    )
    op.drop_column(
        schema="pr_zh",
        table_name="t_zh",
        column_name="input_ref_geo",
    )
    op.drop_column(
        schema="pr_zh",
        table_name="bib_organismes",
        column_name="is_product_owner",
    )
