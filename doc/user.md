# **DOCUMENTATION UTILISATEUR EXPERT**

&nbsp;

## Préalable

Connaître son profil utilisateur (expert ou consultant) pour que l'administrateur puisse configurer les droits adéquats.  

**Expert** : tous les droits (ajout, suppression, modification, lecture) des ZH 

**Consultant** : Accès à la fiche complète + télechargement de la fiche de synthèse 

&nbsp;

## **Ecran d'accueil du module zones humides**

&nbsp;

<kbd>![accueil ecran](doc/ecran_accueil.png)</kbd>
<figcaption align = "center"><b>Ecran d'accueil du module</b></figcaption>

&nbsp;

L'écran d'accueil est constitué d'une carte et de la liste des zones humides. Un clic sur le polygone d'une ZH sur la carte met en surbrillance à droite la ZH correspondante dans la liste (et inversement avec en plus un zoom sur le polygone concerné).  

La liste des zones humides inclut 3 boutons : 
- <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/pen-to-square.svg" width="20" height="20"> pour modifier/terminer la saisie de la zone humide (si droits utilisateur expert - et en fonction des droits donnés dans le module admin) 
- <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/circle-info.svg" width="20" height="20"> pour accéder la fiche complète d'information de la ZH 
- <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/trash-can.svg" width="20" height="20"> pour supprimer une ZH (si droits utilisateur expert - et en fonction des droits donnés dans le module admin) 

La liste permet par défaut l'affichage des 100 dernières ZH saisies/modifiées dans le but d'améliorer les performances. Si l'utilisateur a besoin d'accéder à plus de ZH, il est nécessaire d'en faire la demande à l'administrateur pour qu'il puisse changer le nombre de ligne (100 par défaut) dans le fichier de configuration du module.  

Le bouton, situé à gauche des colonnes de la liste, permet à l'utilisateur de choisir les colonnes à afficher (multiselect). L’ordre d’affichage des colonnes suit l’ordre dans lequel celles-ci ont été sélectionnées. 

Sur la carte, le champ "rechercher un lieu" permet de saisir directement le nom d'un lieu pour accélérer la recherche (en haut à droite de la carte). Un bouton est également disponible à côté de ce champ en haut à droite de la carte pour changer le fond de carte. Si vous avez besoin d’ajouter de nouveaux fonds cartographiques, veuillez contacter votre administrateur. 

En haut à gauche de l'écran, se trouve un bouton pour "filtrer" les zones humides et un bouton pour “ajouter une zone humide” pour commencer une nouvelle saisie (voir ci-dessous pour plus de détails sur le fonctionnement).  

&nbsp;

**Les filtres :** 

- _Filtres de base_ : Une première série de filtres est immédiatement accessible au clic et permet de filtrer les ZH selon leurs principaux critères d'identification : type, nom, critères géographiques, superficie. 

- _Recherche avancée_ : Si l'utilisateur a besoin de filtres supplémentaires, il peut cliquer sur 'recherche avancée' : il pourra alors filtrer sa recherche sur des critères de fonctions, de valeurs socio-économiques et d’intérêts patrimoniaux (avec la possibilité d’affiner la recherche en indiquant des critères de qualification et connaissance). La recherche avancée peut également s’effectuer sur les critères de statuts et gestion de la ZH ainsi que sur les critères d’évaluation de l’état fonctionnel de la zone humide et des menaces.  

_Fonctionnement des filtres multi-critères :_

Les différents critères des filtres peuvent bien entendu s’ajouter les uns aux autres pour contraindre la recherche. Par exemple si l’utilisateur sélectionne le bassin versant du ‘Calavon’ dans le champ ‘Bassin versant’ et le département Alpes-de-Haute-Provence dans le champ ‘Département’, le résultat fera apparaître les zones humides faisant partie à la fois du bassin versant du ‘Calavon’ ET des Alpes-de-Haute-Provence.  

