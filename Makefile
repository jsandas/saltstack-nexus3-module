PASSWORD=$$(docker exec nexus3 bash -c 'cat /nexus-data/admin.password')
COMPOSE_FILE=docker-compose.yml

start: start_nexus
	@docker-compose pull
	@docker-compose up -d

	@sleep 10
	@echo " syncing files with minion..."
	@docker exec salt-master sh -c 'salt \* saltutil.sync_all' > /dev/null 2>&1

start_nexus:
	@docker-compose -f $(COMPOSE_FILE) pull
	@docker-compose -f $(COMPOSE_FILE) up -d nexus3

	@./bin/check_nexus.sh

	@echo
	@echo "admin password:"
	@docker exec nexus3 bash -c 'cat /nexus-data/admin.password'
	@echo
	@echo "NEXUS_PASSWORD=$(PASSWORD)" > .env

stop:
	@docker-compose -f $(COMPOSE_FILE) stop

integration: clean
	@$(MAKE) COMPOSE_FILE=tests/files/integration.yml start_nexus
	@$(MAKE) COMPOSE_FILE=tests/files/integration.yml start
	@docker exec -w /tests/integration salt-master ash -c './test_all.sh'
	@$(MAKE) COMPOSE_FILE=tests/files/integration.yml stop

reload:
	@docker exec -it salt-master salt-key -D -y
	@docker rm -f salt-minion
	@docker-compose up -d
	@sleep 10
	@docker exec salt-master ash -c 'salt \* saltutil.sync_all' > /dev/null 2>&1 

clean: 
	@docker-compose stop
	@docker-compose -f tests/files/integration.yml stop
	@docker container prune -f
	@docker system prune -f --volumes

shell:
	@docker exec -it -w /srv salt-master ash