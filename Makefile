logs:
	docker compose exec -u mio web touch /tmp/mio-c-err.log && tail -f /tmp/mio-c-err.log

prod_logs:
	ssh minionki tail -f /tmp/mio-c-err.log

run:
	docker compose up --build -w

db:
	docker compose exec db mysql --password=root

prod_db:
	ssh minionki mysql -p

deploy:
	./deploy.sh

chmod:
	find . -name "*.cgi" -type f -exec chmod +x {} \;
	find . -name "*.py" -type f -exec chmod +x {} \;
