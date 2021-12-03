BEGIN;

INSERT INTO pr_zh.t_references(authors,pub_year,title,editor,editor_location) VALUES
('Hamouda A', 2021, 'la zone humide en front pour les nuls', 'NS', 'Marseille'),
('Corny J', 2020, 'les MCD de zones humides', 'bla bla editeurs', 'quelque part'),
('Jambon A', 2021, 'comment créer sa zone humide chez soi', 'editor', 'par là')
;



-- insert into t_nomenclature Calavon river basin rules as an example for hierarchy

INSERT INTO ref_nomenclatures.t_nomenclatures(id_type, cd_nomenclature, mnemonique, label_default, label_fr, source, statut) VALUES
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), 'iso', 'ZH isolée', 'ZH isolée', 'ZH isolée', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), 'res', 'ZH participant d''un réseau ou continuum', 'ZH participant d''un réseau ou continuum', 'ZH participant d''un réseau ou continuum', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), '0', 'Aucun', 'Aucun', 'Aucun', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), '1 ou 2', '1 ou 2', '1 ou 2', '1 ou 2', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), '2 à 5', '2 à 5', '2 à 5', '2 à 5', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), '>5', '>5', '>5', '>5', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), '1 à 4', '1 à 4', '1 à 4', '1 à 4', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), '5 à 7', '5 à 7', '5 à 7', '5 à 7', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), '8 ou 9', '8 ou 9', '8 ou 9', '8 ou 9', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), '>9', '>9', '>9', '>9', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), '1', '1', '1', '1', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), '2', '2', '2', '2', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), '3', '3', '3', '3', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), '>3', '>3', '>3', '>3', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), 'faible', 'Faible (conventionnel / contractuel / inventaire)', 'Faible (conventionnel / contractuel / inventaire)', 'Faible (conventionnel / contractuel / inventaire)', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), 'fort', 'Fort (réglementaire / maîtrise foncière)', 'Fort (réglementaire / maîtrise foncière)', 'Fort (réglementaire / maîtrise foncière)', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), 'OUI', 'OUI', 'OUI', 'OUI', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), 'NON', 'NON', 'NON', 'NON', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), 'bon', 'Non dégradée (bon)', 'Non dégradée (bon)', 'Non dégradée (bon)', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), 'mauvais', 'Très fortement dégradée (mauvais)', 'Très fortement dégradée (mauvais)', 'Très fortement dégradée (mauvais)', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), 'moyen', 'Partiellement dégradée (moyen)', 'Partiellement dégradée (moyen)', 'Partiellement dégradée (moyen)', 'ZONES_HUMIDES', 'Non validé'),
((SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY'), 'NE', 'Non évalué', 'Non évalué', 'Non évalué', 'ZONES_HUMIDES', 'Non validé')
;


-- example with bassin versant du calavon (here rb_id = 1) :

INSERT INTO pr_zh.cor_rb_rules VALUES
(1, (SELECT id_rb FROM pr_zh.t_river_basin WHERE name = 'bassin versant 1'), 1),
(2, (SELECT id_rb FROM pr_zh.t_river_basin WHERE name = 'bassin versant 1'), 2),
(3, (SELECT id_rb FROM pr_zh.t_river_basin WHERE name = 'bassin versant 1'), 3),
(4, (SELECT id_rb FROM pr_zh.t_river_basin WHERE name = 'bassin versant 1'), 4),
(5, (SELECT id_rb FROM pr_zh.t_river_basin WHERE name = 'bassin versant 1'), 5),
(6, (SELECT id_rb FROM pr_zh.t_river_basin WHERE name = 'bassin versant 1'), 6),
(7, (SELECT id_rb FROM pr_zh.t_river_basin WHERE name = 'bassin versant 1'), 7),
(8, (SELECT id_rb FROM pr_zh.t_river_basin WHERE name = 'bassin versant 1'), 8),
(9, (SELECT id_rb FROM pr_zh.t_river_basin WHERE name = 'bassin versant 1'), 9),
(10, (SELECT id_rb FROM pr_zh.t_river_basin WHERE name = 'bassin versant 1'), 10),
(11, (SELECT id_rb FROM pr_zh.t_river_basin WHERE name = 'bassin versant 1'), 11),
(12, (SELECT id_rb FROM pr_zh.t_river_basin WHERE name = 'bassin versant 1'), 12),
(13, (SELECT id_rb FROM pr_zh.t_river_basin WHERE name = 'bassin versant 1'), 13),
(14, (SELECT id_rb FROM pr_zh.t_river_basin WHERE name = 'bassin versant 1'), 14),
(15, (SELECT id_rb FROM pr_zh.t_river_basin WHERE name = 'bassin versant 1'), 15),
(16, (SELECT id_rb FROM pr_zh.t_river_basin WHERE name = 'bassin versant 1'), 16),
(17, (SELECT id_rb FROM pr_zh.t_river_basin WHERE name = 'bassin versant 2'), 1)
;


-- to do : mettre check val max 100 pour note ?
INSERT INTO pr_zh.t_items VALUES
(1, 1, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = '07 - zones humides de bas fonds en tête de bassin'), 100, 1),
(2, 1, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = '11 - zones humides ponctuelles'), 75, 1),
(3, 1, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = '05 - bordures de cours d''eau'), 50, 1),
(4, 1, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = '06 - plaines alluviales'), 25, 1),
(5, 1, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = '13 - zones humides artificielles'), 0, 1),

