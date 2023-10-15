PASSWORD=$$(docker exec nexus3 bash -c 'cat /nexus-data/admin.password')

start: start_nexus
	@docker-compose pull
	@docker-compose up -d

	@sleep 10
	@echo " syncing files with minion..."
	@docker exec salt-master sh -c 'salt \* saltutil.sync_all' > /dev/null 2>&1

start_nexus:
	@docker-compose pull
	@docker-compose up -d nexus3

	@./test-env/check_nexus.sh

	@echo
	@echo "admin password:"
	@docker exec nexus3 bash -c 'cat /nexus-data/admin.password'
	@echo
	@echo "NEXUS_PASSWORD=${PASSWORD}" > .env

stop:
	@docker-compose stop

integration: start
	@docker exec -w /tests salt-master ash -c 'pip install pytest; pytest ./'

reload:
	@docker exec -it salt-master salt-key -D -y
	@docker rm -f salt-minion
	@docker-compose up -d
	@sleep 10
	@docker exec salt-master ash -c 'salt \* saltutil.sync_all' > /dev/null 2>&1 

shell:
	@docker exec -it -w /srv salt-master ash || true