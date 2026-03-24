.PHONY: help build up down restart ps logs

help:
	@echo "Available commands:"
	@echo "  build   Build all services"
	@echo "  up      Start all services"
	@echo "  down    Stop all services"
	@echo "  restart Restart all services"
	@echo "  ps      Show service status"
	@echo "  logs    Show service logs"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

ps:
	docker-compose ps

logs:
	docker-compose logs -f
