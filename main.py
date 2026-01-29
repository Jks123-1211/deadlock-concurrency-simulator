import tkinter as tk
import threading
import queue

from bankers import bankers_step_by_step
from deadlock_detection import recover_deadlock, get_deadlock_cycle
from wait_for_graph import visualize_wait_for_graph
import producer_consumer
import philosophers
import starvation_aging


# ================= TOOLTIP =================
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tip:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        tk.Label(
            self.tip,
            text=self.text,
            bg="#333333",
            fg="white",
            font=("Arial", 9),
            padx=6,
            pady=4
        ).pack()

    def hide(self, event=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None


# ================= DARK MODE =================
dark_mode = False

LIGHT_THEME = {"root": "#f5f5f5", "text_bg": "white", "text_fg": "black"}
DARK_THEME = {"root": "#1e1e1e", "text_bg": "#2d2d2d", "text_fg": "white"}

all_frames = []
all_buttons = []
all_labels = []


def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    theme = DARK_THEME if dark_mode else LIGHT_THEME

    root.configure(bg=theme["root"])
    text_area.configure(bg=theme["text_bg"], fg=theme["text_fg"], insertbackground=theme["text_fg"])

    for frame in all_frames:
        frame.configure(bg=theme["root"])

    for lbl in all_labels:
        lbl.configure(bg=theme["root"], fg=theme["text_fg"])

    for btn in all_buttons:
        btn.configure(bg="#444444" if dark_mode else btn.original_bg,
                      fg="white" if dark_mode else "black")


# ================= GUI SETUP =================
root = tk.Tk()
root.title("Deadlock & Concurrency Simulator")
root.geometry("650x520")
root.configure(bg=LIGHT_THEME["root"])

log_queue = queue.Queue()

toggle_btn = tk.Button(root, text="🌙 Dark Mode", command=toggle_dark_mode)
toggle_btn.pack(anchor="ne", padx=10, pady=5)
toggle_btn.original_bg = LIGHT_THEME["root"]
all_buttons.append(toggle_btn)


def log(msg):
    log_queue.put(msg)


def update_log():
    while not log_queue.empty():
        text_area.insert(tk.END, log_queue.get() + "\n")
        text_area.see(tk.END)
    root.after(100, update_log)


# ================= CORE FUNCTIONS =================
def run_deadlock():
    graph = {0: [1], 1: [2], 2: [0]}
    recovered, victim, _ = recover_deadlock(graph)
    if recovered:
        log("Deadlock Detected")
        log(f"Victim Process Selected: P{victim}")
        log("Deadlock Recovered Successfully")
    else:
        log("No Deadlock Detected")


def visualize_deadlock_graph():
    graph = {0: [1], 1: [2], 2: [0]}
    cycle = get_deadlock_cycle(graph)
    log(f"Deadlock cycle detected: {cycle}" if cycle else "No deadlock detected")
    visualize_wait_for_graph(graph, cycle)


def run_producer_consumer():
    threading.Thread(target=producer_consumer.producer, args=(log,), daemon=True).start()
    threading.Thread(target=producer_consumer.consumer, args=(log,), daemon=True).start()


def run_philosophers():
    for i in range(5):
        threading.Thread(target=philosophers.philosopher, args=(i, log), daemon=True).start()


def run_starvation():
    threading.Thread(target=starvation_aging.starvation_demo, args=(log,), daemon=True).start()


def run_aging():
    threading.Thread(target=starvation_aging.aging_demo, args=(log,), daemon=True).start()


# ================= DYNAMIC WAIT-FOR GRAPH =================
def dynamic_wait_for_graph():
    win = tk.Toplevel(root)
    win.title("Dynamic Wait-For Graph")
    win.geometry("400x250")

    tk.Label(win, text="Number of processes:").pack()
    p_entry = tk.Entry(win)
    p_entry.pack()

    tk.Label(win, text="Edges (e.g. 0->1,1->2,2->0):").pack()
    e_entry = tk.Entry(win, width=40)
    e_entry.pack()

    def submit():
        n = int(p_entry.get())
        edges = e_entry.get().split(",")
        graph = {i: [] for i in range(n)}
        for e in edges:
            u, v = e.split("->")
            graph[int(u)].append(int(v))

        cycle = get_deadlock_cycle(graph)
        log(f"Deadlock detected in user graph: {cycle}" if cycle else "No deadlock detected")
        visualize_wait_for_graph(graph, cycle)
        win.destroy()

    tk.Button(win, text="Visualize Graph", command=submit).pack(pady=10)


# ================= DYNAMIC BANKER'S =================
def dynamic_bankers():
    win = tk.Toplevel(root)
    win.title("Dynamic Banker's Algorithm")
    win.geometry("500x400")

    tk.Label(win, text="Processes (comma separated):").pack()
    p_entry = tk.Entry(win)
    p_entry.pack()

    tk.Label(win, text="Available (comma separated):").pack()
    a_entry = tk.Entry(win)
    a_entry.pack()

    tk.Label(win, text="Allocation Matrix (rows ; cols ,):").pack()
    alloc_entry = tk.Entry(win, width=50)
    alloc_entry.pack()

    tk.Label(win, text="Max Matrix (rows ; cols ,):").pack()
    max_entry = tk.Entry(win, width=50)
    max_entry.pack()

    def submit():
        processes = list(map(int, p_entry.get().split(",")))
        avail = list(map(int, a_entry.get().split(",")))
        allot = [list(map(int, r.split(","))) for r in alloc_entry.get().split(";")]
        maxm = [list(map(int, r.split(","))) for r in max_entry.get().split(";")]

        for i in range(len(processes)):
            for j in range(len(avail)):
                if allot[i][j] > maxm[i][j]:
                    log("Invalid input: Allocation > Max")
                    return

        _, _, steps = bankers_step_by_step(processes, avail, maxm, allot)
        log("Running Banker’s Algorithm on user input")
        for s in steps:
            log(s)
        win.destroy()

    tk.Button(win, text="Run Banker’s Algorithm", command=submit).pack(pady=10)


# ================= UI HELPERS =================
def section_label(text):
    lbl = tk.Label(root, text=text, font=("Arial", 10, "bold"),
                   bg=LIGHT_THEME["root"], fg=LIGHT_THEME["text_fg"])
    lbl.pack(pady=(10, 2))
    all_labels.append(lbl)
    return lbl


def make_button(parent, text, bg, cmd, tip):
    btn = tk.Button(parent, text=text, bg=bg, command=cmd)
    btn.original_bg = bg
    btn.pack(fill="x", pady=2)
    ToolTip(btn, tip)
    all_buttons.append(btn)
    return btn


# ================= UI SECTIONS =================
section_label("Deadlock Handling")
deadlock_frame = tk.Frame(root, bg="#ffe6e6", padx=5, pady=5)
deadlock_frame.pack(fill="x", padx=10)
all_frames.append(deadlock_frame)

make_button(deadlock_frame, "Detect & Recover Deadlock", "#ff9999", run_deadlock,
            "Detects deadlock and recovers by terminating one process.")
make_button(deadlock_frame, "Visualize Wait-For Graph", "#ffb3b3", visualize_deadlock_graph,
            "Visualizes wait-for graph and highlights deadlock cycle.")
make_button(deadlock_frame, "Dynamic Wait-For Graph", "#ffcccc", dynamic_wait_for_graph,
            "User-defined deadlock visualization.")

section_label("Deadlock Avoidance (Banker's Algorithm)")
banker_frame = tk.Frame(root, bg="#e6f0ff", padx=5, pady=5)
banker_frame.pack(fill="x", padx=10)
all_frames.append(banker_frame)

make_button(banker_frame, "Dynamic Banker's Algorithm", "#99bbff", dynamic_bankers,
            "Checks system safety using Banker’s Algorithm.")

section_label("Concurrency & Synchronization")
concurrency_frame = tk.Frame(root, bg="#e6ffe6", padx=5, pady=5)
concurrency_frame.pack(fill="x", padx=10)
all_frames.append(concurrency_frame)

make_button(concurrency_frame, "Producer–Consumer", "#99e699", run_producer_consumer,
            "Producer–consumer synchronization using semaphores.")
make_button(concurrency_frame, "Dining Philosophers", "#b3ffb3", run_philosophers,
            "Dining philosophers synchronization problem.")

section_label("Scheduling: Starvation & Aging")
sched_frame = tk.Frame(root, bg="#f2e6ff", padx=5, pady=5)
sched_frame.pack(fill="x", padx=10)
all_frames.append(sched_frame)

make_button(sched_frame, "Starvation Demo", "#d1b3ff", run_starvation,
            "Demonstrates starvation due to priority scheduling.")
make_button(sched_frame, "Aging Demo", "#e0ccff", run_aging,
            "Demonstrates aging to prevent starvation.")

section_label("Execution Log")
text_area = tk.Text(root, height=12, width=80,
                    bg=LIGHT_THEME["text_bg"], fg=LIGHT_THEME["text_fg"])
text_area.pack(padx=10, pady=5)

# Clear Log button (requires text_area to exist)
def clear_log():
    text_area.delete("1.0", tk.END)

clear_btn = tk.Button(root, text="🧹 Clear Log", command=clear_log,
                      bg=LIGHT_THEME["root"])
clear_btn.pack(anchor="ne", padx=10, pady=(0, 5))
clear_btn.original_bg = LIGHT_THEME["root"]
all_buttons.append(clear_btn)
ToolTip(clear_btn, "Clears the execution log for a fresh demonstration.")

update_log()
root.mainloop()
