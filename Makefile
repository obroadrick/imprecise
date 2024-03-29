SLEEP = sleep 5
CLIENT_REQ = 50
NUM_TASK_REQ = 3
CLIENT_NUM = 2
PYTHON = python3
SERVER_RUNNING = pgrep -x "$(PYTHON)"

run: kill
	$(PYTHON) server.py &
	$(SLEEP)
	$(PYTHON) client.py $(CLIENT_REQ) $(NUM_TASK_REQ)
server:
	$(PYTHON) server.py

client:
	$(PYTHON) client.py

tasks: #TODO add flags to gen tasks
	$(PYTHON) tasks/gen_tasks.py

kill:
	@if $(SERVER_RUNNING); then\
		pkill $(PYTHON);\
	fi
