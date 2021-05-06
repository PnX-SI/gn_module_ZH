[33mcommit 00ac78e8e60ff94eb333af7d1bb09f7e075bc707[m[33m ([m[1;36mHEAD -> [m[1;32m23-backend-onglet-0-save-and-get-zh-form-data[m[33m)[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Wed May 5 23:28:32 2021 +0000

    basic post for zh creation

[33mcommit 17b0ef7402907879d561f73882f37375f675050c[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Wed May 5 20:32:50 2021 +0000

    post tab0 user form data

[33mcommit 8f922848bb2c07325e3483a4b0cdeaf7d973eadc[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Tue May 4 22:46:14 2021 +0000

    get tab0 form data

[33mcommit 42d9398d7a1c643c5dfd8b42eaad7f9dac2fee86[m[33m ([m[1;31morigin/22-backend-onglet-0-menu-deroulants-2[m[33m, [m[1;32m22-backend-onglet-0-menu-deroulants-2[m[33m)[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Mon May 3 07:58:12 2021 +0000

    add CorLimList to model

[33mcommit 5e84261a7134dff36215f7dfce878d6cd352c477[m
Merge: d83b655 975283e
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Fri Apr 30 10:25:24 2021 +0000

    backend route for nomenclature values

[33mcommit 975283e5abe8da1c10822ec0ae7c8df04863c367[m[33m ([m[1;31morigin/22-backend-onglet-0-menu-deroulants[m[33m, [m[1;32m22-backend-onglet-0-menu-deroulants[m[33m)[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Fri Apr 30 08:40:39 2021 +0000

    handle exceptions

[33mcommit 33f7fa7c49b69cf9d5235b4066fe01fab1c69904[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Thu Apr 29 22:33:06 2021 +0000

    route for getting tab nomenclature values

[33mcommit 338791fb07e492bb679df535b4bcc84bc0303d76[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Thu Apr 29 14:32:43 2021 +0000

    improved sqlalchemy model for t_zh table

[33mcommit d83b655df967bc3f646bd0bbaea9cfc1de3ebec7[m[33m ([m[1;31morigin/dev[m[33m, [m[1;31morigin/HEAD[m[33m, [m[1;31morigin/23-backend-onglet-0-save-and-get-zh-form-data[m[33m, [m[1;32mdev[m[33m)[m
Merge: ca9972c 66a356f
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Thu Apr 29 12:10:09 2021 +0000

    Merge branch '21-script-pour-inserer-les-nomenclatures-menus-deroulants-dans-t_nomenclatures' into 'dev'
    
    Resolve "script pour insérer les nomenclatures (menus déroulants) dans t_nomenclatures"
    
    Closes #21
    
    See merge request natural-solutions/gn_module_zones_humides!9

[33mcommit 66a356fa8c3362936f5a3e35df5ab339fb73bd93[m[33m ([m[1;31morigin/21-script-pour-inserer-les-nomenclatures-menus-deroulants-dans-t_nomenclatures[m[33m, [m[1;32m21-script-pour-inserer-les-nomenclatures-menus-deroulants-dans-t_nomenclatures[m[33m)[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Wed Apr 28 14:28:12 2021 +0000

    add sdage and sage as foreign key in t_zh

[33mcommit 3815f98299d8fee5ec3d7b2adf8d867fe0c684af[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Wed Apr 28 14:24:53 2021 +0000

    sqlalchemy corrections because of mcd changes

[33mcommit 26dd165ecfdbe26a294bd1ce0bc76abf90fa10df[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Wed Apr 28 13:15:00 2021 +0000

    correct mcd for cor_urban_type_range

[33mcommit 0d62b7343e215ca623132311271772c7093d3a31[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Wed Apr 28 12:16:42 2021 +0000

    add install module scripts for nomenclatures and example data

[33mcommit 578c7b6a1480cc93d7bafc98b34ba4ad5392eeb7[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Mon Apr 26 23:11:05 2021 +0000

    add sql script insert into ref_habitat and pr_zh schema

[33mcommit 8f6e0bbe86afb974a19d0083eec50f0b5b529397[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Mon Apr 26 22:44:51 2021 +0000

    add sql script insert into ref_nomenclatures

[33mcommit 61b9a534c7aa94faaa4690ce5e36b0ab336d73aa[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Mon Apr 26 22:33:47 2021 +0000

    add script create tables in install_gn_module.py

[33mcommit 4c81922d6c260fa44642de8a93911d4ef13c52ed[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Mon Apr 26 22:30:21 2021 +0000

    script create pr_zh schema and tables

[33mcommit ca9972c6a066458311b3e13dfd33c07c6a28334b[m
Merge: 15ce3f3 f36a7a7
Author: amine <amine_hamouda@natural-solutions.eu>
Date:   Mon Apr 12 13:47:12 2021 +0000

    Merge branch '20-creation-du-formulaire-onglet-renseignements-generaux' into 'dev'
    
    Resolve "Création du formulaire onglet renseignements généraux"
    
    Closes #20
    
    See merge request natural-solutions/gn_module_zones_humides!8

[33mcommit f36a7a7f7a4ef8104889fbfcdce983c425434ee7[m
Author: amine <amine_hamouda@natural-solutions.eu>
Date:   Mon Apr 12 15:40:56 2021 +0200

    init tabs forms

[33mcommit 315b2af4ed42ddfc1e9882bc3f3b4b10a40845be[m
Author: amine <amine_hamouda@natural-solutions.eu>
Date:   Wed Apr 7 16:15:56 2021 +0200

    add form tabs

[33mcommit c0646843605ed47c17844ce97d3cd34e1f3b5481[m
Author: amine <amine_hamouda@natural-solutions.eu>
Date:   Wed Apr 7 11:30:16 2021 +0200

    inti general-info form

[33mcommit 15ce3f36ce59ad24aef46173eec0d6eedf339f97[m
Merge: 0cb2100 e98147a
Author: amine <amine_hamouda@natural-solutions.eu>
Date:   Wed Mar 31 13:52:11 2021 +0000

    Merge branch '19-mise-en-place-des-fonctionnalites-associees-a-la-carte-dessin-de-polygones-points-telechargement' into 'dev'
    
    Resolve "Mise en place des fonctionnalités associées à la carte (dessin de polygones, points, téléchargement geom..)"
    
    Closes #19
    
    See merge request natural-solutions/gn_module_zones_humides!7

[33mcommit e98147a069c2017db6ee537703da8c5c0d139d7d[m
Author: amine <amine_hamouda@natural-solutions.eu>
Date:   Thu Mar 18 19:59:35 2021 +0100

    init map draw from

[33mcommit eb1eeb67118587c42aa1adcf495716758805af6e[m[33m ([m[1;31morigin/15-ajout-du-bouton-sur-la-carte-d-accueil[m[33m)[m
Author: amine <amine_hamouda@natural-solutions.eu>
Date:   Tue Mar 16 09:01:06 2021 +0100

    rename add button && reset onResieze listener

[33mcommit 5997d387a9c4c249b151c371698c4959d844746d[m
Author: amine <amine_hamouda@natural-solutions.eu>
Date:   Mon Mar 15 14:47:07 2021 +0100

    add action buttons && delete confirm modal

[33mcommit 0cb2100aa329be5c5f29195623f0119a7fe040cc[m
Merge: a64b04f 6e2a0b7
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Wed Mar 10 14:16:47 2021 +0000

    Merge branch '17-insert-into-script-removed-from-install-process' into 'dev'
    
    Resolve "insert into script removed from install process"
    
    Closes #17
    
    See merge request natural-solutions/gn_module_zones_humides!5

[33mcommit 6e2a0b7c2d575794d3fa0c40799087be2bd3c548[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Wed Mar 10 14:04:28 2021 +0000

    insert into script removed from install process

[33mcommit a64b04f28c912db8d21d3e648000382d5aaf0b84[m
Merge: 3bfbc7e cb25a33
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Fri Mar 5 13:53:55 2021 +0000

    Merge branch '14-adaptation-du-code-d-occtax-pour-la-page-d-accueil' into 'dev'
    
    Resolve "Adaptation du code d'OccTax pour la page d'accueil"
    
    Closes #14
    
    See merge request natural-solutions/gn_module_zones_humides!2

[33mcommit cb25a336dbe7c7c4fa20e8c2e421cbc6e8f6cc58[m
Author: amine <amine_hamouda@natural-solutions.eu>
Date:   Fri Mar 5 14:51:06 2021 +0100

    update gitignore && add not null prop  to geom field

[33mcommit e34deab5c0cd101bb01b56e3efeb3f368405417d[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Fri Mar 5 13:13:22 2021 +0000

    sql script insert 3 fake zh into t_zh table

[33mcommit 21c7b22edb1e25543e92e9f6ec84d83d49f3cbdf[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Thu Mar 4 12:30:02 2021 +0000

    token bug fix : http removed from appconfig of the zh module

[33mcommit 59868f02fb320742487ed1284bc514b7684509d9[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Wed Mar 3 13:49:13 2021 +0000

    module install process : pr_zh schema and t_zh included

[33mcommit 4231ba49f1b7851e6625665039f0f5bb2d33da98[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Mon Feb 22 14:38:59 2021 +0000

    add create t_zh table in /data repo

[33mcommit 29fa3568c353434cb2842f8ff84c221cfdb495af[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Mon Feb 22 14:26:01 2021 +0000

    delete one ZH + permissions on routes

[33mcommit 65af8439a648f677760c379ccbd65aecad26409a[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Sat Feb 20 23:20:33 2021 +0000

    list of zh with ngx data-table + link with polygons of the map

[33mcommit d8960814e91bf9c1f0140f2ded1f645e6084b792[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Wed Feb 17 00:24:49 2021 +0000

    create zh-map-list component - map displayed

[33mcommit 3bfbc7e6b6dbe453d746c8799f4475898c3ddcef[m
Author: AJambon <aureliejambon@orange.fr>
Date:   Thu Jan 14 11:17:21 2021 +0000

    Update issues.md

[33mcommit 2545b41202e1ec6db7619bfa7390b6ee9928182f[m
Author: AJambon <aureliejambon@orange.fr>
Date:   Thu Jan 14 11:11:10 2021 +0000

    Add new file

[33mcommit aeb2e24f2cb49a6b8803d38cf6e7cb3dd4510723[m
Author: AJambon <aureliejambon@orange.fr>
Date:   Thu Jan 14 11:10:10 2021 +0000

    Add new directory issue_templates

[33mcommit 8a8097c121b8b6892111040a1638a10fcb7f3187[m
Author: AJambon <aureliejambon@orange.fr>
Date:   Thu Jan 14 11:09:39 2021 +0000

    Add new directory .gitlab

[33mcommit dd83753ba8b02565b1d612ba0095c824c2b6cffd[m
Author: anthony_henry <anthony_henry@natural-solutions.eu>
Date:   Mon Dec 21 13:27:57 2020 +0000

    Add .gitlab-ci.yml

[33mcommit cdb9ea0c55fa762cf7d44de1254c71c2da6d782a[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Fri Nov 27 18:43:07 2020 +0100

    rst layout corrections3

[33mcommit fe40fb67daab1dcbcf779788e58ac4cd6a996216[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Fri Nov 27 02:09:24 2020 +0100

    rst layout corrections2

[33mcommit d02629e95115fc44fd3d6da8adaa634ce7d6b653[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Fri Nov 27 02:06:53 2020 +0100

    rst layout corrections

[33mcommit 7fef746b1bd933fdf7ccafe92b9966c53bd0d107[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Fri Nov 27 02:01:52 2020 +0100

    readme: install + desinstall

[33mcommit 797ae1e4da312444cded9a1ea3bb1766a77e5dd9[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Fri Nov 27 01:44:33 2020 +0100

    readme: installation

[33mcommit 177f5dff975b85f5e3057b8615283c8d0e956c07[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Fri Nov 27 01:30:51 2020 +0100

    gn_module_templates corrected and adapted

[33mcommit cebcef4da2cf52ef0b0f9e686373897822671e3b[m
Author: Julien Corny <julien_corny@natural-solutions.eu>
Date:   Thu Nov 26 10:56:35 2020 +0100

    create gn repository

[33mcommit 0833fdda8e1ff5e09b4e352b3975c5eeefec3b95[m
Author: TheoLechemia <theo.lechemia@ecrins-parcnational.fr>
Date:   Sat Mar 7 15:16:52 2020 +0100

    ajout style leaflet + ivy compil

[33mcommit 067b875e93a27ea5906c4af543b407afe3048f3e[m
Author: TheoLechemia <theo.lechemia@ecrins-parcnational.fr>
Date:   Sat Mar 7 14:48:35 2020 +0100

    Revue du template de module (ng9 + pnx-map)

[33mcommit 53655176caab087349c139622c4557fd7a1ec6d4[m
Author: Théo Lechémia <theo.lechemia@ecrins-parcnational.fr>
Date:   Tue Feb 11 18:02:59 2020 +0100

    Create requirements.txt

[33mcommit 11a8a9a217c27bbae6a9a12f134c579f75f061fb[m
Author: Théo Lechémia <theo.lechemia@ecrins-parcnational.fr>
Date:   Tue Feb 11 18:02:31 2020 +0100

    Delete requirements.txt

[33mcommit b5a2d7c9a0a8f812ab26f113556c8b89494058f7[m
Author: Camille Monchicourt <camille.monchicourt@ecrins-parcnational.fr>
Date:   Fri Jul 12 13:42:02 2019 +0200

    README - Ajout de lien vers doc

[33mcommit e0537f6b83d8f98c015084e5456b0de726504b95[m
Author: Théo Lechémia <theo.lechemia@ecrins-parcnational.fr>
Date:   Wed Jun 12 10:17:20 2019 +0200

    Update README.rst

[33mcommit b044fcc7c69614dbc213a34be06e26d7c4002aa2[m
Author: Théo Lechémia <theo.lechemia@ecrins-parcnational.fr>
Date:   Wed Jun 12 10:16:30 2019 +0200

    Update README.rst

[33mcommit e4652cd28e914210aac972e94966d5cd6c183ba4[m
Author: TheoLechemia <theo.lechemia@ecrins-parcnational.fr>
Date:   Wed Jun 12 10:12:53 2019 +0200

    template

[33mcommit c8fa1607cd6e510b795e49b4d6bcd97388ea17cc[m
Author: Théo Lechémia <theo.lechemia@ecrins-parcnational.fr>
Date:   Wed Jun 12 09:45:34 2019 +0200

    Initial commit
