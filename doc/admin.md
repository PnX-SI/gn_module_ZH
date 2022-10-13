# **DOCUMENTATION ADMINISTRATEUR**

&nbsp;

## **1 - Modification des paramètres du module**

&nbsp;

Le module ZH contient des paramètres que l'administrateur peut modifier dans le fichier config/conf_schema_toml.py (voir la suite du document pour le détail de ces paramètres).  

Une fois les modifications de config/conf_schema_toml.py enregistrées, la procédure de mise à jour du module est la suivante :   

```bash
cd ~/geonature/backend 
source venv/bin/activate 
geonature update_module_configuration zones_humides 
sudo systemctl restart geonature 
```

&nbsp;

## **2 - Affichage de la liste des zones humides**

&nbsp;

L'administrateur peut modifier les colonnes de la liste des zones humides affichée sur la page d'accueil. Cela est possible grâce au paramètre _available_maplist_column_ de _config/conf_schema_toml.py_ qui contient la liste des colonnes que le backend envoie au frontend. La clé _prop_ doit avoir pour valeur un nom de la colonne de la table _pr_zh.t_zh_. La clé _name_ a pour valeur le nom de la colonne à afficher en frontend. A noter que la liste des colonnes obtenues en cliquant sur le picto <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/gear.svg" width="20" height="20"> dans le tableau en frontend correspond à la liste des colonnes listées dans _available_maplist_column_.

Le paramètre _default_map_list_conf_ contient la liste des colonnes affichées en front. Il faut que les colonnes listées dans ce paramètre soient présentes dans _available_maplist_column_.


&nbsp;

<kbd>![columns](doc/show_columns.png)</kbd>

&nbsp;

## **3 - Les nomenclatures**

&nbsp;

Le paramètre nomenclatures de _config/conf_schema_toml.py_ contient la liste des éléments de nomenclatures contenus dans la table _ref_nomenclatures.t_nomenclatures_ et envoyés vers le frontend. Les termes utilisés dans la liste correspondent pour la quasi-totalité à ceux utilisés dans la colonne mnemonique de la table _ref_nomenclatures.bib_nomenclatures_types_. Si une nomenclature évolue, il suffit donc de modifier en base de données la table _ref_nomenclatures.t_nomenclatures_ (ex : modification de label, suppression/ajout d’élément, …). Ces modifications seront alors reportées directement au frontend (ex : contenu des menus déroulants, …).

&nbsp;

## **4 - Les référentiels géographiques**

&nbsp;

Le paramètre _ref_geo_referentiels_ de _config/conf_schema_toml.py_ contient la liste des inventaires intersectant le territoire de la ZH qui doivent être recherchés et fournis dans la section 6 de la fiche complète. Il est possible de retirer ou ajouter des inventaires : 

Si l'administrateur veut en ajouter un, il doit d'abord vérifier s'il existe dans la table _ref_nomenclatures.bib_nomenclatures_types_, sinon l'ajouter à cette table. Il doit ensuite vérifier si les objets géographiques (notamment les géométries) liés à ce type d'inventaire sont insérés dans la table _ref_geo.l_areas_, sinon les ajouter à cette table. Ensuite, reporter la valeur de la colonne type_code de la table _ref_nomenclatures.bib_nomenclatures_types_ comme valeur de la clé _type_code_ref_geo_ et mettre la clé _active_=True dans _conf_schema_toml.py_.  

Si l'administrateur désire qu'un inventaire n'apparaisse plus dans la section 6 de la fiche complète, il suffit de mettre _active_=False.  

&nbsp;

## **5 - Téléchargement des listes de taxons**

&nbsp;

Lorsque l'utilisateur clique sur "générer la liste des espèces" dans l'onglet 5, l'application génère 3 fichiers csv correspondant aux taxons de flore, faune vertébrée et invertébrée protégés et observés au sein du périmètre de la zone humide. Voir la documentation utilisateur du module pour plus de détails sur les critères retenus pour la composition de cette liste. A noter qu’il s’agit d’une liste de taxons et non pas d’une liste d’occurrences de taxons (les observations liées à 1 taxon représentent donc 1 seule ligne). Chaque clic sur le bouton génère les fichiers, ces derniers étant stockés sur le serveur (et donc constamment disponibles au téléchargement) dans le dossier _static_.  

Par défaut, les 3 vues (_vertebrates_view_name_, _invertebrates_view_name_ et _flore_view_name_) sont paramétrées pour : 

- lister les taxons présents dans la synthèse GeoNature de l'instance sur laquelle est déployé le module ZH. Les vues utilisent donc la table gn_synthese.synthese en base de données. 
- utiliser les statuts d’évaluation, protection et menace listés dans la table taxonomie.bdc_statut 

