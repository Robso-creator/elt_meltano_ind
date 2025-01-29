all:
	@echo "#### functions implemented"
	@echo "make up ............................ docker compose up -d"
	@echo "make stop .......................... docker compose stop"
	@echo "make down .......................... docker compose down"
	@echo "make du ............................ down up"
	@echo "make enter-local ................... enter local"
	@echo "make rm ............................ remove all stopped containers and dangling volumes"
	@echo "make pc ............................ pre-commit"
	@echo "make logs-webserver ................ show logs webserver"
	@echo "make logs-scheduler ................ show logs scheduler"
	@echo "make logs-streamlit ................. show logs streamlit app"
	@echo "make reborn ........................ down | rm | up"
	@echo "make phoenix ....................... down | rm | build | up"
	@echo "make build .......................... build local image docker"
	@echo ""

build:
	@echo "Building local image docker..."
	@docker build -t streamlit_app:1.0 -f "./Dockerfile" "."

up:
	@echo "[UP]"
	@echo "docker compose up -d"
	@docker compose up -d
	@echo "wait 10 seconds and go -> http://localhost:8501/ for streamlit"
	@echo "wait 10 seconds and go -> http://localhost:8080/ for airflow"

stop:
	@echo "[STOP]"
	@echo "docker compose stop"
	@docker compose stop

down:
	@echo "[DOWN]"
	@echo "docker compose down"
	@docker compose down  --remove-orphans

du: down up

enter-local:
	@echo "Enter local"
	@docker exec -it airflow-webserver bash

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
	@docker logs -f airflow-webserver -f

logs-scheduler:
	@echo "Logs webserver"
	@docker logs -f airflow-scheduler -f

logs-streamlit:
	@echo "Logs streamlit app"
	@docker logs -f streamlit-app -f

reborn:
	@echo "[REBORN]"
	@echo ""
	@echo "docker compose down"
	@docker compose down --remove-orphans
	@echo "remove all stopped containers"
	command docker ps -aqf status=exited | xargs -r docker rm
	@echo ""
	@echo ""
	@echo "remove all dangling volumes"
	@# The dangling filter matches on all volumes not referenced by any containers
	command docker volume ls -qf dangling=true | xargs -r docker volume rm
	@echo ""
	@echo "docker compose up -d"
	@docker compose up -d

phoenix:
	@echo "[PHOENIX]"
	@echo ""
	@echo "docker compose down"
	@docker compose down --remove-orphans
	@echo "remove all stopped containers"
	command docker ps -aqf status=exited | xargs -r docker rm
	@echo ""
	@echo ""
	@echo "remove all dangling volumes"
	@# The dangling filter matches on all volumes not referenced by any containers
	command docker volume ls -qf dangling=true | xargs -r docker volume rm
	@echo ""
	@echo "Building local image docker..."
	@docker build -t streamlit_app:1.0 -f "./Dockerfile" "."
	@echo "docker compose up -d"
	@docker compose up -d
