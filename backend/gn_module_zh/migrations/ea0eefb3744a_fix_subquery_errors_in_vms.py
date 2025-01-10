"""fix subquery errors in vms

Revision ID: ea0eefb3744a
Revises: 0052c9eef174
Create Date: 2025-01-10 12:38:26.857124

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ea0eefb3744a"
down_revision = "0052c9eef174"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        DROP MATERIALIZED VIEW pr_zh.vm_vertebrates;
        DROP MATERIALIZED VIEW pr_zh.vm_invertebrates;
        DROP MATERIALIZED VIEW pr_zh.vm_flora;
        
        CREATE MATERIALIZED VIEW pr_zh.vm_vertebrates AS
	    WITH 
		t_id_zh AS (
                SELECT synthese.id_synthese, t_zh.id_zh
				FROM pr_zh.t_zh, gn_synthese.synthese
				WHERE st_intersects(st_setsrid(t_zh.geom, 4326), st_setsrid(synthese.the_geom_point, 4326))
				ORDER BY id_zh
        ),
		synthese_taxa AS (
            SELECT 
                synthese.id_synthese,
				t_id_zh.id_zh,
                synthese.cd_nom,
                synthese.date_max,
                synthese.observers,
                (	
                    SELECT organisme 
                    FROM utilisateurs.v_userslist_forall_applications 
                    WHERE nom_role || ' ' || prenom_role = synthese.observers limit 1
                )
            FROM gn_synthese.synthese
            JOIN t_id_zh ON t_id_zh.id_synthese = synthese.id_synthese     
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

        CREATE MATERIALIZED VIEW pr_zh.vm_invertebrates AS
            WITH 
                t_id_zh AS (
                    SELECT synthese.id_synthese, t_zh.id_zh
                    FROM pr_zh.t_zh, gn_synthese.synthese
                    WHERE st_intersects(st_setsrid(t_zh.geom, 4326), st_setsrid(synthese.the_geom_point, 4326))
                    ORDER BY id_zh
                ),
		        synthese_taxa AS (
                    SELECT 
                        synthese.id_synthese,
                        t_id_zh.id_zh,
                        synthese.cd_nom,
                        synthese.date_max,
                        synthese.observers,
                        (	
                            SELECT organisme 
                            FROM utilisateurs.v_userslist_forall_applications 
                            WHERE nom_role || ' ' || prenom_role = synthese.observers limit 1
                        )
                    FROM gn_synthese.synthese
                    JOIN t_id_zh ON t_id_zh.id_synthese = synthese.id_synthese     
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
            
        CREATE MATERIALIZED VIEW pr_zh.vm_flora AS
            WITH 
                t_id_zh AS (
                        SELECT synthese.id_synthese, t_zh.id_zh
                        FROM pr_zh.t_zh, gn_synthese.synthese
                        WHERE st_intersects(st_setsrid(t_zh.geom, 4326), st_setsrid(synthese.the_geom_point, 4326))
                        ORDER BY id_zh
                ),
                synthese_taxa AS (
                    SELECT 
                        synthese.id_synthese,
                        t_id_zh.id_zh,
                        synthese.cd_nom,
                        synthese.date_max,
                        synthese.observers,
                        (	
                            SELECT organisme 
                            FROM utilisateurs.v_userslist_forall_applications 
                            WHERE nom_role || ' ' || prenom_role = synthese.observers limit 1
                        )
                    FROM gn_synthese.synthese
                    JOIN t_id_zh ON t_id_zh.id_synthese = synthese.id_synthese     
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
        """
    )


def downgrade():
    op.execute(
        """
        DROP MATERIALIZED VIEW pr_zh.vm_vertebrates;
        DROP MATERIALIZED VIEW pr_zh.vm_invertebrates;
        DROP MATERIALIZED VIEW pr_zh.vm_flora;

        CREATE MATERIALIZED VIEW pr_zh.vm_vertebrates AS
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

        CREATE MATERIALIZED VIEW pr_zh.vm_invertebrates AS
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
            
        CREATE MATERIALIZED VIEW pr_zh.vm_flora AS
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
        """
    )
