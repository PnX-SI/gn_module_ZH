'''
   Spécification du schéma toml des paramètres de configurations
   La classe doit impérativement s'appeller GnModuleSchemaConf
   Fichier spécifiant les types des paramètres et leurs valeurs par défaut
   Fichier à ne pas modifier. Paramètres surcouchables dans config/config_gn_module.tml
'''

from marshmallow import Schema, fields


class MapListConfig(Schema):
    pass


default_map_list_conf = [
    {"prop": "main_name", "name": "Nom principal"},
    {"prop": "create_date", "name": "Date de création"}
]

available_maplist_column = [
    {"prop": "main_name", "name": "Nom principal"},
    {"prop": "create_date", "name": "Date de création"},
    {"prop": "update_date", "name": "Date de modification"}
]


class GnModuleSchemaConf(Schema):
    default_maplist_columns = fields.List(fields.Dict(), missing=default_map_list_conf)
    available_maplist_column = fields.List(
        fields.Dict(), missing=available_maplist_column
    )

