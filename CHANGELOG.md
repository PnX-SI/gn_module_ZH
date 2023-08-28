# Changelog

## 1.2.0 - La Brenne (unreleased)

Nécessite la version 2.13.0 (ou plus) de GeoNature.

**🚀 Nouveautés**

- Compatibilité avec GeoNature 2.13.0 et la refonte des permissions, en définissant les permissions disponibles du module (#22)

**🐛 Corrections**

- Correction de l'intersection des géométries (#30, by @cen-cgeier)
- Correction de la Github action de contrôle de formatage du code frontend (#33)

## 1.1.1 (2023-06-06)

**🐛 Corrections**

- Remplacement de la vue matérialisée `pr_zh.atlas_app` par une vue (utilisée par la route `/api/zones_humides/pbf/complete`) pour corriger et simplifier la mise à jour des données de l'[atlas des zones humides](https://github.com/PnX-SI/GeoNature-ZH-atlas) (#24)

## 1.1.0 - Taillefer (2023-06-02)

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
- Si vous mettez à jour le module en même temps que vous mettez à jour GeoNature, suivez la nouvelle procédure de mise à jour de GeoNature qui consiste uniquement à télécharger la nouvelle version du module, la dézipper, la renommer (ou uniquement de faire un `git pull` depuis le dossier du module si celui-ci a été installé avec git) puis lancer le script de migration de GeoNature qui se chargera de mettre à jour les modules en même temps
- Exécutez ensuite la commande suivante afin d’indiquer à Alembic que votre base de données est dans l'état de la version 1.0.0 et appliquer automatiquement les évolutions pour la passer dans l'état de la version 1.1.0 :
  ```
  geonature db stamp 01cb1aaa2062
  geonature db upgrade zones_humides@head
  ```

**📝 Contributeurs**

Cette version a été réalisée grâce à la contribution du Parc national des Écrins et de Natural Solutions.  
Merci à @TheoLechemia, @mvergez, @JulienCorny, @cen-cgeier et @camillemonchicourt.

## 1.0.0 - Camargue (2022-10-03)

**🚀 Première release**

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

**⚠️ Notes de version**

Compatible avec les versions 2.9.1 et 2.9.2 de GeoNature

**Financements**

Cette première version a été commandée par le [PNR du Luberon](https://www.parcduluberon.fr/) au nom du [SIT interparcs PACA](http://geo.pnrpaca.org/), financée par le [PNR du Luberon](https://www.parcduluberon.fr/), le [PNR de la Sainte-Baume](https://www.pnr-saintebaume.fr/) et [Natural Solutions](https://www.natural-solutions.eu/), et réalisée par [Natural Solutions](https://www.natural-solutions.eu/).
