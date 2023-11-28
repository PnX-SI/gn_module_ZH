"""optimize view vertebrates invertebrates flora

Revision ID: 335377e24a52
Revises: 510677623a13
Create Date: 2023-11-27 09:53:25.508645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "335377e24a52"
down_revision = "510677623a13"
branch_labels = None
depends_on = None


def upgrade():
    # FLORA
    # deleting old view
    op.execute("DROP VIEW pr_zh.flora;")
    # creating old view
    op.execute(
        """
    CREATE OR REPLACE VIEW pr_zh.flora
    AS WITH synthese_zh AS (
        SELECT DISTINCT ON (t_zh.id_zh, synthese.cd_nom) synthese.id_synthese,
            t_zh.id_zh,
            synthese.cd_nom,
            synthese.date_max,
            synthese.observers,
		    vu.organisme
		FROM gn_synthese.synthese
        JOIN pr_zh.t_zh ON st_intersects(st_setsrid(t_zh.geom, 4326), synthese.the_geom_point)
		JOIN utilisateurs.v_userslist_forall_applications vu ON ((vu.nom_role::text || ' '::text) || vu.prenom_role::text) = synthese.observers::text
        ORDER BY t_zh.id_zh, synthese.cd_nom, synthese.date_max DESC
        ), bdc_statut AS (
        SELECT bdc_statut_1.cd_nom,
            bdc_statut_1.cd_sig,
            bdc_statut_1.regroupement_type AS statut_type,
            (bdc_statut_1.lb_type_statut::text || ' - '::text) || bdc_statut_1.label_statut::text
               AS statut,
            bdc_statut_1.full_citation AS article,
            bdc_statut_1.doc_url
        FROM taxonomie.bdc_statut bdc_statut_1
        WHERE bdc_statut_1.regroupement_type::text = 'Liste rouge'::text 
            AND (bdc_statut_1.code_statut::text = ANY (ARRAY[
               'VU'::character varying, 'EN'::character varying, 'CR'::character varying]::text[])) 
            OR (bdc_statut_1.regroupement_type::text = ANY (ARRAY[
               'ZNIEFF'::character varying, 'Réglementation'::character varying, 
               'Protection'::character varying, 'Directives européennes'::character varying]::text[]
            ))
    )
    SELECT synthese_zh.id_zh,
        taxref.cd_nom,
        taxref.classe AS group_class,
        taxref.ordre AS group_order,
        taxref.nom_complet AS scientific_name,
        taxref.nom_vern AS vernac_name,
        bdc_statut.statut_type,
        bdc_statut.statut,
        bdc_statut.article,
        bdc_statut.doc_url,
        synthese_zh.date_max AS last_date,
        synthese_zh.observers AS observer,
        synthese_zh.organisme,
        (( SELECT count(sy.cd_nom) AS count
            FROM synthese_zh sy
            WHERE sy.id_zh = synthese_zh.id_zh AND sy.cd_nom = taxref.cd_nom))::integer AS obs_nb
    FROM synthese_zh
        LEFT JOIN taxonomie.taxref taxref ON synthese_zh.cd_nom = taxref.cd_nom
        LEFT JOIN bdc_statut ON bdc_statut.cd_nom = taxref.cd_nom
    WHERE synthese_zh.id_zh IS NOT NULL AND synthese_zh.date_max > (
               now()::timestamp without time zone - '20 years'::interval) 
            AND taxref.regne::text = 'Plantae'::text AND (bdc_statut.cd_sig::text = 'ETATFRA'::text 
               OR (bdc_statut.cd_sig::text IN ( 
               SELECT DISTINCT 'INSEER'::text || lim.insee_reg::text AS cd_sig
            FROM pr_zh.t_zh tzh
                LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
                LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
                LEFT JOIN ref_geo.li_municipalities lim ON lim.id_area = lareas.id_area
            WHERE tzh.id_zh = synthese_zh.id_zh AND lim.insee_reg IS NOT NULL)) 
               OR (bdc_statut.cd_sig::text IN ( 
               SELECT DISTINCT 'INSEED'::text || lareas.area_code::text AS cd_sig
            FROM pr_zh.t_zh tzh
                LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
                LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
            WHERE tzh.id_zh = synthese_zh.id_zh AND lareas.id_type = (( 
                SELECT bib_areas_types.id_type
                    FROM ref_geo.bib_areas_types
                    WHERE bib_areas_types.type_code::text = 'DEP'::text)) 
            AND lareas.area_code IS NOT NULL)) 
            OR (bdc_statut.statut_type::text = ANY (ARRAY[
               'Liste rouge'::character varying, 'Réglementation'::character varying, 
               'Protection'::character varying, 'Directives européennes'::character varying]::text[])) 
            AND bdc_statut.cd_sig::text = 'TERFXFR'::text)
    GROUP BY taxref.nom_complet, taxref.nom_vern, taxref.classe, synthese_zh.id_zh, taxref.cd_nom, 
        bdc_statut.statut_type, bdc_statut.article, bdc_statut.statut, bdc_statut.doc_url, 
        synthese_zh.date_max, synthese_zh.observers, synthese_zh.organisme;
    """
    )
    # INVERTEBRATES
    # deleting old view
    op.execute("DROP VIEW pr_zh.invertebrates;")
    # creating old view
    op.execute(
        """
    CREATE OR REPLACE VIEW pr_zh.invertebrates
    AS WITH synthese_zh AS (
        SELECT DISTINCT ON (t_zh.id_zh, synthese.cd_nom) synthese.id_synthese,
            t_zh.id_zh,
            synthese.cd_nom,
            synthese.date_max,
            synthese.observers,
		    vu.organisme
		FROM gn_synthese.synthese
        JOIN pr_zh.t_zh ON st_intersects(st_setsrid(t_zh.geom, 4326), synthese.the_geom_point)
		JOIN utilisateurs.v_userslist_forall_applications vu ON ((vu.nom_role::text || ' '::text) || vu.prenom_role::text) = synthese.observers::text
        ORDER BY t_zh.id_zh, synthese.cd_nom, synthese.date_max DESC
        ), bdc_statut AS (
        SELECT bdc_statut_1.cd_nom,
            bdc_statut_1.cd_sig,
            bdc_statut_1.regroupement_type AS statut_type,
            (bdc_statut_1.lb_type_statut::text || ' - '::text) || bdc_statut_1.label_statut::text AS statut,
            bdc_statut_1.full_citation AS article,
            bdc_statut_1.doc_url
        FROM taxonomie.bdc_statut bdc_statut_1
        WHERE bdc_statut_1.regroupement_type::text = 'Liste rouge'::text AND (bdc_statut_1.code_statut::text = ANY (ARRAY['VU'::character varying, 'EN'::character varying, 'CR'::character varying]::text[])) OR (bdc_statut_1.regroupement_type::text = ANY (ARRAY['ZNIEFF'::character varying, 'Réglementation'::character varying, 'Protection'::character varying, 'Directives européennes'::character varying]::text[]))
    )
    SELECT synthese_zh.id_zh,
        taxref.cd_nom,
        taxref.classe AS group_class,
        taxref.ordre AS group_order,
        taxref.nom_complet AS scientific_name,
        taxref.nom_vern AS vernac_name,
        bdc_statut.statut_type,
        bdc_statut.statut,
        bdc_statut.article,
        bdc_statut.doc_url,
        synthese_zh.date_max AS last_date,
        synthese_zh.observers AS observer,
        synthese_zh.organisme,
        (( SELECT count(sy.cd_nom) AS count
            FROM synthese_zh sy
            WHERE sy.id_zh = synthese_zh.id_zh AND sy.cd_nom = taxref.cd_nom))::integer AS obs_nb
    FROM synthese_zh
        LEFT JOIN taxonomie.taxref taxref ON synthese_zh.cd_nom = taxref.cd_nom
        LEFT JOIN bdc_statut ON bdc_statut.cd_nom = taxref.cd_nom
    WHERE synthese_zh.id_zh IS NOT NULL AND synthese_zh.date_max > (now()::timestamp without time zone - '20 years'::interval) AND taxref.phylum::text <> 'Chordata'::text AND taxref.regne::text = 'Animalia'::text AND (bdc_statut.cd_sig::text = 'ETATFRA'::text OR (bdc_statut.cd_sig::text IN ( SELECT DISTINCT 'INSEER'::text || lim.insee_reg::text AS cd_sig
            FROM pr_zh.t_zh tzh
                LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
                LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
                LEFT JOIN ref_geo.li_municipalities lim ON lim.id_area = lareas.id_area
            WHERE tzh.id_zh = synthese_zh.id_zh AND lim.insee_reg IS NOT NULL)) OR (bdc_statut.cd_sig::text IN ( SELECT DISTINCT 'INSEED'::text || lareas.area_code::text AS cd_sig
            FROM pr_zh.t_zh tzh
                LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
                LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
            WHERE tzh.id_zh = synthese_zh.id_zh AND lareas.id_type = (( SELECT bib_areas_types.id_type
                    FROM ref_geo.bib_areas_types
                    WHERE bib_areas_types.type_code::text = 'DEP'::text)) AND lareas.area_code IS NOT NULL)) OR (bdc_statut.statut_type::text = ANY (ARRAY['Liste rouge'::character varying, 'Réglementation'::character varying, 'Protection'::character varying, 'Directives européennes'::character varying]::text[])) AND bdc_statut.cd_sig::text = 'TERFXFR'::text)
    GROUP BY taxref.nom_complet, taxref.nom_vern, taxref.classe, synthese_zh.id_zh, taxref.cd_nom, bdc_statut.statut_type, bdc_statut.article, bdc_statut.statut, bdc_statut.doc_url, synthese_zh.date_max, synthese_zh.observers, synthese_zh.organisme;
    """
    )
    # VERTEBRATES
    # deleting old view
    op.execute("DROP VIEW pr_zh.vertebrates;")
    # creating old view
    op.execute(
        """
    CREATE OR REPLACE VIEW pr_zh.vertebrates
    AS WITH synthese_zh AS (
        SELECT DISTINCT ON (t_zh.id_zh, synthese.cd_nom)
            synthese.id_synthese,
            t_zh.id_zh,
            synthese.cd_nom,
            synthese.date_max,
            synthese.observers,
		    vu.organisme
		FROM gn_synthese.synthese
        JOIN pr_zh.t_zh ON st_intersects(st_setsrid(t_zh.geom, 4326), synthese.the_geom_point)
		JOIN utilisateurs.v_userslist_forall_applications vu ON ((vu.nom_role::text || ' '::text) || vu.prenom_role::text) = synthese.observers::text
        ORDER BY t_zh.id_zh, synthese.cd_nom, synthese.date_max DESC
    ), bdc_statut AS (
        SELECT bdc_statut_1.cd_nom,
            bdc_statut_1.cd_sig,
            bdc_statut_1.regroupement_type AS statut_type,
            (bdc_statut_1.lb_type_statut::text || ' - '::text) || bdc_statut_1.label_statut::text AS statut,
            bdc_statut_1.full_citation AS article,
            bdc_statut_1.doc_url
        FROM taxonomie.bdc_statut bdc_statut_1
        WHERE bdc_statut_1.regroupement_type::text = 'Liste rouge'::text AND (bdc_statut_1.code_statut::text = ANY (ARRAY['VU'::character varying, 'EN'::character varying, 'CR'::character varying]::text[])) OR (bdc_statut_1.regroupement_type::text = ANY (ARRAY['ZNIEFF'::character varying, 'Réglementation'::character varying, 'Protection'::character varying, 'Directives européennes'::character varying]::text[]))
    )
    SELECT synthese_zh.id_zh,
        taxref.cd_nom,
        taxref.classe AS group_class,
        taxref.ordre AS group_order,
        taxref.nom_complet AS scientific_name,
        taxref.nom_vern AS vernac_name,
        bdc_statut.statut_type,
        bdc_statut.statut,
        bdc_statut.article,
        bdc_statut.doc_url,
        synthese_zh.date_max AS last_date,
        synthese_zh.observers AS observer,
        synthese_zh.organisme,
        (( SELECT count(sy.cd_nom) AS count
            FROM synthese_zh sy
            WHERE sy.id_zh = synthese_zh.id_zh AND sy.cd_nom = taxref.cd_nom))::integer AS obs_nb
    FROM synthese_zh
        LEFT JOIN taxonomie.taxref taxref ON synthese_zh.cd_nom = taxref.cd_nom
        LEFT JOIN bdc_statut ON bdc_statut.cd_nom = taxref.cd_nom
    WHERE synthese_zh.id_zh IS NOT NULL AND synthese_zh.date_max > (now()::timestamp without time zone - '20 years'::interval) AND taxref.phylum::text = 'Chordata'::text AND (bdc_statut.cd_sig::text = 'ETATFRA'::text OR (bdc_statut.cd_sig::text IN ( SELECT DISTINCT 'INSEER'::text || lim.insee_reg::text AS cd_sig
            FROM pr_zh.t_zh tzh
                LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
                LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
                LEFT JOIN ref_geo.li_municipalities lim ON lim.id_area = lareas.id_area
            WHERE tzh.id_zh = synthese_zh.id_zh AND lim.insee_reg IS NOT NULL)) OR (bdc_statut.cd_sig::text IN ( SELECT DISTINCT 'INSEED'::text || lareas.area_code::text AS cd_sig
            FROM pr_zh.t_zh tzh
                LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
                LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
            WHERE tzh.id_zh = synthese_zh.id_zh AND lareas.id_type = (( SELECT bib_areas_types.id_type
                    FROM ref_geo.bib_areas_types
                    WHERE bib_areas_types.type_code::text = 'DEP'::text)) AND lareas.area_code IS NOT NULL)) OR (bdc_statut.statut_type::text = ANY (ARRAY['Liste rouge'::character varying, 'Réglementation'::character varying, 'Protection'::character varying, 'Directives européennes'::character varying]::text[])) AND bdc_statut.cd_sig::text = 'TERFXFR'::text)
    GROUP BY taxref.nom_complet, taxref.nom_vern, taxref.classe, synthese_zh.id_zh, taxref.cd_nom, bdc_statut.statut_type, bdc_statut.article, bdc_statut.statut, bdc_statut.doc_url, synthese_zh.date_max, synthese_zh.observers, synthese_zh.organisme;
    """
    )


def downgrade():
    # FLORA
    # deleting new view
    op.execute("DROP VIEW pr_zh.flora;")
    # creating old view
    op.execute(
        """
    CREATE OR REPLACE VIEW pr_zh.flora
    AS WITH synthese_taxa AS (
        SELECT synthese.id_synthese,
            ( SELECT t_zh.id_zh
                FROM pr_zh.t_zh
                WHERE st_intersects(st_setsrid(t_zh.geom, 4326), st_setsrid(synthese.the_geom_point, 4326))) AS id_zh,
            synthese.cd_nom,
            synthese.date_max,
            synthese.observers,
            ( SELECT v_userslist_forall_applications.organisme
                FROM utilisateurs.v_userslist_forall_applications
                WHERE ((v_userslist_forall_applications.nom_role::text || ' '::text) || v_userslist_forall_applications.prenom_role::text) = synthese.observers::text
                LIMIT 1) AS organisme
        FROM gn_synthese.synthese
        ), synthese_zh AS (
        SELECT DISTINCT ON (synthese_taxa.id_zh, synthese_taxa.cd_nom) synthese_taxa.id_synthese,
            synthese_taxa.id_zh,
            synthese_taxa.cd_nom,
            synthese_taxa.date_max,
            synthese_taxa.observers,
            synthese_taxa.organisme
        FROM synthese_taxa
        WHERE synthese_taxa.id_zh IS NOT NULL
        ORDER BY synthese_taxa.id_zh, synthese_taxa.cd_nom, synthese_taxa.date_max DESC
        ), bdc_statut AS (
        SELECT bdc_statut_1.cd_nom,
            bdc_statut_1.cd_sig,
            bdc_statut_1.regroupement_type AS statut_type,
            (bdc_statut_1.lb_type_statut::text || ' - '::text) || bdc_statut_1.label_statut::text AS statut,
            bdc_statut_1.full_citation AS article,
            bdc_statut_1.doc_url
        FROM taxonomie.bdc_statut bdc_statut_1
        WHERE bdc_statut_1.regroupement_type::text = 'Liste rouge'::text AND (bdc_statut_1.code_statut::text = ANY (ARRAY['VU'::character varying, 'EN'::character varying, 'CR'::character varying]::text[])) OR (bdc_statut_1.regroupement_type::text = ANY (ARRAY['ZNIEFF'::character varying, 'Réglementation'::character varying, 'Protection'::character varying, 'Directives européennes'::character varying]::text[]))
    )
    SELECT synthese_zh.id_zh,
        taxref.cd_nom,
        taxref.classe AS group_class,
        taxref.ordre AS group_order,
        taxref.nom_complet AS scientific_name,
        taxref.nom_vern AS vernac_name,
        bdc_statut.statut_type,
        bdc_statut.statut,
        bdc_statut.article,
        bdc_statut.doc_url,
        synthese_zh.date_max AS last_date,
        synthese_zh.observers AS observer,
        synthese_zh.organisme,
        (( SELECT count(synthese_taxa.cd_nom) AS count
            FROM synthese_taxa
            WHERE synthese_taxa.id_zh = synthese_zh.id_zh AND synthese_taxa.cd_nom = taxref.cd_nom))::integer AS obs_nb
    FROM synthese_zh
        LEFT JOIN taxonomie.taxref taxref ON synthese_zh.cd_nom = taxref.cd_nom
        LEFT JOIN bdc_statut ON bdc_statut.cd_nom = taxref.cd_nom
    WHERE synthese_zh.id_zh IS NOT NULL AND synthese_zh.date_max > (now()::timestamp without time zone - '20 years'::interval) AND taxref.regne::text = 'Plantae'::text AND (bdc_statut.cd_sig::text = 'ETATFRA'::text OR (bdc_statut.cd_sig::text IN ( SELECT DISTINCT 'INSEER'::text || lim.insee_reg::text AS cd_sig
            FROM pr_zh.t_zh tzh
                LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
                LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
                LEFT JOIN ref_geo.li_municipalities lim ON lim.id_area = lareas.id_area
            WHERE tzh.id_zh = synthese_zh.id_zh AND lim.insee_reg IS NOT NULL)) OR (bdc_statut.cd_sig::text IN ( SELECT DISTINCT 'INSEED'::text || lareas.area_code::text AS cd_sig
            FROM pr_zh.t_zh tzh
                LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
                LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
            WHERE tzh.id_zh = synthese_zh.id_zh AND lareas.id_type = (( SELECT bib_areas_types.id_type
                    FROM ref_geo.bib_areas_types
                    WHERE bib_areas_types.type_code::text = 'DEP'::text)) AND lareas.area_code IS NOT NULL)) OR (bdc_statut.statut_type::text = ANY (ARRAY['Liste rouge'::character varying, 'Réglementation'::character varying, 'Protection'::character varying, 'Directives européennes'::character varying]::text[])) AND bdc_statut.cd_sig::text = 'TERFXFR'::text)
    GROUP BY taxref.nom_complet, taxref.nom_vern, taxref.classe, synthese_zh.id_zh, taxref.cd_nom, bdc_statut.statut_type, bdc_statut.article, bdc_statut.statut, bdc_statut.doc_url, synthese_zh.date_max, synthese_zh.observers, synthese_zh.organisme;
    """
    )
    # INVERTEBRATES
    # deleting new view
    op.execute("DROP VIEW pr_zh.invertebrates;")
    # creating old view
    op.execute(
        """
    CREATE OR REPLACE VIEW pr_zh.invertebrates
    AS WITH synthese_taxa AS (
        SELECT synthese.id_synthese,
            ( SELECT t_zh.id_zh
                FROM pr_zh.t_zh
                WHERE st_intersects(st_setsrid(t_zh.geom, 4326), st_setsrid(synthese.the_geom_point, 4326))) AS id_zh,
            synthese.cd_nom,
            synthese.date_max,
            synthese.observers,
            ( SELECT v_userslist_forall_applications.organisme
                FROM utilisateurs.v_userslist_forall_applications
                WHERE ((v_userslist_forall_applications.nom_role::text || ' '::text) || v_userslist_forall_applications.prenom_role::text) = synthese.observers::text
                LIMIT 1) AS organisme
        FROM gn_synthese.synthese
        ), synthese_zh AS (
        SELECT DISTINCT ON (synthese_taxa.id_zh, synthese_taxa.cd_nom) synthese_taxa.id_synthese,
            synthese_taxa.id_zh,
            synthese_taxa.cd_nom,
            synthese_taxa.date_max,
            synthese_taxa.observers,
            synthese_taxa.organisme
        FROM synthese_taxa
        WHERE synthese_taxa.id_zh IS NOT NULL
        ORDER BY synthese_taxa.id_zh, synthese_taxa.cd_nom, synthese_taxa.date_max DESC
        ), bdc_statut AS (
        SELECT bdc_statut_1.cd_nom,
            bdc_statut_1.cd_sig,
            bdc_statut_1.regroupement_type AS statut_type,
            (bdc_statut_1.lb_type_statut::text || ' - '::text) || bdc_statut_1.label_statut::text AS statut,
            bdc_statut_1.full_citation AS article,
            bdc_statut_1.doc_url
        FROM taxonomie.bdc_statut bdc_statut_1
        WHERE bdc_statut_1.regroupement_type::text = 'Liste rouge'::text AND (bdc_statut_1.code_statut::text = ANY (ARRAY['VU'::character varying, 'EN'::character varying, 'CR'::character varying]::text[])) OR (bdc_statut_1.regroupement_type::text = ANY (ARRAY['ZNIEFF'::character varying, 'Réglementation'::character varying, 'Protection'::character varying, 'Directives européennes'::character varying]::text[]))
    )
    SELECT synthese_zh.id_zh,
        taxref.cd_nom,
        taxref.classe AS group_class,
        taxref.ordre AS group_order,
        taxref.nom_complet AS scientific_name,
        taxref.nom_vern AS vernac_name,
        bdc_statut.statut_type,
        bdc_statut.statut,
        bdc_statut.article,
        bdc_statut.doc_url,
        synthese_zh.date_max AS last_date,
        synthese_zh.observers AS observer,
        synthese_zh.organisme,
        (( SELECT count(synthese_taxa.cd_nom) AS count
            FROM synthese_taxa
            WHERE synthese_taxa.id_zh = synthese_zh.id_zh AND synthese_taxa.cd_nom = taxref.cd_nom))::integer AS obs_nb
    FROM synthese_zh
        LEFT JOIN taxonomie.taxref taxref ON synthese_zh.cd_nom = taxref.cd_nom
        LEFT JOIN bdc_statut ON bdc_statut.cd_nom = taxref.cd_nom
    WHERE synthese_zh.id_zh IS NOT NULL AND synthese_zh.date_max > (now()::timestamp without time zone - '20 years'::interval) AND taxref.phylum::text <> 'Chordata'::text AND taxref.regne::text = 'Animalia'::text AND (bdc_statut.cd_sig::text = 'ETATFRA'::text OR (bdc_statut.cd_sig::text IN ( SELECT DISTINCT 'INSEER'::text || lim.insee_reg::text AS cd_sig
            FROM pr_zh.t_zh tzh
                LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
                LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
                LEFT JOIN ref_geo.li_municipalities lim ON lim.id_area = lareas.id_area
            WHERE tzh.id_zh = synthese_zh.id_zh AND lim.insee_reg IS NOT NULL)) OR (bdc_statut.cd_sig::text IN ( SELECT DISTINCT 'INSEED'::text || lareas.area_code::text AS cd_sig
            FROM pr_zh.t_zh tzh
                LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
                LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
            WHERE tzh.id_zh = synthese_zh.id_zh AND lareas.id_type = (( SELECT bib_areas_types.id_type
                    FROM ref_geo.bib_areas_types
                    WHERE bib_areas_types.type_code::text = 'DEP'::text)) AND lareas.area_code IS NOT NULL)) OR (bdc_statut.statut_type::text = ANY (ARRAY['Liste rouge'::character varying, 'Réglementation'::character varying, 'Protection'::character varying, 'Directives européennes'::character varying]::text[])) AND bdc_statut.cd_sig::text = 'TERFXFR'::text)
    GROUP BY taxref.nom_complet, taxref.nom_vern, taxref.classe, synthese_zh.id_zh, taxref.cd_nom, bdc_statut.statut_type, bdc_statut.article, bdc_statut.statut, bdc_statut.doc_url, synthese_zh.date_max, synthese_zh.observers, synthese_zh.organisme;
    """
    )
    # VERTEBRATES
    # deleting new view
    op.execute("DROP VIEW pr_zh.vertebrates;")
    # creating old view
    op.execute(
        """
    CREATE OR REPLACE VIEW pr_zh.vertebrates
    AS WITH synthese_taxa AS (
        SELECT synthese.id_synthese,
            ( SELECT t_zh.id_zh
                FROM pr_zh.t_zh
                WHERE st_intersects(st_setsrid(t_zh.geom, 4326), st_setsrid(synthese.the_geom_point, 4326))) AS id_zh,
            synthese.cd_nom,
            synthese.date_max,
            synthese.observers,
            ( SELECT v_userslist_forall_applications.organisme
                FROM utilisateurs.v_userslist_forall_applications
                WHERE ((v_userslist_forall_applications.nom_role::text || ' '::text) || v_userslist_forall_applications.prenom_role::text) = synthese.observers::text
                LIMIT 1) AS organisme
        FROM gn_synthese.synthese
        ), synthese_zh AS (
        SELECT DISTINCT ON (synthese_taxa.id_zh, synthese_taxa.cd_nom) synthese_taxa.id_synthese,
            synthese_taxa.id_zh,
            synthese_taxa.cd_nom,
            synthese_taxa.date_max,
            synthese_taxa.observers,
            synthese_taxa.organisme
        FROM synthese_taxa
        WHERE synthese_taxa.id_zh IS NOT NULL
        ORDER BY synthese_taxa.id_zh, synthese_taxa.cd_nom, synthese_taxa.date_max DESC
        ), bdc_statut AS (
        SELECT bdc_statut_1.cd_nom,
            bdc_statut_1.cd_sig,
            bdc_statut_1.regroupement_type AS statut_type,
            (bdc_statut_1.lb_type_statut::text || ' - '::text) || bdc_statut_1.label_statut::text AS statut,
            bdc_statut_1.full_citation AS article,
            bdc_statut_1.doc_url
        FROM taxonomie.bdc_statut bdc_statut_1
        WHERE bdc_statut_1.regroupement_type::text = 'Liste rouge'::text AND (bdc_statut_1.code_statut::text = ANY (ARRAY['VU'::character varying, 'EN'::character varying, 'CR'::character varying]::text[])) OR (bdc_statut_1.regroupement_type::text = ANY (ARRAY['ZNIEFF'::character varying, 'Réglementation'::character varying, 'Protection'::character varying, 'Directives européennes'::character varying]::text[]))
    )
    SELECT synthese_zh.id_zh,
        taxref.cd_nom,
        taxref.classe AS group_class,
        taxref.ordre AS group_order,
        taxref.nom_complet AS scientific_name,
        taxref.nom_vern AS vernac_name,
        bdc_statut.statut_type,
        bdc_statut.statut,
        bdc_statut.article,
        bdc_statut.doc_url,
        synthese_zh.date_max AS last_date,
        synthese_zh.observers AS observer,
        synthese_zh.organisme,
        (( SELECT count(synthese_taxa.cd_nom) AS count
            FROM synthese_taxa
            WHERE synthese_taxa.id_zh = synthese_zh.id_zh AND synthese_taxa.cd_nom = taxref.cd_nom))::integer AS obs_nb
    FROM synthese_zh
        LEFT JOIN taxonomie.taxref taxref ON synthese_zh.cd_nom = taxref.cd_nom
        LEFT JOIN bdc_statut ON bdc_statut.cd_nom = taxref.cd_nom
    WHERE synthese_zh.id_zh IS NOT NULL AND synthese_zh.date_max > (now()::timestamp without time zone - '20 years'::interval) AND taxref.phylum::text = 'Chordata'::text AND (bdc_statut.cd_sig::text = 'ETATFRA'::text OR (bdc_statut.cd_sig::text IN ( SELECT DISTINCT 'INSEER'::text || lim.insee_reg::text AS cd_sig
            FROM pr_zh.t_zh tzh
                LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
                LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
                LEFT JOIN ref_geo.li_municipalities lim ON lim.id_area = lareas.id_area
            WHERE tzh.id_zh = synthese_zh.id_zh AND lim.insee_reg IS NOT NULL)) OR (bdc_statut.cd_sig::text IN ( SELECT DISTINCT 'INSEED'::text || lareas.area_code::text AS cd_sig
            FROM pr_zh.t_zh tzh
                LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
                LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
            WHERE tzh.id_zh = synthese_zh.id_zh AND lareas.id_type = (( SELECT bib_areas_types.id_type
                    FROM ref_geo.bib_areas_types
                    WHERE bib_areas_types.type_code::text = 'DEP'::text)) AND lareas.area_code IS NOT NULL)) OR (bdc_statut.statut_type::text = ANY (ARRAY['Liste rouge'::character varying, 'Réglementation'::character varying, 'Protection'::character varying, 'Directives européennes'::character varying]::text[])) AND bdc_statut.cd_sig::text = 'TERFXFR'::text)
    GROUP BY taxref.nom_complet, taxref.nom_vern, taxref.classe, synthese_zh.id_zh, taxref.cd_nom, bdc_statut.statut_type, bdc_statut.article, bdc_statut.statut, bdc_statut.doc_url, synthese_zh.date_max, synthese_zh.observers, synthese_zh.organisme;
    """
    )