Pour les champs à choix multiples (tels que le type SDAGE, les fonctions, qualifications, …) il suffit que les zones humides respectent l'un des éléments sélectionnés pour qu'elles apparaissent dans les résultats. Par exemple si l’utilisateur sélectionne le bassin versant du ‘Calavon’ dans le champ ‘Bassin versant’, le département Alpes-de-Haute-Provence dans le champ ‘Département’, ainsi que le SDAGE 05 et le SDAGE 06 dans le champ ‘Type SDAGE de la zone humide’, le résultat fera apparaître les zones humides faisant partie à la fois du bassin versant du ‘Calavon’ ET des Alpes-de-Haute-Provence ET ayant un SDAGE 05 OU un SDAGE 06. 


_Filtres pour la hiérarchisation :_ 

Les filtres comprennent également une “recherche par hiérarchisation”. Celle-ci ne peut pas se cumuler à la “recherche avancée”.  Pour utiliser la “recherche par hiérarchisation” il faut d’abord sélectionner un bassin versant dans le champ “Bassin versant” de la recherche multi-critères. Ensuite cliquer sur “Recherche hiérarchisation”. L’utilisateur pourra alors ajouter (bouton  “ajouter”) autant de critères de hiérarchisation que nécessaires à sa recherche, un critère étant défini par le triplet une règle, sa qualification et sa connaissance. Un bouton “OU/ET” permet à l’utilisateur d’indiquer si les zones humides recherchées respecteront tous les critères listés (“ET”) ou au moins un des critères (“OU”).  

Il est possible de cliquer sur le bouton “réinitialiser” pour supprimer tous les filtres. 

&nbsp;

<kbd>![filtres](doc/filtres.png)</kbd>
<figcaption align = "center"><b>A droite de l'écran se trouve la liste des zones humides résultants des filtres appliqués </b></figcaption>

&nbsp;

## **Ecran d'accueil du module zones humides**

&nbsp;

Les formulaires de saisie sont répartis en 10 onglets.  

Ces formulaires peuvent être accédés pour la création ou l’édition d’une zone humide :

- Le bouton "ajouter une zone humide" sur l'écran d'accueil permet de commencer la saisie d'une nouvelle zone humide : l'utilisateur arrive sur l'onglet 'Carte' pour commencer par saisir les informations minimales nécessaires à la création d'une ZH. 

- Le bouton de la liste des zones humides permet d’éditer une ZH si elle a déjà été créée et qu'il veut modifier/ajouter/supprimer des informations. 

&nbsp;

**Enregistrer :** 

En bas à droite de chaque onglet se trouvent des boutons "quitter" et "enregistrer".

L'utilisateur peut enregistrer sa saisie à tout moment en cliquant sur le bouton "enregistrer". S'il change d'onglet sans enregistrer alors qu'il a fait une modification, une pop-up demande confirmation à l'utilisateur : 

<kbd>![save_modif](doc/save_modif.png)</kbd>


&nbsp;

**Naviguer :** 

L'utilisateur peut naviguer :  

- progressivement lors de la saisie en suivant l'ordre des onglets : chaque enregistrement amène automatiquement à l'onglet suivant.   

- directement vers l'onglet de son choix en cliquant sur le titre de l'onglet en haut de l'écran 

La seule contrainte de navigation se trouve lorsque l'utilisateur clique sur "ajouter une zone humide" : il arrive alors sur l'onglet 'Carte' et ne peut pas changer d'onglet avant d'avoir enregistré les informations minimales requises pour la création d'une ZH. 

&nbsp;

**Quitter :** 

L'utilisateur peut cliquer sur le bouton "quitter" à tout moment. Une pop-up de confirmation s'ouvre pour demander l'action à suivre : retourner sur la liste des ZH ou aller dans sa fiche complète.

<kbd>![redirection](doc/redirection.png)</kbd>

