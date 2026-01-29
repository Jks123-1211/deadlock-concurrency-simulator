🖥️ Deadlock & Concurrency Simulator

Operating Systems Project

A Python-based interactive simulator that demonstrates core Operating System concepts including deadlock detection, avoidance, recovery, concurrency control, starvation, and aging, with real-time visualization and a user-friendly GUI.

🚀 Features
🔴 Deadlock Handling

Deadlock Detection using Wait-For Graph cycle detection

Deadlock Recovery by terminating a victim process

Graph Visualization with deadlock cycles highlighted

Dynamic Wait-For Graph: user-defined processes and dependencies

🔵 Deadlock Avoidance

Banker’s Algorithm implementation

Step-by-step safety check with Need, Available, and Safe Sequence

Dynamic user input for processes, resources, allocation, and max matrices

🟢 Concurrency & Synchronization

Producer–Consumer Problem using semaphores and mutex locks

Dining Philosophers Problem with deadlock-free synchronization

🟣 Scheduling Concepts

Starvation Demonstration showing indefinite waiting of low-priority processes

Aging Demonstration preventing starvation via dynamic priority increase

🎨 GUI & UX Highlights

Interactive Tkinter-based GUI

Color-coded sections for each OS concept

Dark Mode toggle for better readability

Hover tooltips explaining each feature

Clear Log button for repeated demonstrations

Real-time execution log panel

🧠 Technologies Used

Python 3

Tkinter (GUI)

Threading & Synchronization

NetworkX + Matplotlib (Graph Visualization)

📂 Project Structure
deadlockconcurrencysimulator/
│
├── main.py                 # GUI & application controller
├── bankers.py              # Banker's Algorithm implementation
├── deadlock_detection.py   # Deadlock detection & recovery logic
├── wait_for_graph.py       # Wait-for graph visualization
├── producer_consumer.py    # Producer–Consumer synchronization
├── philosophers.py         # Dining Philosophers simulation
├── starvation_aging.py     # Starvation & aging demonstrations

▶️ How to Run
1️⃣ Install Dependencies
pip install matplotlib networkx

2️⃣ Run the Application
python main.py

🧪 Example Use Cases

Visualize deadlock cycles in a wait-for graph

Test system safety using Banker’s Algorithm with custom input

Observe starvation and how aging resolves it

Demonstrate classic synchronization problems interactively