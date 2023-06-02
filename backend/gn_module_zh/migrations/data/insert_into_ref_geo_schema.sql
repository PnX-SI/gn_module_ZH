BEGIN;

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = ref_geo, public, pg_catalog;


CREATE TABLE IF NOT EXISTS ref_geo.insee_regions (
    insee_reg varchar(2) NOT NULL, 
    region_name varchar(50) NOT NULL,
    CONSTRAINT pk_insee_regions_insee_code PRIMARY KEY ( insee_reg ),
    CONSTRAINT unq_insee_region_name UNIQUE ( region_name ) 
);


INSERT INTO ref_geo.insee_regions(insee_reg,region_name) VALUES
('01','Guadeloupe'),
('02','Martinique'),
('03','Guyane'),
('04','La Réunion'),
('06','Mayotte'),
('11','Île-de-France'),
('24','Centre-Val de Loire'),
('27','Bourgogne-Franche-Comté'),
('28','Normandie'),
('32','Hauts-de-France'),
('44','Grand Est'),
('52','Pays de la Loire'),
('53','Bretagne'),
('75','Nouvelle-Aquitaine'),
('76','Occitanie'),
('84','Auvergne-Rhône-Alpes'),
('93','Provence-Alpes-Côte d''Azur'),
('94','Corse')
ON CONFLICT (insee_reg) DO NOTHING
;


COMMIT;