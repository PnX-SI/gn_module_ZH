"""set SRID

Revision ID: 22b14fc3abe0
Revises: 01cb1aaa2062
Create Date: 2023-04-19 14:58:14.295664

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "22b14fc3abe0"
down_revision = "01cb1aaa2062"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
          UPDATE pr_zh.t_hydro_area
            SET geom = ST_Force2D(ST_MakeValid(geom));
    
          UPDATE pr_zh.t_river_basin
            SET geom = ST_Force2D(ST_MakeValid(geom));

            drop view pr_zh.vertebrates;
            drop view pr_zh.invertebrates;
            drop view pr_zh.flora;
            drop materialized view  pr_zh.atlas_app;
            ALTER TABLE pr_zh.t_zh
            ALTER COLUMN geom TYPE geometry(geometry, 4326)
                USING ST_SetSRID(geom,4326);
            
            ALTER TABLE pr_zh.t_hydro_area
            ALTER COLUMN geom TYPE geometry(geometry, 4326)
                USING ST_SetSRID(geom,4326);
            
            ALTER TABLE pr_zh.t_river_basin
            ALTER COLUMN geom TYPE geometry(geometry, 4326)
                USING ST_SetSRID(geom,4326);
            
            ALTER TABLE pr_zh.t_fct_area
            ALTER COLUMN geom TYPE geometry(geometry, 4326)
                USING ST_SetSRID(geom,4326);

CREATE OR REPLACE VIEW pr_zh.vertebrates AS
	WITH 
		synthese_taxa AS (
			SELECT 
				synthese.id_synthese,
				( 
					SELECT t_zh.id_zh
					FROM pr_zh.t_zh
					WHERE st_intersects(st_setsrid(t_zh.geom, 4326), st_setsrid(synthese.the_geom_point, 4326))
				) AS id_zh,
				synthese.cd_nom,
				synthese.date_max,
				synthese.observers,
				(	
					SELECT organisme 
					FROM utilisateurs.v_userslist_forall_applications 
					WHERE nom_role || ' ' || prenom_role = synthese.observers limit 1
				)
			FROM gn_synthese.synthese
		),
		synthese_zh AS (
				SELECT DISTINCT ON (id_zh, cd_nom) *
				FROM synthese_taxa
				WHERE id_zh IS NOT null
				ORDER BY id_zh, cd_nom, date_max DESC
		),
		bdc_statut AS (
			SELECT 
				cd_nom,
				cd_sig,
				regroupement_type AS statut_type,
				lb_type_statut || ' - ' || label_statut AS statut,
				full_citation AS article,
				doc_url AS doc_url
			FROM taxonomie.bdc_statut
			WHERE (
				regroupement_type = 'Liste rouge'
				AND code_statut IN ('VU', 'EN', 'CR')
			)
			OR (
				regroupement_type IN ('ZNIEFF', 'Réglementation', 'Protection', 'Directives européennes')
			)
		)

		SELECT 
			synthese_zh.id_zh,
			taxref.cd_nom,
			taxref.classe AS group_class,
			taxref.ordre AS group_order,
			taxref.nom_complet AS scientific_name,
			taxref.nom_vern AS vernac_name,
			bdc_statut.statut_type AS statut_type,
			bdc_statut.statut AS statut,
			bdc_statut.article AS article,
			bdc_statut.doc_url AS doc_url,
			synthese_zh.date_max AS last_date,
			synthese_zh.observers AS observer,
			synthese_zh.organisme AS organisme,
			(select count(cd_nom) from synthese_taxa where id_zh = synthese_zh.id_zh and cd_nom = taxref.cd_nom)::integer AS obs_nb
		FROM synthese_zh
		LEFT JOIN taxonomie.taxref taxref ON synthese_zh.cd_nom = taxref.cd_nom
		LEFT JOIN bdc_statut ON bdc_statut.cd_nom = taxref.cd_nom
		WHERE synthese_zh.id_zh IS NOT NULL
		AND (synthese_zh.date_max::timestamp > (NOW()::timestamp - interval '20 years'))
		AND taxref.phylum = 'Chordata'
		AND (
			bdc_statut.cd_sig = 'ETATFRA'
			OR bdc_statut.cd_sig IN
				(
					SELECT 
						DISTINCT('INSEER' || lim.insee_reg) AS cd_sig
					FROM pr_zh.t_zh tzh
					LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
					LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
					LEFT JOIN ref_geo.li_municipalities lim ON lim.id_area = lareas.id_area
					WHERE tzh.id_zh = synthese_zh.id_zh
					AND lim.insee_reg IS NOT NULL
				)
			OR bdc_statut.cd_sig IN 
				(
					SELECT 
						DISTINCT('INSEED' || lareas.area_code) AS cd_sig
					FROM pr_zh.t_zh tzh
					LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
					LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
					WHERE tzh.id_zh = synthese_zh.id_zh
					AND id_type = (SELECT id_type FROM ref_geo.bib_areas_types WHERE type_code = 'DEP')
					AND lareas.area_code IS NOT NULL
			)
			OR (bdc_statut.statut_type in ('Liste rouge', 'Réglementation', 'Protection', 'Directives européennes') and bdc_statut.cd_sig = 'TERFXFR')
		)
		GROUP BY taxref.nom_complet, taxref.nom_vern, taxref.classe, synthese_zh.id_zh, taxref.cd_nom, bdc_statut.statut_type, bdc_statut.article, bdc_statut.statut, bdc_statut.doc_url, synthese_zh.date_max, synthese_zh.observers, synthese_zh.organisme;

CREATE OR REPLACE VIEW pr_zh.invertebrates AS
	WITH 
		synthese_taxa AS (
			SELECT 
				synthese.id_synthese,
				( 
					SELECT t_zh.id_zh
					FROM pr_zh.t_zh
					WHERE st_intersects(st_setsrid(t_zh.geom, 4326), st_setsrid(synthese.the_geom_point, 4326))
				) AS id_zh,
				synthese.cd_nom,
				synthese.date_max,
				synthese.observers,
				(	
					SELECT organisme 
					FROM utilisateurs.v_userslist_forall_applications 
					WHERE nom_role || ' ' || prenom_role = synthese.observers limit 1
				)
			FROM gn_synthese.synthese
		),
		synthese_zh AS (
				SELECT DISTINCT ON (id_zh, cd_nom) *
				FROM synthese_taxa
				WHERE id_zh IS NOT null
				ORDER BY id_zh, cd_nom, date_max DESC
		),
		bdc_statut AS (
			SELECT 
				cd_nom,
				cd_sig,
				regroupement_type AS statut_type,
				lb_type_statut || ' - ' || label_statut AS statut,
				full_citation AS article,
				doc_url AS doc_url
			FROM taxonomie.bdc_statut
			WHERE (
				regroupement_type = 'Liste rouge'
				AND code_statut IN ('VU', 'EN', 'CR')
			)
			OR (
				regroupement_type IN ('ZNIEFF', 'Réglementation', 'Protection', 'Directives européennes')
			)
		)

		SELECT 
			synthese_zh.id_zh,
			taxref.cd_nom,
			taxref.classe AS group_class,
			taxref.ordre AS group_order,
			taxref.nom_complet AS scientific_name,
			taxref.nom_vern AS vernac_name,
			bdc_statut.statut_type AS statut_type,
			bdc_statut.statut AS statut,
			bdc_statut.article AS article,
			bdc_statut.doc_url AS doc_url,
			synthese_zh.date_max AS last_date,
			synthese_zh.observers AS observer,
			synthese_zh.organisme AS organisme,
			(select count(cd_nom) from synthese_taxa where id_zh = synthese_zh.id_zh and cd_nom = taxref.cd_nom)::integer AS obs_nb
		FROM synthese_zh
		LEFT JOIN taxonomie.taxref taxref ON synthese_zh.cd_nom = taxref.cd_nom
		LEFT JOIN bdc_statut ON bdc_statut.cd_nom = taxref.cd_nom
		WHERE synthese_zh.id_zh IS NOT NULL
		AND (synthese_zh.date_max::timestamp > (NOW()::timestamp - interval '20 years'))
		AND taxref.phylum != 'Chordata'
		AND taxref.regne = 'Animalia'
		AND (
			bdc_statut.cd_sig = 'ETATFRA'
			OR bdc_statut.cd_sig IN
				(
					SELECT 
						DISTINCT('INSEER' || lim.insee_reg) AS cd_sig
					FROM pr_zh.t_zh tzh
					LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
					LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
					LEFT JOIN ref_geo.li_municipalities lim ON lim.id_area = lareas.id_area
					WHERE tzh.id_zh = synthese_zh.id_zh
					AND lim.insee_reg IS NOT NULL
				)
			OR bdc_statut.cd_sig IN 
				(
					SELECT 
						DISTINCT('INSEED' || lareas.area_code) AS cd_sig
					FROM pr_zh.t_zh tzh
					LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
					LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
					WHERE tzh.id_zh = synthese_zh.id_zh
					AND id_type = (SELECT id_type FROM ref_geo.bib_areas_types WHERE type_code = 'DEP')
					AND lareas.area_code IS NOT NULL
			)
			OR (bdc_statut.statut_type in ('Liste rouge', 'Réglementation', 'Protection', 'Directives européennes') and bdc_statut.cd_sig = 'TERFXFR')
		)
		GROUP BY taxref.nom_complet, taxref.nom_vern, taxref.classe, synthese_zh.id_zh, taxref.cd_nom, bdc_statut.statut_type, bdc_statut.article, bdc_statut.statut, bdc_statut.doc_url, synthese_zh.date_max, synthese_zh.observers, synthese_zh.organisme;
	 
        
        	
CREATE OR REPLACE VIEW pr_zh.flora AS
	WITH 
		synthese_taxa AS (
			SELECT 
				synthese.id_synthese,
				( 
					SELECT t_zh.id_zh
					FROM pr_zh.t_zh
					WHERE st_intersects(st_setsrid(t_zh.geom, 4326), st_setsrid(synthese.the_geom_point, 4326))
				) AS id_zh,
				synthese.cd_nom,
				synthese.date_max,
				synthese.observers,
				(	
					SELECT organisme 
					FROM utilisateurs.v_userslist_forall_applications 
					WHERE nom_role || ' ' || prenom_role = synthese.observers limit 1
				)
			FROM gn_synthese.synthese
		),
		synthese_zh AS (
				SELECT DISTINCT ON (id_zh, cd_nom) *
				FROM synthese_taxa
				WHERE id_zh IS NOT null
				ORDER BY id_zh, cd_nom, date_max DESC
		),
		bdc_statut AS (
			SELECT 
				cd_nom,
				cd_sig,
				regroupement_type AS statut_type,
				lb_type_statut || ' - ' || label_statut AS statut,
				full_citation AS article,
				doc_url AS doc_url
			FROM taxonomie.bdc_statut
			WHERE (
				regroupement_type = 'Liste rouge'
				AND code_statut IN ('VU', 'EN', 'CR')
			)
			OR (
				regroupement_type IN ('ZNIEFF', 'Réglementation', 'Protection', 'Directives européennes')
			)
		)

		SELECT 
			synthese_zh.id_zh,
			taxref.cd_nom,
			taxref.classe AS group_class,
			taxref.ordre AS group_order,
			taxref.nom_complet AS scientific_name,
			taxref.nom_vern AS vernac_name,
			bdc_statut.statut_type AS statut_type,
			bdc_statut.statut AS statut,
			bdc_statut.article AS article,
			bdc_statut.doc_url AS doc_url,
			synthese_zh.date_max AS last_date,
			synthese_zh.observers AS observer,
			synthese_zh.organisme AS organisme,
			(select count(cd_nom) from synthese_taxa where id_zh = synthese_zh.id_zh and cd_nom = taxref.cd_nom)::integer AS obs_nb
		FROM synthese_zh
		LEFT JOIN taxonomie.taxref taxref ON synthese_zh.cd_nom = taxref.cd_nom
		LEFT JOIN bdc_statut ON bdc_statut.cd_nom = taxref.cd_nom
		WHERE synthese_zh.id_zh IS NOT NULL
		AND (synthese_zh.date_max::timestamp > (NOW()::timestamp - interval '20 years'))
		AND taxref.regne = 'Plantae'
		AND (
			bdc_statut.cd_sig = 'ETATFRA'
			OR bdc_statut.cd_sig IN
				(
					SELECT 
						DISTINCT('INSEER' || lim.insee_reg) AS cd_sig
					FROM pr_zh.t_zh tzh
					LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
					LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
					LEFT JOIN ref_geo.li_municipalities lim ON lim.id_area = lareas.id_area
					WHERE tzh.id_zh = synthese_zh.id_zh
					AND lim.insee_reg IS NOT NULL
				)
			OR bdc_statut.cd_sig IN 
				(
					SELECT 
						DISTINCT('INSEED' || lareas.area_code) AS cd_sig
					FROM pr_zh.t_zh tzh
					LEFT JOIN pr_zh.cor_zh_area cza ON cza.id_zh = tzh.id_zh
					LEFT JOIN ref_geo.l_areas lareas ON cza.id_area = lareas.id_area
					WHERE tzh.id_zh = synthese_zh.id_zh
					AND id_type = (SELECT id_type FROM ref_geo.bib_areas_types WHERE type_code = 'DEP')
					AND lareas.area_code IS NOT NULL
			)
			OR (bdc_statut.statut_type in ('Liste rouge', 'Réglementation', 'Protection', 'Directives européennes') and bdc_statut.cd_sig = 'TERFXFR')
		)
		GROUP BY taxref.nom_complet, taxref.nom_vern, taxref.classe, synthese_zh.id_zh, taxref.cd_nom, bdc_statut.statut_type, bdc_statut.article, bdc_statut.statut, bdc_statut.doc_url, synthese_zh.date_max, synthese_zh.observers, synthese_zh.organisme;


        CREATE MATERIALIZED VIEW pr_zh.atlas_app
        TABLESPACE pg_default
        AS SELECT tzh.id_zh AS id,
            tzh.main_name AS nom,
            ( SELECT pr_zh.slugify(tzh.main_name::text) AS slugify) AS slug,
            tzh.code,
            tzh.create_date AS date,
            tzh.geom AS polygon_4326,
            ( SELECT st_area(st_transform(st_setsrid(tzh.geom, 4326), 2154)) AS st_area) AS superficie,
            bo.nom_organisme AS operateur,
            ( SELECT t_nomenclatures.cd_nomenclature
                FROM ref_nomenclatures.t_nomenclatures
                WHERE t_nomenclatures.id_nomenclature = tzh.id_sdage) AS type_code,
            ( SELECT t_nomenclatures.mnemonique
                FROM ref_nomenclatures.t_nomenclatures
                WHERE t_nomenclatures.id_nomenclature = tzh.id_sdage) AS type,
            ( SELECT t_nomenclatures.mnemonique
                FROM ref_nomenclatures.t_nomenclatures
                WHERE t_nomenclatures.id_nomenclature = tzh.id_thread) AS menaces,
            ( SELECT t_nomenclatures.mnemonique
                FROM ref_nomenclatures.t_nomenclatures
                WHERE t_nomenclatures.id_nomenclature = tzh.id_diag_bio) AS diagnostic_bio,
            ( SELECT t_nomenclatures.mnemonique
                FROM ref_nomenclatures.t_nomenclatures
                WHERE t_nomenclatures.id_nomenclature = tzh.id_diag_hydro) AS diagnostic_hydro,
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
            LEFT JOIN ref_geo.bib_areas_types bat ON la.id_type = bat.id_type
            LEFT JOIN pr_zh.cor_zh_rb czr ON tzh.id_zh = czr.id_zh
            LEFT JOIN pr_zh.t_river_basin trb ON czr.id_rb = trb.id_rb
            LEFT JOIN gn_commons.t_medias med ON med.uuid_attached_row = tzh.zh_uuid
            LEFT JOIN utilisateurs.t_roles tr ON tr.id_role = tzh.create_author
            LEFT JOIN utilisateurs.bib_organismes bo ON bo.id_organisme = tr.id_organisme
        WHERE cza.cover IS NOT NULL
        GROUP BY tzh.id_zh, bo.nom_organisme
        ORDER BY tzh.id_zh
        WITH DATA;

                
        """
    )


def downgrade():
    pass
