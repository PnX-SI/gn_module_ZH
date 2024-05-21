BEGIN;

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;


DELETE FROM pr_zh.cor_zh_notes WHERE cor_rule_id > 1000000;
DELETE FROM pr_zh.t_items WHERE val_id > 1000000;
DELETE FROM pr_zh.cor_rb_rules WHERE rb_id > 1000000;

DELETE FROM pr_zh.cor_zh_rb WHERE id_rb > 1000000;
DELETE FROM pr_zh.t_river_basin WHERE id_rb > 1000000;
DELETE FROM pr_zh.t_hydro_area WHERE id_hydro > 1000000;

COMMIT;