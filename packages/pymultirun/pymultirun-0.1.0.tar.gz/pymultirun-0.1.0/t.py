import os
import time

def worker_function(name: str, age:int, sleep_time=1, **kwargs):
    pid = os.getpid()
    count = 0
    print(f"Name {name}, Age {age}, Kwargs {kwargs}.")

    try:
        while True:
            time.sleep(sleep_time)
            count += 1
            print(f"Worker {name} (PID: {pid}) - count: {count}")
    except KeyboardInterrupt:
        print(f"Worker {name} (PID: {pid}) shutting down")