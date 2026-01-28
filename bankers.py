def bankers_step_by_step(processes, avail, maxm, allot):
    steps = []

    n = len(processes)
    m = len(avail)

    need = [[maxm[i][j] - allot[i][j] for j in range(m)] for i in range(n)]
    steps.append(f"Initial Available: {avail}")
    steps.append("Need Matrix:")
    for i in range(n):
        steps.append(f"P{i}: {need[i]}")

    finish = [False] * n
    safe_seq = []
    work = avail[:]

    while len(safe_seq) < n:
        allocated = False

        for i in range(n):
            if not finish[i]:
                if all(need[i][j] <= work[j] for j in range(m)):
                    steps.append(f"\nChecking P{i} → CAN be allocated")
                    for j in range(m):
                        work[j] += allot[i][j]
                    steps.append(f"Updated Available: {work}")

                    safe_seq.append(processes[i])
                    finish[i] = True
                    allocated = True

        if not allocated:
            steps.append("\nSystem is in UNSAFE state (Deadlock possible)")
            return False, safe_seq, steps

    steps.append("\nSystem is in SAFE state")
    steps.append(f"Safe Sequence: {safe_seq}")
    return True, safe_seq, steps
