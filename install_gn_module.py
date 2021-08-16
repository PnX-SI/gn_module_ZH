import subprocess
import sys

import logging
from pathlib import Path

ROOT_DIR = Path(__file__).absolute().parent
log = logging.getLogger(__name__)


def gnmodule_install_app(gn_db, gn_app):
    '''
        Fonction principale permettant de réaliser les opérations d'installation du module
    '''
    with gn_app.app_context():
        # To run a SQL script use the gn_db parameter
        # gn_db.session.execute(open(<my_sql_data.sql>, 'r').read())
        # gn_db.session.commit()
        try:
            gn_db.session.execute(
                open(str(ROOT_DIR / "data/script_create_tables.sql"), "r").read()
            )
            gn_db.session.execute(
                open(
                    str(ROOT_DIR / "data/insert_into_ref_nomenclatures_schema.sql"), "r").read()
            )
            # gn_db.session.execute(
            #    open(
            #        str(ROOT_DIR / "data/insert_into_ref_habitats_schema.sql"), "r").read()
            # )
            gn_db.session.execute(
                open(str(ROOT_DIR / "data/insert_into_pr_zh_schema.sql"), "r").read()
            )
            gn_db.session.execute(
                open(str(ROOT_DIR / "data/insert_into_fake_data.sql"), "r").read()
            )
            gn_db.session.execute(
                open(str(ROOT_DIR / "data/insert_into_atlas_vm.sql"), "r").read()
            )
            gn_db.session.commit()
        except Exception as e:
            log.error(e)
            raise
