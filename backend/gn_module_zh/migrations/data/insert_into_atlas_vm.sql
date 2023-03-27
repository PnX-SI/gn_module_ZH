CREATE EXTENSION IF NOT EXISTS "unaccent";

CREATE OR REPLACE FUNCTION pr_zh.slugify("value" TEXT)
RETURNS TEXT AS $$
  -- removes accents (diacritic signs) from a given string --
  WITH "unaccented" AS (
    SELECT unaccent("value") AS "value"
  ),
  -- lowercases the string
  "lowercase" AS (
    SELECT lower("value") AS "value"
    FROM "unaccented"
  ),
  -- replaces anything that's not a letter, number, hyphen('-'), or underscore('_') with a hyphen('-')
  "hyphenated" AS (
    SELECT regexp_replace("value", '[^a-z0-9\\-_]+', '-', 'gi') AS "value"
    FROM "lowercase"
  ),
  -- trims hyphens('-') if they exist on the head or tail of the string
  "trimmed" AS (
    SELECT regexp_replace(regexp_replace("value", '\\-+$', ''), '^\\-', '') AS "value"
    FROM "hyphenated"
  )
  SELECT "value" FROM "trimmed";
$$ LANGUAGE SQL STRICT IMMUTABLE;
-- https://medium.com/broadlume-product/using-postgresql-to-generate-slugs-5ec9dd759e88


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


CREATE OR REPLACE FUNCTION pr_zh.build_geojson()
RETURNS TABLE(qres jsonb)
language plpgsql
AS
$$
BEGIN
   RETURN QUERY
SELECT jsonb_build_object(
    'type',     'FeatureCollection',
    'features', jsonb_agg(features.feature)
)
FROM (
  SELECT jsonb_build_object(
    'type',       'Feature',
    'id',         id,
    'geometry',   ST_AsGeoJSON(polygon_4326)::jsonb,
    'properties', to_jsonb(inputs) - 'id' - 'polygon_4326'
  ) AS feature
FROM (
	SELECT * FROM pr_zh.atlas_app
	) inputs) features;

END;
$$;
