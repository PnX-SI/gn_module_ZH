INSERT INTO pr_zh.t_zh(
	code, 
	main_name, 
	create_author, 
	update_author, 
	geom,
	id_sdage
	)
	VALUES (
		'XX-XXXX-X1', 
		'zone humide 1', 
		2, 
		2,
		(SELECT the_geom_4326
		FROM gn_synthese.synthese
		WHERE id_synthese=4),
		3
	),
	(
		'XX-XXXX-X2', 
		'zone humide 2', 
		2, 
		2,
		(SELECT the_geom_4326
		FROM gn_synthese.synthese
		WHERE id_synthese=5),
		3
	),
	(
		'XX-XXXX-X3', 
		'zone humide 3', 
		2, 
		2,
		(SELECT the_geom_4326
		FROM gn_synthese.synthese
		WHERE id_synthese=6),
		3
	);
