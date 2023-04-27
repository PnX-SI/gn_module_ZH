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

## **Commandes d'installation**

- Téléchargez le module dans `/home/<myuser>/`, en remplacant `X.Y.Z` par la version souhaitée

```bash
wget https://github.com/PnX-SI/gn_module_ZH/archive/vX.Y.Z.zip
unzip vX.Y.Z.zip
rm vX.Y.Z.zip
```

- Renommez le répertoire du module

```bash
mv ~/gn_module_ZH-X.Y.Z ~/gn_module_ZH
```

- Lancez l'installation du module

```bash
source ~/geonature/backend/venv/bin/activate
geonature install-gn-module ~/gn_module_ZH ZONES_HUMIDES
#sudo systemctl restart geonature
#deactivate
```

- Facultatif : modifier les paramètres par défaut du module :

```bash
nano /home/`whoami`/gn_module_ZH/config/conf_schema_toml.py
```

Après avoir modifié le fichier de paramètres, faire une mise à jour :

```bash
cd /home/`whoami`/geonature/backend
source venv/bin/activate
geonature update_configuration
```

Voir [ici](/doc/admin.md) pour documentation des paramètres de configuration du module pour les administrateurs

## **Désinstallation**

- Suppression des données dans plusieurs tables de la base de données

```bash
cd /home/`whoami`/geonature/backend
source venv/bin/activate
geonature db downgrade zones_humides@base
```

- Suppression des répertoires sur le serveur

{- Attention, commandes irréversibles de suppression de fichiers sur le serveur (à faire uniquement si vous êtes certain de savoir ce que vous faites !) -}

```bash
rm -rf /home/`whoami`/gn_module_ZH
rm -rf /home/`whoami`/geonature/frontend/external_modules/zones_humides
```
