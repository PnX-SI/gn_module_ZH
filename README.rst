Module Zones Humides de GeoNature
=================================

Installation
------------

- cd /home/\`whoami\`
- git clone https://gitlab.com/natural-solutions/gn_module_zones_humides.git
- cd /home/\`whoami\`/gn_module_zones_humides
- git checkout branchname
- cd /home/\`whoami\`/geonature/backend
- source venv/bin/activate
- geonature install_gn_module /home/\`whoami\`/gn_module_zones_humides /zones_humides

Désinstallation (à mettre à jour lorsque la base de données sera concernée)
---------------------------------------------------------------------------

- cd /home/\`whoami\`/geonature/backend
- source venv/bin/activate
- geonature deactivate_gn_module zones_humides # attention à corriger, deactivate_gn_module = erreur
- sudo psql -h localhost -p 5432 -U geonatadmin -d geonature2db -b -c "DELETE FROM gn_commons.t_modules WHERE module_code='ZONES_HUMIDES';"
- rm -rf /home/\`whoami\`/gn_module_zones_humides
- rm -rf /home/\`whoami\`/geonature/external_modules/zones_humides