Si l'administrateur veut changer la source de données, par exemple se brancher sur la synthèse d'une autre instance en configurant un foreign data wrapper, il devra supprimer les vues déjà existantes en base de données puis les recréer en respectant leur structure :  
- _id_zh_ - integer : id de la zh concernée 
- _cd_nom_ - integer : cd_nom du taxon 
- _group_class_ - character varying (50) : classe du taxon 
- _group_order_ - character varying (50) : ordre du taxon 
- _scientific_name_ - character varying (500) : nom scientifique du taxon 
- _vernac_name_ - character varying (1000) : nom vernaculaire du taxon 
- _statut_type_ - character varying (250) : type de statut d’évaluation, de protection et/ou de menace 
- _statut_ - text : détail du statut d’évaluation, de protection et/ou de menace du taxon 
- _article_ - text : références de l’article détaillant le statut 
- _doc_url_ - text : url vers l’article 
- _last_date_ – timestamp without time zone : date de dernière observation du taxon 
- _observer_ - character varying (1000) : nom et prénom de l’observateur 
- _organisme_ - character varying (500) : organisme de l’observateur 
- _obs_nb_ - integer : nombre d’observations 

L’association _id_zh_/_cd_nom_ doit être unique puisque la vue liste les taxons protégés présents dans chaque zone humide.  

Le script _data/script_create_taxon_view.sh_ permet d’aider la génération des vues en indiquant la table source des occurrences de taxons et la table listant les statuts d’évaluation, protection et menaces. Etant donné que par défaut les vues sont construites sur la base de la structure des tables _gn_synthese.synthese_ et _taxonomie.bdc_statut_ de GeoNature, ce script fonctionne de manière optimale en utilisant des sources de données dont la structure est identique, c’est-à-dire provenant de GeoNature, que ce soit en local (= l’instance sur laquelle est installé le module ZH) ou à l’extérieur (ex : un _foreign data wrapper_ vers les données d’un autre GeoNature). Si l’administrateur désire utiliser d’autres sources de données structurées différemment, il devra modifier le code sql de ce script pour obtenir la structure attendue (décrite ci-dessus) des vues.

&nbsp;

<kbd>![columns](doc/taxons.png)</kbd>

&nbsp;

## **6- Les ressources documentaires**

&nbsp;

Les fichiers uploadés par l'utilisateur dans l'_onglet 8 – ressources documentaires_ doivent respecter des règles par défaut :  
- les extensions acceptées sont ".pdf" et ".jpg" 
- la taille maximale du fichier doit être de 1,5 Mo pour les pdf et 0,5 Mo pour les jpg.  
- les noms de fichiers jpg doivent respecter le format suivant : codeZH_numeroPhoto 
- l'administrateur peut modifier ces valeurs dans les paramètres _allowed_extensions_, _max_pdf_size_, _max_jpg_size_. Il peut également supprimer les vérifications de nom de fichier et d'extensions en modifiant les paramètres _filename_validated_ et _fileformat_validated_.  

&nbsp;

## **7- La fiche de synthese en pdf**

&nbsp;

La fiche de synthese en pdf peut se télécharger dans la fiche complète. Il est possible d’insérer une image à la fin du pdf (par exemple un bandeau jpg illustrant les différents partenaires) en indiquant le nom de l’image comme valeur du paramètre “pdf_last_page_img” du fichier _config/conf_schema_toml.py_. L’image doit être insérée dans le répertoire _static_ du module.  

&nbsp;

## **8- Paramétrage des règles pour les calculs de la hiérarchisation**
&nbsp;

Voir le document dédié : [hiérarchisation](/doc/hierarchy.md)

&nbsp;

## **9- Gestion des ressources bibliographiques**

&nbsp;

Dans la version actuelle du module, la création d'une référence bibliographique se fait directement en base de données. L'utilisateur a donc seulement la possibilité de lier une référence existante à une zone humide (onglet 1). Si la référence dont l'utilisateur a besoin est manquante dans l'autocomplete _Références bibliographiques_ de l'onglet 1, il doit s'adresser à l'administrateur pour que celui-ci l'ajoute. 

L'administrateur doit donc remplir la table _pr_zh.t_references_, dont seulement le champ _titre_ est à renseigner obligatoirement, pour ajouter une référence bibliographique. 

&nbsp;

## **10- Configurer un export de données**

&nbsp;

Le module export de GeoNature peut être utilisé. Voir son fonctionnement [ici](https://github.com/PnX-SI/gn_module_export)

&nbsp;

## **11- Gestion des fonds cartographiques**

&nbsp;

Les fonds cartographiques sont configurés au niveau du fichier de laconfiguration GeoNature (voir exemple de _MAPCONFIG_ [ici](https://github.com/PnX-SI/GeoNature/blob/master/config/default_config.toml.example#L188)) - donc hors de la configuration du module. Cette configuration permet d'avoir accès à différents fonds de carte au sein du module : 
- sur la page d’accueil
- sur la page de création d’une ZH (onglet "Carte")
- sur la fiche complète