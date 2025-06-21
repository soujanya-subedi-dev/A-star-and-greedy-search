# Pathfinding Graph Project - Nepal Locations

This project demonstrates the use of **A\*** and **Greedy Best-First Search** algorithms to find optimal paths between major landmarks in two Nepali regions: **Kathmandu** and **Pokhara**.

It uses:

- Geographical coordinates of 20 locations (10 from each region)
- Haversine distance as a heuristic
- Complete graph generation
- Visualizations of both pathfinding results and the full graph structure using `folium`

---

## 📁 Project Structure

```
project_root/
│
├── data/
│   └── coordinates.json              # Location coordinates
│
├── output/
│   ├── a_star_path.html             # A* path visualization
│   ├── graph.json                   # Full graph structure (distances)
│   └── graph_visualization.html     # Full graph visual map
│
├── pathfinder.py                    # Builds graph, runs A*, Greedy, saves results
├── graph_visualizer.py              # Visualizes all nodes and edges
├── run_all.py                       # Runs pathfinder and visualizer sequentially
└── README.md                        # Project documentation
```

---

## 📌 Requirements

Install required Python packages:

```bash
pip install folium
```

---

## 🚀 How to Run the Project

From the root folder, run:

```bash
python run_all.py
```

This will:

1. Build the graph and compute paths using A\* and Greedy (via `pathfinder.py`)
2. Visualize the full graph structure (via `graph_visualizer.py`)
3. Save all outputs inside the `output/` folder

---

## 🌍 Data Sources

- Coordinates were manually collected using public map data (Google Maps and OpenStreetMap).

---

## 📈 Algorithms Used

Start: *Kirtipur, Kathmandu* — Goal: *Hemja, Pokhara*

- **Greedy Best-First Search**: Explores nodes based only on heuristic (Haversine to goal).
- **A\***: Explores based on actual cost so far + heuristic to goal.

Both algorithms use a complete graph of all locations.

---

## 📎 Notes

- Haversine distance is in meters.
- Graph is stored in `output/graph.json` and visualized with `folium` in HTML.
- Supports easy customization of start and goal nodes in `pathfinder.py`

---

## 🛠 Future Improvements

- Add OpenStreetMap support to avoid Google API limits
- Allow interactive selection of nodes
- Color-code Kathmandu vs Pokhara nodes

---

Created by: **Soujanya Subedi**

