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


CREATE MATERIALIZED VIEW pr_zh.atlas_app AS
SELECT
	tzh.id_zh AS id,
	tzh.main_name AS nom,
	(select pr_zh.slugify(tzh.main_name)) AS slug,
	tzh.code AS code,
	tzh.create_date AS date,
	tzh.geom AS polygon_4326,
	(select st_area(st_transform(st_setsrid(tzh.geom,4326), 2154))) AS superficie,
	(select prenom_role || ' ' || nom_role from utilisateurs.t_roles where id_role=tzh.create_author) AS operateur,
	(select cd_nomenclature from ref_nomenclatures.t_nomenclatures where id_nomenclature=tzh.id_sdage) AS type_code,
	(select mnemonique from ref_nomenclatures.t_nomenclatures where id_nomenclature=tzh.id_sdage) AS type,
	(select mnemonique from ref_nomenclatures.t_nomenclatures where id_nomenclature=tzh.id_thread) AS menaces,
	(select mnemonique from ref_nomenclatures.t_nomenclatures where id_nomenclature=tzh.id_diag_bio) AS diagnostic_bio,
	(select mnemonique from ref_nomenclatures.t_nomenclatures where id_nomenclature=tzh.id_diag_hydro) AS diagnostic_hydro,
	(select array_agg(distinct(tn.mnemonique))) AS criteres_delim,
	(select array_agg(distinct(la.area_name))) AS communes,
	(select array_agg(distinct(trb.name))) AS bassin_versant,
	(select coalesce(json_agg(t) ,'[]')
		from (
			select 
				title_fr as label, 
				media_path as url
			from gn_commons.t_medias
			where uuid_attached_row=tzh.zh_uuid
		) t
	) as images
FROM pr_zh.t_zh tzh
LEFT JOIN pr_zh.cor_lim_list cll on tzh.id_lim_list = cll.id_lim_list
LEFT JOIN ref_nomenclatures.t_nomenclatures tn on cll.id_lim = tn.id_nomenclature
LEFT JOIN pr_zh.cor_zh_area cza on tzh.id_zh = cza.id_zh
LEFT JOIN ref_geo.l_areas la on cza.id_area = la.id_area
LEFT JOIN pr_zh.cor_zh_rb czr on tzh.id_zh = czr.id_zh
LEFT JOIN pr_zh.t_river_basin trb on czr.id_rb = trb.id_rb
LEFT JOIN gn_commons.t_medias med on med.uuid_attached_row = tzh.zh_uuid
WHERE cza.cover NOTNULL
GROUP BY tzh.id_zh
ORDER BY tzh.id_zh ASC;


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
