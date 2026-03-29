PASSWORD=$$(docker exec nexus3 bash -c 'cat /nexus-data/admin.password')
COMPOSE_FILE=docker-compose.yml

.PHONY: start start_nexus stop integration reload clean shell docs docs-check docs-sphinx set-version test test-integration lint format changelog-draft sync-src

start: start_nexus
	@docker compose --progress quiet pull
	@docker compose up -d

	@sleep 10
	@echo " syncing files with minion..."
	@docker exec salt-master sh -c 'salt \* saltutil.sync_all' > /dev/null 2>&1

start_nexus:
	@docker compose --progress quiet -f $(COMPOSE_FILE) pull
	@docker compose -f $(COMPOSE_FILE) up -d nexus3

	@./bin/check_nexus.sh

	@echo
	@echo "admin password:"
	@docker exec nexus3 bash -c 'cat /nexus-data/admin.password'
	@echo
	@echo "NEXUS_PASSWORD=$(PASSWORD)" > .env

stop:
	@docker compose -f $(COMPOSE_FILE) stop

integration: clean
	@$(MAKE) COMPOSE_FILE=tests/files/integration.yml start
	@docker exec -w /tests/integration salt-master ash -c 'pip install pytest; pytest ./'
	@$(MAKE) COMPOSE_FILE=tests/files/integration.yml stop

test:
	@nox -e tests

test-integration:
	@nox -e integration

lint:
	@pre-commit run --all-files

format:
	@ruff format src _modules _states _utils tests

reload:
	@docker exec -it salt-master salt-key -D -y
	@docker rm -f salt-minion
	@docker compose up -d
	@sleep 10
	@docker exec salt-master ash -c 'salt \* saltutil.sync_all' > /dev/null 2>&1 

clean: 
	@docker compose stop
	@docker compose -f tests/files/integration.yml stop
	@docker container prune -f
	@docker system prune -f --volumes

shell:
	@docker exec -it -w /srv salt-master ash || true

docs:
	@python3 ./bin/generate_docs_from_docstrings.py

docs-check:
	@python3 ./bin/generate_docs_from_docstrings.py --check

docs-sphinx:
	@nox -e docs

changelog-draft:
	@nox -e changelog

sync-src:
	@python3 ./bin/sync_legacy_to_src.py

set-version:
	@if [ -n "$(VERSION)" ]; then \
		python3 ./bin/update_file_versions.py "$(VERSION)"; \
	else \
		python3 ./bin/update_file_versions.py --from-branch; \
	fi