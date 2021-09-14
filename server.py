import socket
import threading
import time
from scheduler import Scheduler

def run_scheduler_tasks(scheduler):
    scheduler.run_tasks()

if __name__ == "__main__":
    s = socket.socket()
    port = 8888

    s.bind(('', port))

    s.listen(5)

    schedule = Scheduler()

    t1 = threading.Thread(target=run_scheduler_tasks, args=(schedule, ))
    t1.start()


    while True:
        c, addr = s.accept()
        print('Got connection from', addr)
        task = c.recv(1024).decode()
        schedule.add_task(task)
        c.close()
        break
