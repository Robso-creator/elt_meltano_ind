all:
	@echo "#### functions implemented"
	@echo "make up ............................ docker compose up -d"
	@echo "make stop .......................... docker compose stop"
	@echo "make down .......................... docker compose down"


up:
	@echo "[UP]"
	@echo "docker compose up -d"
	@docker compose up -d
	@echo "wait 10 seconds and go -> http://localhost:9004/ for minio"

stop:
	@echo "[STOP]"
	@echo "docker compose stop"
	@docker compose stop

down:
	@echo "[DOWN]"
	@echo "docker compose down"
	@docker compose down  --remove-orphans

pc:
	@echo "pre-commit"
	@pre-commit run --all-files
