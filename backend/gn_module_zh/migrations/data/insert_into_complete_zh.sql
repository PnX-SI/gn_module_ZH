BEGIN;

-- ZH complete sample data for PDF

-- Main picture (placeholder file; base64 filled in migration resources)
INSERT INTO gn_commons.t_medias (
    unique_id_media,
    id_nomenclature_media_type,
    id_table_location,
    uuid_attached_row,
    title_fr,
    media_path,
    author,
    description_fr,
    is_public
) VALUES (
    '00000000-0000-0000-0000-000000000901',
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'TYPE_MEDIA')
          AND cd_nomenclature = '2'
        ORDER BY id_nomenclature LIMIT 1),
    (SELECT id_table_location FROM gn_commons.bib_tables_location
        WHERE table_desc = 'Liste des zones humides' LIMIT 1),
    '00000000-0000-0000-0000-000000000901',
    'Photo ZH exemple',
    'backend/media/attachments/sample_zh.jpg',
    'Administrateur',
    'Image d''exemple (base64 à compléter)',
    true
);

INSERT INTO pr_zh.t_zh (
    id_zh,
    zh_uuid,
    code,
    main_name,
    secondary_name,
    is_id_site_space,
    id_site_space,
    create_author,
    update_author,
    id_org,
    create_date,
    update_date,
    geom,
    id_lim_list,
    remark_lim,
    remark_lim_fs,
    id_sdage,
    id_sage,
    remark_pres,
    v_habref,
    ef_area,
    global_remark_activity,
    id_thread,
    id_frequency,
    id_spread,
    id_connexion,
    id_diag_hydro,
    id_diag_bio,
    id_strat_gestion,
    remark_diag,
    is_other_inventory,
    is_carto_hab,
    nb_hab,
    total_hab_cover,
    nb_flora_sp,
    nb_vertebrate_sp,
    nb_invertebrate_sp,
    remark_eval_functions,
    remark_eval_heritage,
    remark_eval_thread,
    remark_eval_actions,
    remark_is_other_inventory,
    main_pict_id,
    area
) VALUES (
    9000001,
    '00000000-0000-0000-0000-000000000901',
    'ZH-SAMPLE01',
    'Zone humide exemple complete',
    'ZH exemple secondaire',
    false,
    (SELECT id_site_space FROM pr_zh.bib_site_space ORDER BY id_site_space LIMIT 1),
    (SELECT id_role FROM utilisateurs.t_roles WHERE nom_role = 'Administrateur' LIMIT 1),
    (SELECT id_role FROM utilisateurs.t_roles WHERE nom_role = 'Administrateur' LIMIT 1),
    (SELECT id_org FROM pr_zh.bib_organismes ORDER BY id_org LIMIT 1),
    NOW(),
    NOW(),
    ST_SetSRID(ST_GeomFromText('POLYGON((5.39591 43.875472, 5.39631 43.875472, 5.39631 43.875872, 5.39591 43.875872, 5.39591 43.875472))'), 4326),
    '00000000-0000-0000-0000-000000000901',
    'Limite basee sur observations de terrain',
    'Limite espace fonctionnel basee sur imagerie',
    ref_nomenclatures.get_id_nomenclature('SDAGE','1'),
    ref_nomenclatures.get_id_nomenclature('SAGE','6'),
    'Remarques sur la presentation des milieux',
    NULL,
    12.34,
    'Remarque globale sur les activites',
    ref_nomenclatures.get_default_nomenclature_value('EVAL_GLOB_MENACES'),
    ref_nomenclatures.get_default_nomenclature_value('SUBMERSION_FREQ'),
    ref_nomenclatures.get_default_nomenclature_value('SUBMERSION_ETENDUE'),
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'TYPE_CONNEXION')
        ORDER BY id_nomenclature LIMIT 1),
    ref_nomenclatures.get_default_nomenclature_value('FONCTIONNALITE_HYDRO'),
    ref_nomenclatures.get_default_nomenclature_value('FONCTIONNALITE_BIO'),
    ref_nomenclatures.get_default_nomenclature_value('STRAT_GESTION'),
    'Remarque sur le diagnostic fonctionnel',
    true,
    true,
    8,
    70,
    25,
    18,
    12,
    'Remarque evaluation des fonctions',
    'Remarque evaluation du patrimoine',
    'Remarque evaluation des menaces',
    'Remarque evaluation des actions',
    'Autres inventaires : inventaire local 2024',
    NULL,
    45.67
);

-- Link main picture to ZH
UPDATE pr_zh.t_zh
SET main_pict_id = (
    SELECT id_media FROM gn_commons.t_medias
    WHERE unique_id_media = '00000000-0000-0000-0000-000000000901'
    ORDER BY id_media DESC
    LIMIT 1
)
WHERE id_zh = 9000001;

