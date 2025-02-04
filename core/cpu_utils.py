import multiprocessing
import time


def cpu_intensive_task():
    while True:
        num = 2
        while True:
            num += 1
            for i in range(2, num):
                if num % i == 0:
                    break
            else:
                pass  # Prime number found


def simulate_high_cpu_load():
    processes = []
    for _ in range(multiprocessing.cpu_count()):  # Spawn one per CPU core
        p = multiprocessing.Process(target=cpu_intensive_task)
        p.start()
        processes.append(p)

    time.sleep(10)  # Simulate high CPU load for 10 seconds

    # Terminate all processes
    for p in processes:
        p.terminate()
