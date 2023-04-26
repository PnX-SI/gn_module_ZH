# Changelog


## 1.1.0 (2022-10-03)

- installer le module (sans la partie BDD) :
  geonature install-gn-module <chemin vers module> ZONES-HUMIDES --upgrade-db
- stamper la version suivante : 
  geonature db stamp 01cb1aaa2062
  geonature db upgrade zones_humides@head

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