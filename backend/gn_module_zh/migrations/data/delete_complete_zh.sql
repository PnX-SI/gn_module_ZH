BEGIN;

-- Remove complete sample ZH data

DELETE FROM pr_zh.cor_zh_doc_range
WHERE id_doc = '00000000-0000-0000-0000-000000000903';

DELETE FROM pr_zh.t_urban_planning_docs
WHERE id_doc = '00000000-0000-0000-0000-000000000903';

DELETE FROM pr_zh.cor_impact_list
WHERE id_impact_list = '00000000-0000-0000-0000-000000000902';

DELETE FROM pr_zh.t_activity
WHERE id_impact_list = '00000000-0000-0000-0000-000000000902'
  AND id_zh = 9000001;

DELETE FROM pr_zh.t_actions WHERE id_zh = 9000001;
DELETE FROM pr_zh.t_instruments WHERE id_zh = 9000001;
DELETE FROM pr_zh.t_management_plans
WHERE id_structure IN (SELECT id_structure FROM pr_zh.t_management_structures WHERE id_zh = 9000001);
DELETE FROM pr_zh.t_management_structures WHERE id_zh = 9000001;
DELETE FROM pr_zh.t_ownership WHERE id_zh = 9000001;
DELETE FROM pr_zh.t_hab_heritage WHERE id_zh = 9000001;
DELETE FROM pr_zh.t_functions WHERE id_zh = 9000001;
DELETE FROM pr_zh.t_inflow WHERE id_zh = 9000001;
DELETE FROM pr_zh.t_outflow WHERE id_zh = 9000001;
DELETE FROM pr_zh.cor_zh_protection WHERE id_zh = 9000001;
DELETE FROM pr_zh.cor_zh_ref WHERE id_zh = 9000001;
DELETE FROM pr_zh.cor_zh_rb WHERE id_zh = 9000001;
DELETE FROM pr_zh.cor_zh_hydro WHERE id_zh = 9000001;
DELETE FROM pr_zh.cor_zh_area WHERE id_zh = 9000001;
DELETE FROM pr_zh.cor_zh_corine_cover WHERE id_zh = 9000001;
DELETE FROM pr_zh.cor_zh_cb WHERE id_zh = 9000001;
DELETE FROM pr_zh.cor_zh_lim_fs WHERE id_zh = 9000001;
DELETE FROM pr_zh.cor_lim_list WHERE id_lim_list = '00000000-0000-0000-0000-000000000901';
DELETE FROM pr_zh.t_zh WHERE id_zh = 9000001;
DELETE FROM gn_commons.t_medias
WHERE unique_id_media = '00000000-0000-0000-0000-000000000901'
  AND media_path = 'backend/media/attachments/sample_zh.jpg';

COMMIT;
