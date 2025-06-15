logs:
	docker compose exec -u mio web touch /tmp/mio-c-err.log && tail -f /tmp/mio-c-err.log

run:
	docker compose up --build -w

deploy:
	./deploy.sh