(6, 2, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Aucun' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 0, 2),
(7, 2, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Aucun' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 1, 3),
(8, 2, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '1 ou 2' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 13, 2),
(9, 2, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '1 ou 2' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 13, 3),
(10, 2, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '2 à 5' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 19, 2),
(11, 2, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '2 à 5' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 19, 3),
(12, 2, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '>5' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 25, 2),
(13, 2, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '>5' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 25, 3),

(14, 3, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Aucun' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 0, 2),
(15, 3, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Aucun' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 1, 3),
(16, 3, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '1 ou 2' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 11, 2),
(17, 3, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '1 ou 2' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 14, 3),
(18, 3, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '2 à 5' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 17, 2),
(19, 3, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '2 à 5' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 19, 3),
(20, 3, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '>5' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 22, 2),
(21, 3, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '>5' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 25, 3),

(22, 4, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Aucun' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 0, 2),
(23, 4, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Aucun' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 1, 3),
(24, 4, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '1 à 4' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 9, 2),
(25, 4, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '1 à 4' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 11, 3),
(26, 4, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '5 à 7' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 14, 2),
(27, 4, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '5 à 7' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 16, 3),
(28, 4, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '8 ou 9' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 18, 2),
(29, 4, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '8 ou 9' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 20, 3),
(30, 4, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '>9' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 23, 2),
(31, 4, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '>9' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 25, 3),

(32, 5, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Aucun' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 0, 2),
(33, 5, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Aucun' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 1, 3),
(34, 5, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '1' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 9, 2),
(35, 5, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '1' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 11, 3),
(36, 5, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '2' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 14, 2),
(37, 5, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '2' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 16, 3),
(38, 5, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '3' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 18, 2),
(39, 5, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '3' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 20, 3),
(40, 5, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '>3' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 23, 2),
(41, 5, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '>3' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 25, 3),

-- a inserer avec trigger quand 6 inséré dans cor_rb_rules
(42, 6, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'ZH isolée' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 0, 1),
(43, 6, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'ZH participant d''un réseau ou continuum' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 100, 1),

(44, 7, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Non évaluée'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 15, 2),
(45, 7, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Non évaluée'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 15, 3),
(46, 7, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Nulle à faible'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 0, 2),
(47, 7, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Nulle à faible'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 10, 3),
(48, 7, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Moyenne'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 20, 2),
(49, 7, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Moyenne'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 25, 3),
(50, 7, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Forte'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 33.3, 2),
(51, 7, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Forte'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 33.3, 3),

(52, 8, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Non évaluée'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 15, 2),
(53, 8, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Non évaluée'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 15, 3),
(54, 8, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Nulle à faible'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 0, 2),
(55, 8, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Nulle à faible'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 10, 3),
(56, 8, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Moyenne'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 20, 2),
(57, 8, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Moyenne'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 25, 3),
(58, 8, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Forte'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 33.3, 2),
(59, 8, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Forte'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 33.3, 3),

(60, 9, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Non évaluée'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 15, 2),
(61, 9, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Non évaluée'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 15, 3),
(62, 9, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Nulle à faible'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 0, 2),
(63, 9, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Nulle à faible'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 10, 3),
(64, 9, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Moyenne'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 20, 2),
(65, 9, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Moyenne'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 25, 3),
(66, 9, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Forte'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 33.3, 2),
(67, 9, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Forte'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 33.3, 3),

(68, 10, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Non évaluée'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 10, 1),
(69, 10, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Nulle à faible'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 0, 1),
(70, 10, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Moyenne'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 25, 1),
(71, 10, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Forte'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 50, 1),

(72, 11, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Non évaluée'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 10, 1),
(73, 11, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Nulle à faible'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 0, 1),
(74, 11, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Moyenne'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 25, 1),
(75, 11, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Forte'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'FONCTIONS_QUALIF')), 50, 1),

(76, 12, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Aucun' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 50, 1),
(77, 12, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Faible (conventionnel / contractuel / inventaire)' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 25, 1),
(78, 12, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Fort (réglementaire / maîtrise foncière)' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 0, 1),

(79, 13, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'OUI' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 0, 1),
(80, 13, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'NON' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 50, 1),

(81, 14, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Non dégradée (bon)' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 0, 1),
(82, 14, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Partiellement dégradée (moyen)' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 25, 1),
(83, 14, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Très fortement dégradée (mauvais)' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 50, 1),
(84, 14, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Non évalué' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 10, 1),

(85, 15, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Non dégradée (bon)' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 0, 1),
(86, 15, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Partiellement dégradée (moyen)' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 25, 1),
(87, 15, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Très fortement dégradée (mauvais)' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 50, 1),
(88, 15, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Non évalué' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 10, 1),

(89, 16, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Zh pas ou peu menacée'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'EVAL_GLOB_MENACES')), 0, 1),
(90, 16, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Zh modérément menacée'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'EVAL_GLOB_MENACES')), 50, 1),
(91, 16, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Zh fortement menacée'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'EVAL_GLOB_MENACES')), 100, 1),
(92, 16, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = 'Non évaluée'  and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'EVAL_GLOB_MENACES')), 25, 1),

(93, 17, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = '07 - zones humides de bas fonds en tête de bassin'), 110, 1),
(94, 17, (SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE label_default = '11 - zones humides ponctuelles'), 20, 1);


INSERT INTO pr_zh.cor_item_value VALUES
((SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = 'Aucun' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 0, 0),
((SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '1 ou 2' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 1, 2),
((SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '2 à 5' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 2, 5),
((SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '>5' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 6, 999999999),
((SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '1 à 4' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 1, 4),
((SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '5 à 7' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 5, 7),
((SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '8 ou 9' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 8, 9),
((SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '>9' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 9, 999999999),
((SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '1' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 1, 1),
((SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '2' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 2, 2),
((SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '3' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 3, 3),
((SELECT id_nomenclature FROM ref_nomenclatures.t_nomenclatures WHERE mnemonique = '>3' and id_type = (SELECT id_type FROM ref_nomenclatures.bib_nomenclatures_types WHERE mnemonique = 'HIERARCHY')), 4, 999999999);

COMMIT;
