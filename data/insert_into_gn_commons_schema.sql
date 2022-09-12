BEGIN;

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = gn_commons, public, pg_catalog;

INSERT INTO gn_commons.bib_tables_location(table_desc, schema_name, table_name, pk_field, uuid_field_name) VALUES
    ('Liste des zones humides','pr_zh','t_zh', 'id_zh', 'zh_uuid')
;

COMMIT;
