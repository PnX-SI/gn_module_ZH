#!/bin/bash

db_name="geonature2db"
host="localhost"
db_user="geonatadmin"
db_port="5432"

# view names (without schema name)
flora_view_name="flora_new"
vertebrate_view_name="vertebrate_new"
invertebrate_view_name="invertebrate_new"

# taxon source
taxon_shema_source="gn_synthese"
taxon_table_source="synthese"

# protection/reglementation source
# taxon_info_table="taxonomie.taxref_bdc_statut"
taxon_info_table="taxonomie.bdc_statut"

# create views :
declare -a ViewArray=(${flora_view_name} ${vertebrate_view_name} ${invertebrate_view_name})

# Iterate the string array using for loop
for val in ${ViewArray[@]}; do
    if [ "${val}" = "${flora_view_name}" ]
    then
        branch="taxref.regne = 'Plantae'"
    elif [ "${val}" = "${vertebrate_view_name}" ]
    then
        branch="taxref.phylum = 'Chordata'"
    else
        branch="taxref.phylum != 'Chordata' AND taxref.regne = 'Animalia'"
    fi
    query=("
        CREATE MATERIALIZED VIEW pr_zh.vm_$val AS
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
                    FROM ${taxon_shema_source}.${taxon_table_source}
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
                    FROM ${taxon_info_table}
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
                AND ${branch}
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
            ")
    sudo -u "postgres" -s psql -d ${db_name} -h ${host} -U ${db_user} -p ${db_port} -c "${query}"
    done
