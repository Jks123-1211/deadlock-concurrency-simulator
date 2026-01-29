import time

class Process:
    def __init__(self, pid, priority):
        self.pid = pid
        self.priority = priority
        self.wait_time = 0

    def __repr__(self):
        return f"P{self.pid}(Priority={self.priority})"


def starvation_demo(log):
    log("STARVATION DEMO STARTED")

    processes = [
        Process(0, 1),  # Low priority (starves)
        Process(1, 5),
        Process(2, 6),
        Process(3, 7)
    ]

    for cycle in range(5):
        processes.sort(key=lambda p: p.priority, reverse=True)
        running = processes[0]

        log(f"CPU allocated to {running}")
        time.sleep(1)

        for p in processes[1:]:
            p.wait_time += 1

    log("Process P0 is starving (never executed)")
    log("STARVATION DEMO COMPLETED\n")


def aging_demo(log):
    log("AGING DEMO STARTED")

    processes = [
        Process(0, 1),   # Low priority initially
        Process(1, 5),
        Process(2, 6),
        Process(3, 7)
    ]

    for cycle in range(8):
        # Apply aging to waiting process P0
        for p in processes:
            if p.pid == 0:
                p.priority += 2   # stronger aging

        processes.sort(key=lambda p: p.priority, reverse=True)
        running = processes[0]

        log(f"Cycle {cycle}: CPU allocated to {running}")
        time.sleep(1)

        # Once P0 runs, stop demo
        if running.pid == 0:
            log("Aging successful: P0 got CPU")
            break

    log("AGING DEMO COMPLETED\n")
