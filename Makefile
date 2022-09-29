kafak_build:
	@docker-compose up -d
check_kafka:
	@nc -z localhost 22181 && nc -z localhost 29092