-- Delimitation criteria
INSERT INTO pr_zh.cor_lim_list (id_lim_list, id_lim)
SELECT '00000000-0000-0000-0000-000000000901', id_nomenclature
FROM ref_nomenclatures.t_nomenclatures
WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'CRIT_DELIM')
ORDER BY id_nomenclature
LIMIT 2;

INSERT INTO pr_zh.cor_zh_lim_fs (id_zh, id_lim_fs)
SELECT 9000001, id_nomenclature
FROM ref_nomenclatures.t_nomenclatures
WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'CRIT_DEF_ESP_FCT')
ORDER BY id_nomenclature
LIMIT 2;

-- Corine biotopes and landcovers
INSERT INTO pr_zh.cor_zh_cb (id_zh, lb_code)
SELECT 9000001, lb_code
FROM pr_zh.bib_cb
ORDER BY lb_code
LIMIT 2;

INSERT INTO pr_zh.cor_zh_corine_cover (id_cover, id_zh)
SELECT id_nomenclature, 9000001
FROM ref_nomenclatures.t_nomenclatures
WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'OCCUPATION_SOLS')
ORDER BY id_nomenclature
LIMIT 2;

-- Geo areas (department + commune)
INSERT INTO pr_zh.cor_zh_area (id_area, id_zh, cover)
SELECT id_area, 9000001, 50
FROM ref_geo.l_areas
WHERE id_type = (SELECT id_type FROM ref_geo.bib_areas_types WHERE type_code = 'DEP')
ORDER BY id_area
LIMIT 1;

INSERT INTO pr_zh.cor_zh_area (id_area, id_zh, cover)
SELECT id_area, 9000001, 12
FROM ref_geo.l_areas
WHERE id_type = (SELECT id_type FROM ref_geo.bib_areas_types WHERE type_code = 'COM')
ORDER BY id_area
LIMIT 1;

-- Basin / hydro zones
INSERT INTO pr_zh.cor_zh_rb (id_zh, id_rb)
SELECT 9000001, id_rb
FROM pr_zh.t_river_basin
ORDER BY id_rb
LIMIT 1;

INSERT INTO pr_zh.cor_zh_hydro (id_zh, id_hydro)
SELECT 9000001, id_hydro
FROM pr_zh.t_hydro_area
ORDER BY id_hydro
LIMIT 1;

-- References
INSERT INTO pr_zh.cor_zh_ref (id_ref, id_zh)
SELECT id_reference, 9000001
FROM pr_zh.t_references
ORDER BY id_reference
LIMIT 1;

-- Flows (in/out)
INSERT INTO pr_zh.t_inflow (id_inflow, id_zh, id_permanance, topo)
VALUES (
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'ENTREE_EAU')
        ORDER BY id_nomenclature LIMIT 1),
    9000001,
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'PERMANENCE_ENTREE')
        ORDER BY id_nomenclature LIMIT 1),
    'Ruisseau de la source'
);

INSERT INTO pr_zh.t_outflow (id_outflow, id_zh, id_permanance, topo)
VALUES (
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'SORTIE_EAU')
        ORDER BY id_nomenclature LIMIT 1),
    9000001,
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'PERMANENCE_SORTIE')
        ORDER BY id_nomenclature LIMIT 1),
    'Fosse d''evacuation'
);

-- Activities + impacts
INSERT INTO pr_zh.t_activity (id_activity, id_zh, id_position, id_impact_list, remark_activity)
VALUES (
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'ACTIV_HUM')
        ORDER BY id_nomenclature LIMIT 1),
    9000001,
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'LOCALISATION')
        ORDER BY id_nomenclature LIMIT 1),
    '00000000-0000-0000-0000-000000000902',
    'Activite agricole en bordure'
);

INSERT INTO pr_zh.cor_impact_list (id_impact_list, id_cor_impact_types)
SELECT '00000000-0000-0000-0000-000000000902', id_cor_impact_types
FROM pr_zh.cor_impact_types
ORDER BY id_cor_impact_types
LIMIT 2;

-- Functions (used in PDF and evaluation)
INSERT INTO pr_zh.t_functions (id_function, id_zh, justification, id_qualification, id_knowledge)
VALUES (
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_HYDRO')
        ORDER BY id_nomenclature LIMIT 1),
    9000001,
    'Justification hydrologique',
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')
        AND mnemonique = 'Moyenne'
        ORDER BY id_nomenclature LIMIT 1),
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_CONNAISSANCE')
        ORDER BY id_nomenclature LIMIT 1)
);

INSERT INTO pr_zh.t_functions (id_function, id_zh, justification, id_qualification, id_knowledge)
VALUES (
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_BIO')
        ORDER BY id_nomenclature LIMIT 1),
    9000001,
    'Justification biologique',
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')
        AND mnemonique = 'Moyenne'
        ORDER BY id_nomenclature LIMIT 1),
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_CONNAISSANCE')
        ORDER BY id_nomenclature LIMIT 1)
);

