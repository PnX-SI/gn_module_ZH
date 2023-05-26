# Changelog

## 1.1.0 (2023-05-26)

Nécessite la version 2.12.0 (ou plus) de GeoNature.

**🚀 Nouveautés**

- Compatibilité avec GeoNature 2.12 : Angular 15, configuration dynamique, configuration centralisée
- Packaging du module (#7)
- Gestion de la BDD du module avec Alembic
- Externalisation du RefGeo
- Corrections et refactorisation diverses

**🐛 Corrections**

- Définition du SRID des champs de géométrie dans la BDD (#13)
- Correction du fonctionnement quand le module ne contient encore aucune zone humide (#10)
- Correction du fichier d'exemple de configuration (#9)
- Correction du moteur de recherche multi-critères dans la recherche sur les bassins versants (#14)
- Correction du menu déroulant du filtre sur les menaces (#19)

**⚠️ Notes de version**

- Si vous mettez à jour le module indépendamment de GeoNature, suivez la procédure classique de mise à jour du module, mais sans exécuter les évolutions de la BDD dans un premier temps (`geonature install-gn-module ~/gn_module_ZH ZONES_HUMIDES --upgrade-db=false`)
- Si vous mettez à jour le module en même que vous mettez à jour GeoNature, suivez la nouvelle procédure de mise à jour de GeoNature qui consiste uniquement à télécharger la nouvelle version du module, la dézipper, la renommer (ou uniquement de faire un `git pull` depuis le dossier du module si celui-ci a été installé avec git) puis lancer le script de migration de GeoNature qui se chargera de mettre à jour les modules en même temps
- Exécutez ensuite la commande suivante afin d’indiquer à Alembic que votre base de données est dans l'état de la version 1.0.0 et appliquer automatiquement les évolutions pour la passer dans l'état de la version 1.1.0 :
  ```
  geonature db stamp 01cb1aaa2062
  geonature db upgrade zones_humides@head
  ```

## 1.0.0 (2022-10-03)

**🚀 Première release 🚀**

Version fonctionnelle permettant :
- La création de nouvelles zones humides
- L'édition des géométries et caractéristiques des zones humides existantes
- La suppression de zones humides
- La recherche de zones humides suivant :
  - des critères généraux
  - des critères fonctionnels
  - les notes de hiérarchisation
- La consultation d'une fiche complète des caractéristiques d'une zone humide
- L'export au format pdf d'une fiche descriptive synthétique
- L'export au format csv des espèces à statut (évaluation/protection/menace) 
  observées dans le périmètre de la zone humide.
