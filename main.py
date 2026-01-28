import tkinter as tk
import threading
import queue
from wait_for_graph import visualize_wait_for_graph
from deadlock_detection import get_deadlock_cycle

from deadlock_detection import recover_deadlock

from bankers import bankers_step_by_step

import producer_consumer
import philosophers


# ---------- GUI SETUP ----------
root = tk.Tk()
root.title("Deadlock & Concurrency Simulator")
root.geometry("550x400")

log_queue = queue.Queue()


def log(message):
    log_queue.put(message)


def update_log():
    while not log_queue.empty():
        msg = log_queue.get()
        text_area.insert(tk.END, msg + "\n")
        text_area.see(tk.END)
    root.after(100, update_log)


# ---------- BUTTON FUNCTIONS ----------
def run_deadlock():
    graph = {
        0: [1],
        1: [2],
        2: [0]
    }

    recovered, victim, new_graph = recover_deadlock(graph)

    if recovered:
        log("Deadlock Detected")
        log(f"Victim Process Selected: P{victim}")
        log("Process terminated to recover from deadlock")
        log("Deadlock Recovered Successfully")
    else:
        log("No Deadlock Detected")
def run_bankers():
    processes = [0, 1, 2]
    avail = [3, 3, 2]
    maxm = [[7, 5, 3], [3, 2, 2], [9, 0, 2]]
    allot = [[0, 1, 0], [2, 0, 0], [3, 0, 2]]

    safe, seq, steps = bankers_step_by_step(
        processes, avail, maxm, allot
    )

    for step in steps:
        log(step)



def run_producer_consumer():
    threading.Thread(
        target=producer_consumer.producer, args=(log,), daemon=True
    ).start()

    threading.Thread(
        target=producer_consumer.consumer, args=(log,), daemon=True
    ).start()


def run_philosophers():
    for i in range(5):
        threading.Thread(
            target=philosophers.philosopher,
            args=(i, log),
            daemon=True
        ).start()


def visualize_deadlock_graph():
    graph = {
        0: [1],
        1: [2],
        2: [0]
    }

    cycle = get_deadlock_cycle(graph)
    visualize_wait_for_graph(graph, cycle)


# ---------- UI ----------
tk.Button(root, text="Detect & Recover Deadlock", command=run_deadlock).pack(pady=5)

tk.Button(root, text="Run Banker's Algorithm", command=run_bankers).pack(pady=5)
tk.Button(root, text="Producer-Consumer", command=run_producer_consumer).pack(pady=5)
tk.Button(root, text="Dining Philosophers", command=run_philosophers).pack(pady=5)
tk.Button(
    root,
    text="Visualize Wait-For Graph",
    command=visualize_deadlock_graph
).pack(pady=5)

text_area = tk.Text(root, height=15, width=65)
text_area.pack(pady=10)

update_log()
root.mainloop()
