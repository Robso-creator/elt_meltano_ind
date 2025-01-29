all:
	@echo "#### functions implemented"
	@echo "make up ............................ docker compose up -d"
	@echo "make stop .......................... docker compose stop"
	@echo "make down .......................... docker compose down"
	@echo "make du ............................ down up"
	@echo "make rm ............................ remove all stopped containers and dangling volumes"
	@echo "make pc ............................ pre-commit"
	@echo "make logs-webserver ................ show logs webserver"
	@echo "make logs-scheduler ................ show logs scheduler"


up:
	@echo "[UP]"
	@echo "docker compose up -d"
	@docker compose up -d

stop:
	@echo "[STOP]"
	@echo "docker compose stop"
	@docker compose stop

down:
	@echo "[DOWN]"
	@echo "docker compose down"
	@docker compose down  --remove-orphans

du: down up

pc:
	@echo "pre-commit"
	@pre-commit run --all-files

rm: down
	@echo ""
	@echo ""
	@echo "remove all stopped containers"
	command docker ps -aqf status=exited | xargs -r docker rm
	@echo ""
	@echo ""
	@echo "remove all dangling volumes"
	@# The dangling filter matches on all volumes not referenced by any containers
	command docker volume ls -qf dangling=true | xargs -r docker volume rm
	@echo ""

logs-webserver:
	@echo "Logs webserver"
	@docker logs -f elt_meltano_ind-airflow-webserver-1 -f

logs-scheduler:
	@echo "Logs webserver"
	@docker logs -f elt_meltano_ind-airflow-scheduler-1 -f
