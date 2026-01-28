import threading
import time

N = 5
forks = [threading.Lock() for _ in range(N)]


def philosopher(i, log):
    left = forks[i]
    right = forks[(i + 1) % N]

    for _ in range(2):
        time.sleep(1)
        log(f"Philosopher {i} is thinking")

        with left:
            with right:
                log(f"Philosopher {i} is eating")
                time.sleep(1)


if __name__ == "__main__":
    threads = []
    for i in range(N):
        t = threading.Thread(target=philosopher, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
