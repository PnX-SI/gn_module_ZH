BEGIN;

INSERT INTO gn_commons.bib_tables_location(table_desc, schema_name, table_name, pk_field, uuid_field_name) VALUES
    ('Liste des zones humides','pr_zh','t_zh', 'id_zh', 'zh_uuid')
;

COMMIT;
