import json
import folium
import os

# Load coordinates and graph structure
with open("data/coordinates.json") as f:
    coordinates = json.load(f)
    coordinates = {k: tuple(v) for k, v in coordinates.items()}

with open("output/graph.json") as f:
    graph = json.load(f)

# Create a folium map centered on average location
avg_lat = sum(coord[0] for coord in coordinates.values()) / len(coordinates)
avg_lon = sum(coord[1] for coord in coordinates.values()) / len(coordinates)
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=8)

# Draw all edges in the graph
for src, neighbors in graph.items():
    for dest, dist in neighbors.items():
        loc1 = coordinates[src]
        loc2 = coordinates[dest]
        folium.PolyLine([loc1, loc2], color="gray", weight=1, opacity=0.4).add_to(m)

# Add markers for each vertex
for name, coord in coordinates.items():
    folium.Marker(coord, popup=name, icon=folium.Icon(color="blue", icon="info-sign")).add_to(m)

# Save graph visualization
os.makedirs("output", exist_ok=True)
m.save("output/graph_visualization.html")
print("Graph visualization saved to output/graph_visualization.html")
