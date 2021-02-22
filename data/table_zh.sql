SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;


CREATE SCHEMA IF NOT EXISTS pr_zh;


--SET search_path = pr_zh, pg_catalog;
SET default_with_oids = false;

CREATE  TABLE pr_zh.bib_site_space ( 
	id_site_space        integer  NOT NULL ,
	name                 varchar(100)  NOT NULL ,
	CONSTRAINT pk_bib_site_space_id_site_space PRIMARY KEY ( id_site_space )
 );

COMMENT ON TABLE pr_zh.bib_site_space IS 'Liste of site space';

COMMENT ON COLUMN pr_zh.bib_site_space.name IS 'site space name';



CREATE SEQUENCE pr_zh.t_zh_id_zh_seq START WITH 1 INCREMENT BY 1;


CREATE  TABLE pr_zh.t_zh ( 
	id_zh                integer DEFAULT nextval('pr_zh.t_zh_id_zh_seq'::regclass) NOT NULL ,
	zh_uuid              uuid,		
	code                 varchar(12)  NOT NULL ,
	main_name            varchar(100)  NOT NULL ,
	secondary_name       varchar(100)   ,
	id_site_space        integer   ,
	create_author        integer  NOT NULL ,
	update_author        integer  NOT NULL ,
	create_date          timestamp(0) DEFAULT CURRENT_TIMESTAMP NOT NULL ,
	update_date          timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL ,
	geom           geometry(Geometry,4326)   ,
	remark_lim           text   ,
	remark_lim_fs        text   ,
	id_sdage             integer ,
	id_local_typo        integer   ,
	remark_pres          text   ,
	v_habref             varchar   ,
	ef_area              integer   ,
	global_remark_activity text   ,
	id_thread            integer   ,
	id_frequency         integer   ,
	id_spread            integer   ,
	id_connexion         integer   ,
	id_diag_hydro        integer DEFAULT 99  ,
	id_diag_bio          integer DEFAULT 99  ,
	remark_diag          text   ,
	other_inventory      boolean   ,
	carto_hab            boolean   ,
	nb_hab               integer   ,
	total_hab_cover      integer   ,
	nb_flora_sp          integer   ,
	nb_vertebrate_sp     integer   ,
	nb_invertebrate_sp   integer   ,
	remark_eval_functions          text   ,
	remark_eval_heritage          text   ,
	remark_eval_thread          text   ,
	reamrk_eval_actions          text   ,
	CONSTRAINT pk_t_zh_zh_id PRIMARY KEY ( id_zh ),
	CONSTRAINT unq_t_zh_code UNIQUE ( code ) ,
	CONSTRAINT unq_t_zh_name UNIQUE ( main_name ) 
 );

COMMENT ON TABLE pr_zh.t_zh IS 'list of zh';

COMMENT ON COLUMN pr_zh.t_zh.id_zh IS 'ZH unique id';

COMMENT ON COLUMN pr_zh.t_zh.code IS '12 caracters unique cod';

COMMENT ON COLUMN pr_zh.t_zh.main_name IS 'Main zh name';

COMMENT ON COLUMN pr_zh.t_zh.secondary_name IS 'Nom secondaire de la zone humide';

COMMENT ON COLUMN pr_zh.t_zh.create_author IS 'Author who created the ZH in the db';

COMMENT ON COLUMN pr_zh.t_zh.update_author IS 'Auteur des dernières modifications';

COMMENT ON COLUMN pr_zh.t_zh.create_date IS 'zh creation date in database';

COMMENT ON COLUMN pr_zh.t_zh.update_date IS 'Date of the last modification';

COMMENT ON COLUMN pr_zh.t_zh.geom IS 'polygone du périmètre de la zone humide';

COMMENT ON COLUMN pr_zh.t_zh.remark_lim IS 'remark about zh limit';

COMMENT ON COLUMN pr_zh.t_zh.remark_lim_fs IS 'remark about limit of fonctionnal space';

COMMENT ON COLUMN pr_zh.t_zh.id_sdage IS 'typologie sdage';

COMMENT ON COLUMN pr_zh.t_zh.id_local_typo IS 'typologie locale';

COMMENT ON COLUMN pr_zh.t_zh.remark_pres IS 'remarque concernant la présentation de la zone humide et de ses milieux';

COMMENT ON COLUMN pr_zh.t_zh.v_habref IS 'version of habref';

COMMENT ON COLUMN pr_zh.t_zh.ef_area IS 'superficie de l''espace fonctionnel (en ha)';