Si l'utilisateur quitte la saisie avant d'avoir enregistré les informations de l'onglet 'Carte', aucune ZH n'est créée. A partir du moment où l'utilisateur a enregistré les infos minimales dans l'onglet 'Carte', l'utilisateur peut quitter à tout moment et la ZH apparaîtra (même si incomplète) au sein de la liste des autres ZH, sur la page d'accueil.  

&nbsp;

**Onglet 'Carte' :** 

Il permet de saisir les informations minimales requises pour la création d'une ZH :  

- Nom de la ZH 

- Organisme de l'utilisateur : attention, après un premier enregistrement, le nom de l'organisme n'est plus modifiable (même en revenant sur l'onglet en mode édition) car il est utilisé pour générer le code unique de la zone humide lors de sa création.  

- Critères de délimitation de la ZH 

- Type de zone humide SDAGE 

- Contour de la zone humide

<kbd>![carte_tab](doc/carte_tab.png)</kbd>

&nbsp;

**Géométrie de la zone humide :** 

- Le bouton  en haut à gauche de la carte permet de dessiner les contours de la zone humide sur la carte. Il faut que le dernier point du tracé corresponde au 1er point pour terminer le tracé.  

- Il est possible de dessiner le contour de la ZH en plusieurs parties (= multiples polygones) si nécessaire.

- Pour faciliter le tracé de la zone humide : 
  - Un bouton "afficher toutes les zones humides sur la carte" permet d'afficher en bleu toutes les zones humides déjà saisies dans le module.  
  - Si le tracé de la ZH intersecte une ZH déjà existante, le tracé de la nouvelle ZH sera automatiquement rogné de l'intersection lors de l'enregistrement. 

<kbd>![intersection](doc/intersection.png)</kbd>
<figcaption align = "center"><b>A gauche, tracé d'une nouvelle ZH (en vert) qui recouvre en partie une ZH déjà existante (en bleu). A droite, la partie commune a automatiquement été rognée de la nouvelle ZH lors de l'enregistrement.   </b></figcaption>

&nbsp;

Il est possible de modifier le tracé du polygone en cliquant sur le bouton "éditer" en haut à gauche de la carte.

_Important : ne pas oublier de cliquer sur "save" une fois la modification du tracé faite, sinon la modification ne sera pas prise en compte lorsque l'utilisateur cliquera sur le bouton "enregistrer"._

<kbd>![save_contour](doc/save_contour.png)</kbd>

&nbsp;

Il est possible de supprimer le tracer d'une ZH : cliquer sur le bouton , cliquer ensuite une fois sur le polygone, puis sur "save" (et bien sûr "enregistrer" avant de changer d'onglet) 

Comme pour l'écran d'accueil, il est possible de rechercher un lieu pour accélérer la recherche sur la carte, et de changer le fond de carte.  

&nbsp;

**Onglet 1 'Renseignements' :** 

- Identification de la ZH 

- Références bibliographiques :
  - pour ajouter des références à la ZH : un champs en "autocomplete" permet de saisir quelques lettres de l'élément à trouver, puis de cliquer sur l'élément sélectionné dans l'autocomplete pour l'ajouter dans un tableau en-dessous. Il est possible d'ajouter et supprimer des éléments de ce tableau. La suppression d’un élément du tableau entraine juste la suppression de la liaison entre la ZH et la référence, en aucun cas la référence ne sera retirée de la liste des références de l’outil. 
  - si des références bibliographiques sont manquantes dans l’outil (pas la recherche via l’autocomplete ne donne pas de résultat : il faut demander à l'administrateur d'ajouter l'élément manquant en base de données (pas de possibilité pour l'utilisateur de modifier la base de données).

&nbsp;

**Onglet 2 'Délimitation' :** 

- Critères de délimitation de la zone humide : les informations obligatoires saisies dans l'onglet "Carte" sont reportées automatiquement ici. Si l'utilisateur les modifie ici, elles seront également reportées dans l'onglet "Carte".  

