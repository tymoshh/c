logs:
	docker compose exec -u mio web touch /tmp/mio-c-err.log && tail -f /tmp/mio-c-err.log

prod_logs:
	ssh minionki tail -f /tmp/mio-c-err.log

run:
	docker compose up --build -w

db:
	docker compose exec db mysql --password=root

deploy:
	./deploy.sh