COMMENT ON COLUMN pr_zh.t_zh.id_thread IS 'evolution globale des menaces potentielles ou avancees';

COMMENT ON COLUMN pr_zh.t_zh.id_frequency IS 'Régime hydrique - submersion frequence';

COMMENT ON COLUMN pr_zh.t_zh.id_spread IS 'Regime hydrique - submersion étendue';

COMMENT ON COLUMN pr_zh.t_zh.id_connexion IS 'Connexion de la zone humide dans son environnement';

COMMENT ON COLUMN pr_zh.t_zh.id_diag_hydro IS 'fonctionnalité hydrologique';

COMMENT ON COLUMN pr_zh.t_zh.id_diag_bio IS 'fonctionnalité biologique';

COMMENT ON COLUMN pr_zh.t_zh.remark_diag IS 'Remarque sur diagnostic fonctionnel';

COMMENT ON COLUMN pr_zh.t_zh.other_inventory IS 'Autres études / inventaires naturalistes';

COMMENT ON COLUMN pr_zh.t_zh.carto_hab IS 'cartographie d''habitats';

COMMENT ON COLUMN pr_zh.t_zh.nb_hab IS 'nombre d''habitats';

COMMENT ON COLUMN pr_zh.t_zh.total_hab_cover IS 'recouverment total de la zh en pourcentage';

COMMENT ON COLUMN pr_zh.t_zh.nb_flora_sp IS 'flore - nombre d''especes';

COMMENT ON COLUMN pr_zh.t_zh.nb_vertebrate_sp IS 'faune vertebres - nombre d''especes';

COMMENT ON COLUMN pr_zh.t_zh.nb_invertebrate_sp IS 'faune invvertebres - nombre d''especes';



ALTER TABLE pr_zh.t_zh ADD CONSTRAINT fk_t_zh_bib_site_space FOREIGN KEY ( id_site_space ) REFERENCES pr_zh.bib_site_space( id_site_space );

ALTER TABLE pr_zh.t_zh ADD CONSTRAINT fk_t_zh_t_roles FOREIGN KEY ( create_author ) REFERENCES utilisateurs.t_roles( id_role );

ALTER TABLE pr_zh.t_zh ADD CONSTRAINT fk_t_zh_id_nomenclature_sdage FOREIGN KEY ( id_sdage ) REFERENCES ref_nomenclatures.t_nomenclatures( id_nomenclature );

ALTER TABLE pr_zh.t_zh ADD CONSTRAINT fk_t_zh_t_nomenclatures_id_frequency FOREIGN KEY ( id_frequency ) REFERENCES ref_nomenclatures.t_nomenclatures( id_nomenclature );

ALTER TABLE pr_zh.t_zh ADD CONSTRAINT fk_t_zh_t_nomenclatures_spread FOREIGN KEY ( id_spread ) REFERENCES ref_nomenclatures.t_nomenclatures( id_nomenclature );

ALTER TABLE pr_zh.t_zh ADD CONSTRAINT fk_t_zh_t_roles_update_author FOREIGN KEY ( update_author ) REFERENCES utilisateurs.t_roles( id_role );

ALTER TABLE pr_zh.t_zh ADD CONSTRAINT fk_t_zh_t_nomenclatures_thread FOREIGN KEY ( id_thread ) REFERENCES ref_nomenclatures.t_nomenclatures( id_nomenclature );

ALTER TABLE pr_zh.t_zh ADD CONSTRAINT fk_t_zh_t_nomenclatures_connexion FOREIGN KEY ( id_connexion ) REFERENCES ref_nomenclatures.t_nomenclatures( id_nomenclature );

ALTER TABLE pr_zh.t_zh ADD CONSTRAINT fk_t_zh_t_nomenclatures_diag_hydro FOREIGN KEY ( id_diag_hydro ) REFERENCES ref_nomenclatures.t_nomenclatures( id_nomenclature );

ALTER TABLE pr_zh.t_zh ADD CONSTRAINT fk_t_zh_t_nomenclatures_diag_bio FOREIGN KEY ( id_diag_bio ) REFERENCES ref_nomenclatures.t_nomenclatures( id_nomenclature );

ALTER TABLE pr_zh.t_zh ADD CONSTRAINT fk_t_zh_t_nomenclatures_local_typo FOREIGN KEY ( id_local_typo ) REFERENCES ref_nomenclatures.t_nomenclatures( id_nomenclature );