INSERT INTO pr_zh.t_functions (id_function, id_zh, justification, id_qualification, id_knowledge)
VALUES (
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'INTERET_PATRIM')
        ORDER BY id_nomenclature LIMIT 1),
    9000001,
    'Justification patrimoniale',
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')
        AND mnemonique = 'Moyenne'
        ORDER BY id_nomenclature LIMIT 1),
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_CONNAISSANCE')
        ORDER BY id_nomenclature LIMIT 1)
);

INSERT INTO pr_zh.t_functions (id_function, id_zh, justification, id_qualification, id_knowledge)
VALUES (
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'VAL_SOC_ECO')
        ORDER BY id_nomenclature LIMIT 1),
    9000001,
    'Justification socio-economique',
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')
        AND mnemonique = 'Moyenne'
        ORDER BY id_nomenclature LIMIT 1),
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_CONNAISSANCE')
        ORDER BY id_nomenclature LIMIT 1)
);

-- Habitats patrimoniaux (guarded: ref_habitats schema may be missing)
DO $$
BEGIN
  IF to_regclass('ref_habitats.typo_ref') IS NOT NULL
     AND to_regclass('ref_habitats.habref') IS NOT NULL
  THEN
    EXECUTE $sql$
      INSERT INTO pr_zh.t_hab_heritage (id_zh, id_corine_bio, id_cahier_hab, id_preservation_state, hab_cover)
      VALUES (
        9000001,
        (SELECT lb_code FROM ref_habitats.habref
          WHERE cd_typo = (SELECT cd_typo FROM ref_habitats.typo_ref WHERE cd_table = 'TYPO_CORINE_BIOTOPES')
          ORDER BY lb_code LIMIT 1),
        (SELECT cd_hab FROM ref_habitats.habref
          WHERE cd_typo = (SELECT cd_typo FROM ref_habitats.typo_ref WHERE cd_table = 'TYPO_CH')
          ORDER BY cd_hab LIMIT 1),
        ref_nomenclatures.get_default_nomenclature_value('ETAT_CONSERVATION'),
        30
      )
    $sql$;
  END IF;
END $$;

-- Ownership
INSERT INTO pr_zh.t_ownership (id_status, id_zh, remark)
VALUES (
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'STATUT_PROPRIETE')
        ORDER BY id_nomenclature LIMIT 1),
    9000001,
    'Statut foncier mixte'
);

-- Management structures and plans
INSERT INTO pr_zh.t_management_structures (id_zh, id_org)
VALUES (
    9000001,
    (SELECT id_org FROM pr_zh.bib_organismes ORDER BY id_org LIMIT 1)
);

INSERT INTO pr_zh.t_management_plans (id_nature, id_structure, plan_date, duration, remark)
VALUES (
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'PLAN_GESTION')
        ORDER BY id_nomenclature LIMIT 1),
    (SELECT id_structure FROM pr_zh.t_management_structures WHERE id_zh = 9000001 ORDER BY id_structure LIMIT 1),
    NOW(),
    5,
    'Plan de gestion quinquennal'
);

-- Instruments
INSERT INTO pr_zh.t_instruments (id_instrument, id_zh, instrument_date)
VALUES (
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'INSTRU_CONTRAC_FINANC')
        ORDER BY id_nomenclature LIMIT 1),
    9000001,
    NOW()
);

-- Protections
INSERT INTO pr_zh.cor_zh_protection (id_protection, id_zh)
SELECT id_protection, 9000001
FROM pr_zh.cor_protection_level_type
ORDER BY id_protection
LIMIT 1;

-- Urban planning documents
INSERT INTO pr_zh.t_urban_planning_docs (id_area, id_zh, id_doc_type, id_doc, remark)
VALUES (
    (SELECT id_area FROM ref_geo.l_areas
        WHERE id_type = (SELECT id_type FROM ref_geo.bib_areas_types WHERE type_code = 'COM')
        ORDER BY id_area LIMIT 1),
    9000001,
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'TYP_DOC_COMM')
        ORDER BY id_nomenclature LIMIT 1),
    '00000000-0000-0000-0000-000000000903',
    'Zonage du PLU'
);

INSERT INTO pr_zh.cor_zh_doc_range (id_doc, id_cor)
SELECT '00000000-0000-0000-0000-000000000903', id_cor
FROM pr_zh.cor_urban_type_range
ORDER BY id_cor
LIMIT 1;

-- Actions
INSERT INTO pr_zh.t_actions (id_action, id_zh, id_priority_level, remark)
VALUES (
    (SELECT id_action FROM pr_zh.bib_actions ORDER BY id_action LIMIT 1),
    9000001,
    (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'NIVEAU_PRIORITE')
        ORDER BY id_nomenclature LIMIT 1),
    'Action prioritaire de restauration'
);

COMMIT;
