import subprocess
import os

# Define script paths
pathfinder_script = "pathfinder.py"
graph_script = "graph_visualizer.py"

# Run pathfinder.py
print("Running pathfinder.py...")
result1 = subprocess.run(["python", pathfinder_script])
if result1.returncode != 0:
    print("Error: pathfinder.py failed.")
    exit(1)

# Run graph_visualizer.py
print("\nRunning graph_visualizer.py...")
result2 = subprocess.run(["python", graph_script])
if result2.returncode != 0:
    print("Error: graph_visualizer.py failed.")
    exit(1)

print("\n All scripts executed successfully.")
