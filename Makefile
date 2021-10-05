SLEEP = sleep 5
PYTHON = python3

run:
	$(PYTHON) server.py &
	$(SLEEP)
	python3 client.py

server:
	$(PYTHON) server.py

client:
	$(PYTHON) client.py

kill:
	pkill python3
