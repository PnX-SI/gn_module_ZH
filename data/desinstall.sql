BEGIN;

-- delete zh data in geonature database

DELETE FROM gn_commons.t_modules WHERE module_code='ZONES_HUMIDES';

DROP SCHEMA IF EXISTS pr_zh CASCADE;

DELETE FROM gn_commons.t_medias where id_table_location = (SELECT id_table_location FROM gn_commons.bib_tables_location WHERE table_desc = 'Liste des zones humides');

DELETE FROM gn_commons.bib_tables_location WHERE table_desc = 'Liste des zones humides';

DROP TABLE ref_geo.insee_regions;

DELETE FROM ref_nomenclatures.defaults_nomenclatures_value WHERE mnemonique_type IN ('CRIT_DEF_ESP_FCT', 'EVAL_GLOB_MENACES', 'PERMANENCE_ENTREE', 'PERMANENCE_SORTIE', 'SUBMERSION_FREQ', 'SUBMERSION_ETENDUE', 'FONCTIONNALITE_HYDRO', 'FONCTIONNALITE_BIO', 'FONCTIONS_QUALIF', 'FONCTIONS_CONNAISSANCE', 'ETAT_CONSERVATION', 'STATUT_PROPRIETE', 'STATUT_PROTECTION', 'STRAT_GESTION');

DELETE FROM ref_nomenclatures.t_nomenclatures WHERE source IN ('ZONES_HUMIDES', 'BASSINS_VERSANTS');

DELETE FROM ref_nomenclatures.bib_nomenclatures_types WHERE source IN ('ZONES_HUMIDES', 'BASSINS_VERSANTS');

-- update ref_nomenclatures table sequences :
-- SELECT SETVAL('ref_nomenclatures."bib_nomenclatures_types_id_type_seq"', (SELECT MAX(id_type) FROM ref_nomenclatures.bib_nomenclatures_types));
-- SELECT SETVAL('ref_nomenclatures."t_nomenclatures_id_nomenclature_seq"', (SELECT MAX(id_nomenclature) FROM ref_nomenclatures.t_nomenclatures));

COMMIT;
