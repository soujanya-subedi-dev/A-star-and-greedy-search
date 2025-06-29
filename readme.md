# Pathfinding in Nepal using A* and Greedy Search

This project implements two graph search algorithms — **A\* Search** and **Greedy Best-First Search** — to find the most optimal route between cities in Nepal.

### ✅ What it does:
- Uses real-world city coordinates (from `coordinates.json`)
- Defines road connections manually in `adjacency.json`
- Calculates edge weights using the **Haversine distance**
- Builds a weighted graph based on adjacency
- Runs **A\*** and **Greedy** to find paths from **Biratnagar** to **Pokhara**
- Compares path length and cost between the two algorithms
- Visualizes the resulting paths on a map using **Folium**

### 📌 Notes:
- This is the **working version**. Previous implementations did not handle data correctly and produced inaccurate outputs.
- The A\* implementation guarantees the shortest path, while Greedy may be faster but not always optimal.

---

### 📂 Files
- `coordinates.json` – city coordinates (lat, lon)
- `adjacency.json` – valid road connections between cities
- `pathfinder.py` – main program
- `astar_path_map.html` – interactive
