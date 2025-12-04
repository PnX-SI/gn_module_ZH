###########################
#          colors         #
###########################
PRINT_COLOR = printf
COLOR_SUCCESS = \033[1;32m
COLOR_DEBUG = \033[36m
COLOR_RESET = \033[0m

###########################
#        Variables        #
###########################

DIR_BIN = .venv/bin/
API_ENDPOINT = http://localhost:8000/api

-include Makefile.perso.mk

###########################
#      Environment        #
###########################

.PHONY: create_venv
create_venv:
	$(call display_cmd, Create venv)
	python3 -m venv .venv

.PHONY: install_geonature
install_geonature: create_venv
	$(call display_cmd, Install Geonature)
ifeq "$(wildcard .venv/lib/python3.12/site-packages/geonature)" ""
	.venv/bin/pip install "geonature[tests] @ git+https://github.com/PnX-SI/GeoNature.git@develop"
endif

###########################
#          Tests          #
###########################

.PHONY: tests
tests: install_geonature
	$(call display_cmd, Launch tests)
	.venv/bin/pip install -e .
	. .venv/bin/activate && GEONATURE_CONFIG_FILE="config/test_config.toml" ./install_db_test/03b_populate_db.sh
	GEONATURE_CONFIG_FILE="config/test_config.toml" .venv/bin/geonature upgrade-modules-db
	GEONATURE_CONFIG_FILE="config/test_config.toml" .venv/bin/pytest -vs --cov --cov-report xml

define display_cmd
	@$(PRINT_COLOR) "\n$(COLOR_SUCCESS) ########################## $(COLOR_RESET)\n"
	@$(PRINT_COLOR) "$(COLOR_SUCCESS) ### $(1) $(COLOR_RESET)\n"
	@$(PRINT_COLOR) "$(COLOR_SUCCESS) ########################## $(COLOR_RESET)\n\n"
endef
