# Changelog

## 1.4.1 - (2025-XX-XX)

(à déterminer)

**🐛 Corrections**

- Ajout du boutton "quitter" sur l'onglet 9 (#114, by @juggler31)
- Correction de la gestion des images lors de la génération (#110, by @juggler31)
- Correction de la génération de PDF (#110, by @juggler31)

## 1.4.0 - La Narse de Nouvialle (2025-03-27)

Compatibilité avec GeoNature 2.15.0 minimum.

**🚀 Nouveautés**

- Possibilité pour l'utilisateur de charger un fichier (geojson par exemple) sur la carte (#76)
- Détermination dynamique du SRID (#85)
- Les rubriques qui n'ont pas de notes de hiérarchisation (seulement affichées pour grouper les sous-catégories) sont maintenant en disable dans les filtres de hiérarchisation dans le select "Rubriques" (#91)
- Amélioration de l'affichage du nom du bassin versant principal onglet 9 et dans la fiche ZH (#98)
- Utilisation de ref_geo.l_areas pour les régions (#99)
- Amélioration de la performance du calcul de la hiérarchisation : vue pr_zh.rb_notes_summary convertie en vue matérialisée (#101)
- Affichage de la liste des bassins versants et zones hydrographiques par ordre de surface de recouvrement de la ZH dans la fiche complète et la colonne “Bassin versant” de la page d’accueil (#102)

**🐛 Corrections**

- Correction d’un bug lors de la modification d’une entrée/sortie d’eau, d’un statut de protection ou d’une action (#83, #86)
- Les règles du linting ont été ajustées aux changements de celles de geonature (#77, #84, #105)
- Correction du filtre sur les départements et bassins versants (#87)
- Correction de l’affichage du nom des sous-catégories dans l’onglet 9 (#90)
- Corrections d'une série de bugs sur les filtres de hiérarchisation (#91)
- Correction d’un bug sur l’affichage de la liste des noms des zones hydrographiques (#93)
- Correction des erreurs d’affichage de la 1ere page de la fiche pdf (#100)
- Correction de l’affichage du nom des communes dans les documents d’urbanisme (#103)
- Update configuration files (#78)
- Correction des erreurs de mise à jour des notes de hiérarchisation (#104)
- Correction erreur sous-requête à la création des vues matérialisées de taxons (#106)
- Modification de l’utilisation de leaflet.vectorgrid suite à la mise à jour de Leaflet dans geonature 2.15 (#113)
- Correction erreur 500 lorsqu’un instrument contractuel et financier était posté avec une date nulle onglet 6 (#108)
- Suppression d’un doublon de clé dans le fichier TOML d’exemple (#112)

## 1.3.1

**🐛 Corrections**

- Conversion explicite du geojson en geometry dans l'appel set_geom (#4)
- Ajout d'une vérification empêchant de créer une ZH contenant entièrement une autre ZH (#3)
- Warnings mineurs résolus (#1, #5)

## 1.3.0 - Les Eyguestres (2024-07-01)

Nécessite la version 2.14.0 (ou plus) de GeoNature.

**🚀 Nouveautés**

- Compatibilité avec GeoNature 2.14 : mise à jour de SQLAlchemy en version 1.4 (#59)
- Amélioration des performances pour générer la liste des espèces par l’utilisation de vues matérialisées mises à jour avec une tâche Celery (#61)
- Remplacement de ng-multiselect-dropdown et angular2-multiselect par zh-multiselect basé sur ng-select (#66)

**🐛 Corrections**

- Correction du message d’erreur à l’ouverture de la fiche ZH en mode consultation (#63)
- Correction de nom de bassin versant dans l’onglet 9 (#64) et fiche complète (#69 et #71)
- Correction d’un bug lors de la modification d’un média dans l'onglet 8 (#62)
- Correction d’une erreur lors de l’insertion de données d’exemple (#60)
- Nettoyage du fichier package.json (#66)

## 1.2.0 - La Brenne (2023-10-17)

Nécessite la version 2.13.3 (ou plus) de GeoNature.

**🚀 Nouveautés**

- Compatibilité avec GeoNature 2.13 et la refonte des permissions, en définissant les permissions disponibles du module (#22)

**🐛 Corrections**

- Correction de l'intersection des géométries (#30, by @cen-cgeier)
- Correction de la Github action de contrôle de formatage du code frontend (#33)
- Suppression des derniers restes de l'ancienne méthode d'accès à la configuration de GeoNature (`appConfig`)

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
