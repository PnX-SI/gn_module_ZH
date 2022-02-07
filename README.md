# **MODULE ZONES HUMIDES DE GEONATURE**

&nbsp;

## **Installation**

- Définir le nom de la branche

```bash
BRANCHNAME='master'
```

- Copier le dépôt

```bash
cd /home/\`whoami\`
git clone https://github.com/PnX-SI/gn_module_ZH.git
cd /home/\`whoami\`/gn_module_zones_humides
git checkout $BRANCHNAME
```

- Exécuter la commande GeoNature d'installation de module

```bash
cd /home/\`whoami\`/geonature/backend
source venv/bin/activate
geonature install_gn_module /home/\`whoami\`/gn_module_zones_humides /zones_humides
```

- Facultatif : modifier les paramètres par défaut du module :

```bash
nano /home/\`whoami\`/gn_module_zones_humides /zones_humides/config/conf_schema_toml.py
```

Après avoir modifié le fichier de paramètres, faire une mise à jour :

```bash
cd /home/\`whoami\`/geonature/backend
source venv/bin/activate
geonature update_module_configuration zones_humides
```

Voir [ici](/doc/admin.md) pour documentation des paramètres de configuration du module pour les administrateurs

&nbsp;

## **Désinstallation**

- Exécuter la commande GeoNature de désactivation de module

```bash
cd /home/\`whoami\`/geonature/backend
source venv/bin/activate
geonature deactivate_gn_module zones_humides
```

- Suppression des données dans plusieurs tables de la base de données

```bash
SQL_PORT=5432
GEONAT_USER=geonatadmin
GEONAT_DB=geonature2db
```

{- Attention, commandes irréversibles de suppression de données en base de données (à faire uniquement si vous êtes certain de savoir ce que vous faites !) -}

```bash
sudo psql -h localhost -p $SQL_PORT -U $GEONAT_USER -d $GEONAT_DB -b -c "DELETE FROM gn_commons.t_modules WHERE module_code='ZONES_HUMIDES';"
sudo psql -h localhost -p $SQL_PORT -U $GEONAT_USER -d $GEONAT_DB -b -c "DROP SCHEMA IF EXISTS pr_zh CASCADE;"
sudo psql -h localhost -p $SQL_PORT -U $GEONAT_USER -d $GEONAT_DB -b -c "DELETE FROM gn_commons.t_medias where id_table_location = (SELECT id_table_location FROM gn_commons.bib_tables_location WHERE table_desc = 'Liste des zones humides');"
sudo psql -h localhost -p $SQL_PORT -U $GEONAT_USER -d $GEONAT_DB -b -c "DELETE FROM gn_commons.bib_tables_location WHERE table_desc = 'Liste des zones humides';"
sudo psql -h localhost -p $SQL_PORT -U $GEONAT_USER -d $GEONAT_DB -b -c "DROP TABLE ref_geo.insee_regions;"
sudo psql -h localhost -p $SQL_PORT -U $GEONAT_USER -d $GEONAT_DB -b -c "DELETE FROM ref_nomenclatures.defaults_nomenclatures_value WHERE mnemonique_type IN ('CRIT_DEF_ESP_FCT', 'EVAL_GLOB_MENACES', 'PERMANENCE_ENTREE', 'PERMANENCE_SORTIE', 'SUBMERSION_FREQ', 'SUBMERSION_ETENDUE', 'FONCTIONNALITE_HYDRO', 'FONCTIONNALITE_BIO', 'FONCTIONS_QUALIF', 'FONCTIONS_CONNAISSANCE', 'ETAT_CONSERVATION', 'STATUT_PROPRIETE', 'STATUT_PROTECTION');"
sudo psql -h localhost -p $SQL_PORT -U $GEONAT_USER -d $GEONAT_DB -b -c "DELETE FROM ref_nomenclatures.t_nomenclatures WHERE source IN ('ZONES_HUMIDES', 'BASSINS_VERSANTS');"
sudo psql -h localhost -p $SQL_PORT -U $GEONAT_USER -d $GEONAT_DB -b -c "DELETE FROM ref_nomenclatures.bib_nomenclatures_types WHERE source IN ('ZONES_HUMIDES', 'BASSINS_VERSANTS');"
```

- Suppression des répertoires sur le serveur

{- Attention, commandes irréversibles de suppression de fichiers sur le serveur (à faire uniquement si vous êtes certain de savoir ce que vous faites !) -}

```bash
rm -rf /home/\`whoami\`/gn_module_zones_humides
rm -rf /home/\`whoami\`/geonature/external_modules/zones_humides
```
&nbsp;

## **Hierarchisation**

- Consulter [ici](/doc/hierarchy.md) la documentation d'implémentation des règles de hiérarchisation en base de données
- {- Mettre le lien quand sera dispo : Consulter [ici](https://geonature.fr/documents/) le pdf contenant la méthodologie complète de hiérarchisation -}
