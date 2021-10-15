export const ModuleConfig = {
  ID_MODULE: 11,
  MODULE_CODE: "ZONES_HUMIDES",
  MODULE_URL: "zones_humides",
  available_maplist_column: [
    {
      name: "Id",
      prop: "id_zh",
    },
    {
      name: "Code",
      prop: "code",
    },
    {
      name: "Nom de la zone humide",
      prop: "main_name",
    },
    {
      name: "Auteur",
      prop: "author",
    },
    {
      name: "Auteur derniere modification",
      prop: "update_author",
    },
    {
      name: "Date de creation",
      prop: "create_date",
    },
    {
      name: "Date de modification",
      prop: "update_date",
    },
  ],
  default_maplist_columns: [
    {
      name: "Nom de la zone humide",
      prop: "main_name",
    },
    {
      name: "Code de la zone humide",
      prop: "code",
    },
    {
      name: "Typologie SDAGE",
      prop: "sdage",
    },
    {
      name: "Bassin versant",
      prop: "bassin_versant",
    },
  ],
  nomenclatures: [
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
  ],
};
