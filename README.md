# **MODULE ZONES HUMIDES DE GEONATURE**

## **Documentation**

- [Utilisateur](/doc/user.md)
- [Administrateur](/doc/admin.md)
- Hiérarchisation : 
  - Consulter [ici](/doc/hierarchy.md) la documentation d'implémentation des règles de hiérarchisation en base de données
  - Consulter (pas encore disponible) [ici](https://geonature.fr/documents/) le pdf contenant la méthodologie complète de hiérarchisation

## **Requis**

Pour que la fonctionnalité d'export de PDF, fonctionne il est nécessaire d'installer sur Debian 11 le paquet suivant :
`sudo apt install libgdk-pixbuf2.0-dev` (lancer un `sudo apt update` peut être nécessaire).

Cela est dû à la version de la lirairie Python `weasyprint` qui requiert ce paquet. Cela sera résolu quand cette librairie sera mise à jour car, dans les dernières versions, cette dépendance n'est plus requise.

Ne pas oublier de redémarrer GeoNature : 
`sudo systemctl restart geonature`

## **Installation**

- Définir le nom de la branche

```bash
BRANCHNAME='master'
```

- Copier le dépôt

```bash
cd /home/`whoami`
git clone https://github.com/PnX-SI/gn_module_ZH.git
cd /home/`whoami`/gn_module_ZH
git checkout $BRANCHNAME
```

- Exécuter la commande GeoNature d'installation de module

```bash
cd /home/`whoami`/geonature/backend
source venv/bin/activate
geonature install_gn_module /home/`whoami`/gn_module_ZH /zones_humides
```

- Facultatif : modifier les paramètres par défaut du module :

```bash
nano /home/`whoami`/gn_module_ZH/config/conf_schema_toml.py
```

Après avoir modifié le fichier de paramètres, faire une mise à jour :

```bash
cd /home/`whoami`/geonature/backend
source venv/bin/activate
geonature update_module_configuration zones_humides
```

Voir [ici](/doc/admin.md) pour documentation des paramètres de configuration du module pour les administrateurs

## **Désinstallation**

- Exécuter la commande GeoNature de désactivation de module

```bash
cd /home/`whoami`/geonature/backend
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
sudo psql -h localhost -p $SQL_PORT -U $GEONAT_USER -d $GEONAT_DB -b -f "/home/`whoami`/gn_module_ZH/data/desinstall.sql"
```

- Suppression des répertoires sur le serveur

{- Attention, commandes irréversibles de suppression de fichiers sur le serveur (à faire uniquement si vous êtes certain de savoir ce que vous faites !) -}

```bash
rm -rf /home/`whoami`/gn_module_ZH
rm -rf /home/`whoami`/geonature/external_modules/zones_humides
```
