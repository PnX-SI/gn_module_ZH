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

Ne pas oublier de redémarrer GeoNature après cette installation : 
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
  geonature install-gn-module ~/gn_module_ZH ZONES_HUMIDES
  deactivate
  sudo systemctl restart geonature
  ```

Vous pouvez modifier la configuration du module en créant un fichier `zones_humides_config.toml` dans le dossier `config` de GeoNature, en vous inspirant 
du fichier `zones_humides_config.toml.example` et en surcouchant uniquement les paramètres que vous souhaitez.

Voir [ici](/doc/admin.md) la documentation des paramètres de configuration du module pour les administrateurs.

Il vous faut désormais attribuer des permissions aux groupes ou utilisateurs que vous souhaitez, pour qu'ils puissent accéder et utiliser le module (voir https://docs.geonature.fr/admin-manual.html#gestion-des-droits). Si besoin une commande permet d'attribuer automatiquement toutes les permissions dans tous les modules à un groupe ou utilisateur administrateur.

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
  geonature install-gn-module ~/gn_module_ZH ZONES_HUMIDES
  sudo systemctl restart geonature
  ```

## **Désinstallation**

- Suppression des données dans plusieurs tables de la base de données

```bash
cd /home/`whoami`/geonature/backend
source venv/bin/activate
geonature db downgrade zones_humides@base
pip uninstall gn_module_zh
```

- Suppression des répertoires sur le serveur

```bash
rm -rf /home/`whoami`/gn_module_ZH
rm -rf /home/`whoami`/geonature/frontend/external_modules/zones_humides
```
