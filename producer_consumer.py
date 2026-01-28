import threading
import time
import queue

buffer = queue.Queue(5)
empty = threading.Semaphore(5)
full = threading.Semaphore(0)
mutex = threading.Lock()


def producer(log):
    for i in range(10):
        time.sleep(1)
        empty.acquire()
        mutex.acquire()
        buffer.put(i)
        log(f"Produced: {i}")
        mutex.release()
        full.release()


def consumer(log):
    for i in range(10):
        full.acquire()
        mutex.acquire()
        item = buffer.get()
        log(f"Consumed: {item}")
        mutex.release()
        empty.release()
        time.sleep(1)



if __name__ == "__main__":
    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
