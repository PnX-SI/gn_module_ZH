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

- Télécharger puis renommer la version souhaitée du module :

  ```
  cd
  wget https://github.com/PnX-SI/gn_module_ZH/archive/X.Y.Z.zip
  unzip X.Y.Z.zip
  rm X.Y.Z.zip
  mv gn_module_ZH-X.Y.Z gn_module_ZH
  ```

- Exécuter la commande GeoNature d'installation de module

  ```
  source ~/geonature/backend/venv/bin/activate
  geonature install-gn-module ~/gn_module_ZH zones_humides
  deactivate
  sudo systemctl restart geonature
  ```

Vous pouvez modifier la configuration du module en créant un fichier `zones_humides_config.toml` dans le dossier `config` de GeoNature, en vous inspirant 
du fichier `zones_humides_config.toml.example` et en surcouchant uniquement les paramètres que vous souhaitez.

Voir [ici](/doc/admin.md) la documentation des paramètres de configuration du module pour les administrateurs.

## **Mise à jour**

- Téléchargez la nouvelle version du module

  ```
  wget https://github.com/PnX-SI/gn_module_ZH/archive/X.Y.Z.zip
  unzip X.Y.Z.zip
  rm X.Y.Z.zip
  ```

- Renommez l'ancien et le nouveau répertoire

  ```
  mv ~/gn_module_ZH ~/gn_module_ZH_old
  mv ~/gn_module_ZH-X.Y.Z ~/gn_module_ZH
  ```

- Si vous avez encore votre configuration du module dans le dossier `config` du module, copiez le vers le dossier de configuration centralisée de GeoNature :

  ```
  cp ~/gn_module_ZH_old/config/conf_gn_module.toml  ~/geonature/config/zones_humides_config.toml
  ```

- Lancez la mise à jour du module

  ```
  source ~/geonature/backend/venv/bin/activate
  geonature install-gn-module ~/gn_module_ZH zones_humides
  sudo systemctl restart geonature
  ```

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