- Critères de délimitation de l'espace de fonctionnalité 

&nbsp;

**Onglet 3 'Description' :**

- Présentation de la ZH et de des milieux :
  - Pour la typologie SDAGE : les informations obligatoires saisies dans l'onglet "Carte" sont reportées automatiquement ici. Si l'utilisateur les modifie ici, elles seront également reportées dans l'onglet "Carte". 
  - Les éléments disponibles dans le sous-type SAGE dépendent du choix fait pour le champ "Typologie SDAGE".  

- Description de l'espace de fonctionnalité 
- Usages ou processus naturels 

&nbsp;

**Onglet 4 'Fonctionnement' :**

- Régime hydrique 
- Connexion de la zone humide dans son environnement 
- Diagnostic fonctionnel

&nbsp;

**Onglet 5 'Fonctions et valeurs' :**

- Fonctions hydrologiques / biogéochimiques 
- Fonctions biologiques / écologiques 
- Intérêts patrimoniaux 
- Habitats naturels humides patrimoniaux : lors de l'ajout d'un habitat, la liste des cahiers habitats disponibles dépend du choix fait dans le champ précédent "Corine biotopes" 
- Faune et flore patrimoniale

Dans la partie " Faune et flore patrimoniale", il est possible de télécharger la liste des taxons observés sur le territoire de la zone humide en cliquant sur le bouton "Générer la liste des espèces".  Cette liste de taxons doit respecter les critères suivants (disponibles également en cliquant sur le point d'interrogation) : 
- Les taxons listés sont issus d’observations ayant des coordonnées géographiques précises, ce qui permet de garantir que les observations ont été réalisées dans le périmètre strict de la zone humide 
- Les taxons listés ont au moins un statut d’évaluation et/ou de protection et/ou de menace (au minimum vulnérable) 
- Les taxons listés sont issus d’observations datant de moins de 20 ans

C'est l'administrateur qui paramètre la source de la liste des espèces (synthèse de l'instance GeoNature sur laquelle se trouve le module zones humides, GeoNature d'une autre instance ou autres).  

Si aucune espèce respectant les critères n'a été observée dans la ZH, un message s'affiche pour l'indiquer. 

&nbsp;

<kbd>![taxons](doc/taxons.png)</kbd>

&nbsp;

La liste des espèces est fournie par 3 fichiers csv (1 pour la flore, 1 pour la faune invertébrée, 1 pour la faune vertébrée). Les fichiers peuvent être téléchargés directement sous le bouton 'Générer la liste des espèces' et sont également automatiquement disponibles dans l'onglet 8. Chaque clic sur le bouton génère les fichiers, ce qui permet à l'expert de voir l'évolution des espèces sur la zone concernée à travers le temps. 

<kbd>![ressources_taxons](doc/ressources_taxons.png)</kbd>
<figcaption align = "center"><b>Les csv sont listés automatiquement dans l'onglet 8 </b></figcaption>

Ces fichiers permettent à l'expert de remplir les autres champs de la partie "Faune et flore patrimoniale" : Flore – nombre d'espèces, Faune vertébrée – nombre d'espèces, Faune invertébrée – nombre d'espèces. 

&nbsp;

**Onglet 6 'Statuts' :**

- Régime foncier - Statut de propriété 
- Structure de gestion 
- Instruments contractuels et financiers 
- Inventaires 
- Principaux statuts 
- Zonage des documents d'urbanisme : possibilité pour chaque commune intersectéeant dans par la ZH de renseigner un type de document communal, avec pour chacun, plusieurs types de classements

<kbd>![tab6](doc/tab6.png)</kbd>

&nbsp;

**Onglet 7 'Evaluation' :**

Onglet de synthèse et de proposition d'actions où sont reportées certaines informations précédemment saisies. Ces informations assistent l'expert pour remplir la dernière partie de cet onglet concernant les propositions d'actions.  

La liste de propositions d'actions ne peut pas être modifiée par l'utilisateur l'expert. L'administrateur se charge des modifications nécessaires dans la table concernée en BDD sur demande de l'utilisateur.  

<kbd>![tab7](doc/tab7.png)</kbd>

&nbsp;

**Onglet 8 'Ressources documentaires' :**

Cet onglet permet de stocker des ressources documentaires selon 3 formats : 

- _Des images_. Par défaut, le format accepté est .jpg et le fichier ne doit pas dépasser 0,5 Mo. Le nom du fichier doit aussi respecter un format strict (codeZH_nb, ex: 83PNRL0001_8) pour pouvoir être uploadé. 

Un bouton à gauche de chaque image uploadée permet de définir l'image principale de la ZH (possibilité de cocher une seule image à la fois).  

- _Des documents PDF_. Par défaut, la taille du fichier ne doit pas excéder 1,5 Mo.  

- _Des csv_. Ces fichiers concernent uniquement les csv téléchargés lors de la "génération de la liste des espèces" dans l'onglet 5. Il n'est pas encore possible d'uploader des csv.  

Chaque fichier peut être supprimé ou téléchargé par l'utilisateur.  

Lors de l'upload, l'utilisateur doit également indiquer le titre et l'auteur du document.

&nbsp;

<kbd>![tab8](doc/tab8.png)</kbd>

&nbsp;

**Onglet 9 'Hiérarchisation' :**

Cet onglet permet de générer automatiquement (= pas d'action requise par l'utilisateur expert) une note pour la ZH. Cette note est générée en fonction des renseignements fournis par l'utilisateur expert dans les onglets précédents.  

La note dépend de règles de calcul propres au bassin versant dans lequel se situe la ZH :
- si la ZH est située sur plusieurs bassins versants, celui ayant la plus grande intersection avec la ZH est utilisé.
- Si la ZH n'est située sur aucun bassin versant ou si aucune règle n'est disponible pour le bassin versant, un message en informera l'utilisateur. 

Si le bassin versant sur lequel est la ZH possède la rubrique 1 "Type de zones humides" comme règle, l'application va vérifier si le type SDAGE sélectionné dans l'onglet 3 par l'utilisateur fait bien partie de la liste des types SDAGE disponibles pour le calcul de la hiérarchisation. Dans le cas contraire, un message en informera l'utilisateur et celui-ci pourra modifier son choix dans l'onglet 3 pour pouvoir générer une note dans l'onglet 9.

Pour plus de détails sur le fonctionnement de la hiérarchisation, voir la documentation [hiérarchisation](/doc/hierarchy.md)

&nbsp;

**La fiche complète :**

La fiche complète regroupe toutes les infos de la ZH, y compris celles non visibles lors de la saisie dans les formulaires car générées en arrière-plan (ex : la liste des communes présentes sur le territoire de la ZH, leur pourcentage de recouvrement, …).  

Pour faciliter la consultation, un bouton <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/sort.svg" width="20" height="20"> en bas à droite de l'écran permet de déplier/replier les informations de toutes les sections en une seule fois.

&nbsp;

<kbd>![fiche_complete](doc/fiche_complete.png)</kbd>

&nbsp;

3 boutons sont disponibles en haut à droite :  

- _Fiche pdf_ : permet de générer une fiche de synthèse de la ZH en pdf, automatiquement stockée comme ressource documentaire de la zone humide dans l'onglet 8. A noter que seule la photo principale est retenue dans cette fiche synthèse pour illustrer la ZH.  

- _Modifier_ : permet de renvoyer directement en mode édition pour modifier les données dans les différents onglets pour les utilisateurs autorisés à le faire. 

- _Supprimer_ : permet de supprimer la ZH pour les utilisateurs autorisés à le faire. Une pop-up demande confirmation avant d'exécuter l'action.  

