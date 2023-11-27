export const ModuleConfig = {
 "MODULE_CODE": "ZONES_HUMIDES",
 "MODULE_URL": "/zones_humides",
 "allowed_extensions": [
  ".pdf",
  ".jpg"
 ],
 "available_maplist_column": [
  {
   "name": "Nom principal",
   "prop": "main_name"
  },
  {
   "name": "Code",
   "prop": "code"
  },
  {
   "name": "Typologie SDAGE",
   "prop": "sdage",
   "sortable": true
  },
  {
   "name": "Bassin versant",
   "prop": "bassin_versant",
   "sortable": true
  },
  {
   "name": "Crit\u00e8res d\u00e9limitation (de la zh)",
   "prop": "delims",
   "sortable": true
  },
  {
   "name": "Date de cr\u00e9ation",
   "prop": "create_date"
  },
  {
   "name": "Auteur",
   "prop": "author"
  },
  {
   "name": "Organisme",
   "prop": "organism"
  },
  {
   "name": "Date de modification",
   "prop": "update_date"
  },
  {
   "name": "Auteur derni\u00e8re modification",
   "prop": "update_author"
  },
  {
   "name": "Organisme de derni\u00e8re modification",
   "prop": "update_organism"
  }
 ],
 "default_maplist_columns": [
  {
   "name": "Nom principal",
   "prop": "main_name"
  },
  {
   "name": "Code",
   "prop": "code"
  },
  {
   "name": "Typologie SDAGE",
   "prop": "sdage",
   "sortable": true
  },
  {
   "name": "Bassin versant",
   "prop": "bassin_versant",
   "sortable": true
  }
 ],
 "file_path": "static",
 "fileformat_validated": true,
 "filename_validated": true,
 "flora_view_name": {
  "category": "flora",
  "schema_name": "pr_zh",
  "table_name": "flora"
 },
 "invertebrates_view_name": {
  "category": "invertebrates",
  "schema_name": "pr_zh",
  "table_name": "invertebrates"
 },
 "max_jpg_size": 1.5,
 "max_pdf_size": 3.5,
 "module_dir_name": "gn_module_zones_humides",
 "nomenclatures": [
  "SDAGE-SAGE",
  "SDAGE",
  "CORINE_BIO",
  "CRIT_DELIM",
  "CRIT_DELIM",
  "CRIT_DEF_ESP_FCT",
  "OCCUPATION_SOLS",
  "ACTIV_HUM",
  "LOCALISATION",
  "IMPACTS",
  "EVAL_GLOB_MENACES",
  "STATUT_PROPRIETE",
  "TYP_DOC_COMM",
  "PLAN_GESTION",
  "PROTECTIONS",
  "INSTRU_CONTRAC_FINANC",
  "ENTREE_EAU",
  "SORTIE_EAU",
  "PERMANENCE_ENTREE",
  "PERMANENCE_SORTIE",
  "SUBMERSION_FREQ",
  "SUBMERSION_ETENDUE",
  "TYPE_CONNEXION",
  "FONCTIONNALITE_HYDRO",
  "FONCTIONNALITE_BIO",
  "FONCTIONS_HYDRO",
  "FONCTIONS_BIO",
  "INTERET_PATRIM",
  "VAL_SOC_ECO",
  "FONCTIONS_QUALIF",
  "FONCTIONS_CONNAISSANCE",
  "ETAT_CONSERVATION",
  "NIVEAU_PRIORITE",
  "STRAT_GESTION"
 ],
 "pdf_last_page_img": "",
 "pdf_layer_number": 6,
 "pdf_layer_threashold_ha": 1000.0,
 "pdf_small_layer_number": 0,
 "pdf_title": "Inventaire des zones humides du territoire Is\u00e8rois",
 "ref_geo_referentiels": [
  {
   "active": true,
   "type_code_ref_geo": "ZNIEFF1",
   "zh_name": "ZNIEFF Terre Type 1"
  },
  {
   "active": true,
   "type_code_ref_geo": "ZNIEFF2",
   "zh_name": "ZNIEFF Terre Type 2"
  },
  {
   "active": true,
   "type_code_ref_geo": "SRAM",
   "zh_name": "RAMSAR"
  },
  {
   "active": true,
   "type_code_ref_geo": "SIC",
   "zh_name": "Natura 2000 \u2013 Directive \u00ab\u202fHabitats, faune, flore \u00bb"
  },
  {
   "active": true,
   "type_code_ref_geo": "ZPS",
   "zh_name": "Natura 2000 \u2013 Directive \u00ab\u202fOiseaux \u00bb\u202f(ZPS)"
  }
 ],
 "species_source_name": "GeoNature",
 "vertebrates_view_name": {
  "category": "vertebrates",
  "schema_name": "pr_zh",
  "table_name": "vertebrates"
 }
}