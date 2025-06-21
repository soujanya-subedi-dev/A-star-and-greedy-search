import json
import heapq
import math
import folium
import os

# Load coordinates from JSON
with open("data/coordinates.json") as f:
    coordinates = json.load(f)
    coordinates = {k: tuple(v) for k, v in coordinates.items()}

# Function to calculate haversine distance (used as heuristic)
def haversine(coord1, coord2):
    R = 6371e3  # Earth radius in meters
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # distance in meters

# Generate a complete weighted graph using Haversine distances
graph = {}
locations = list(coordinates.keys())

for i in range(len(locations)):
    for j in range(len(locations)):
        if i == j:
            continue
        loc1 = locations[i]
        loc2 = locations[j]
        dist = haversine(coordinates[loc1], coordinates[loc2])
        graph.setdefault(loc1, {})[loc2] = dist

# Greedy Best-First Search
def greedy_search(graph, start, goal, coords):
    visited = set()
    queue = [(haversine(coords[start], coords[goal]), start, [start])]

    while queue:
        _, current, path = heapq.heappop(queue)
        if current == goal:
            return path
        visited.add(current)
        for neighbor in graph.get(current, {}):
            if neighbor not in visited:
                heapq.heappush(queue, (haversine(coords[neighbor], coords[goal]), neighbor, path + [neighbor]))
    return None

# A* Search
def a_star(graph, start, goal, coords):
    visited = set()
    queue = [(haversine(coords[start], coords[goal]), 0, start, [start])]

    while queue:
        f, g, current, path = heapq.heappop(queue)
        if current == goal:
            return path
        visited.add(current)
        for neighbor in graph.get(current, {}):
            if neighbor not in visited:
                cost = graph[current][neighbor]
                heur = haversine(coords[neighbor], coords[goal])
                heapq.heappush(queue, (g + cost + heur, g + cost, neighbor, path + [neighbor]))
    return None

# Choose start and goal locations
start = "Kirtipur, Kathmandu"
goal = "Hemja, Pokhara"
print(f"Start: {start}, Goal: {goal}")
print("Coordinates loaded successfully.")

# Run both algorithms
greedy_path = greedy_search(graph, start, goal, coordinates)
a_star_path = a_star(graph, start, goal, coordinates)

# Print results
print("\nGreedy Best-First Search Path:")
print(" -> ".join(greedy_path))

print("\nA* Search Path:")
print(" -> ".join(a_star_path))

# Create visualization map centered between start and goal
midpoint_lat = (coordinates[start][0] + coordinates[goal][0]) / 2
midpoint_lon = (coordinates[start][1] + coordinates[goal][1]) / 2
m = folium.Map(location=[midpoint_lat, midpoint_lon], zoom_start=8)

# Plot A* path in blue
for i in range(len(a_star_path) - 1):
    loc1 = coordinates[a_star_path[i]]
    loc2 = coordinates[a_star_path[i + 1]]
    folium.PolyLine([loc1, loc2], color="blue", weight=3, opacity=0.7).add_to(m)

# Add markers for A* path
for loc in a_star_path:
    lat, lon = coordinates[loc]
    folium.Marker([lat, lon], popup=f"A*: {loc}", icon=folium.Icon(color='blue')).add_to(m)

# Plot Greedy Best-First Search path in red
for i in range(len(greedy_path) - 1):
    loc1 = coordinates[greedy_path[i]]
    loc2 = coordinates[greedy_path[i + 1]]
    folium.PolyLine([loc1, loc2], color="red", weight=3, opacity=0.7, dash_array='5').add_to(m)

# Add markers for Greedy path
for loc in greedy_path:
    lat, lon = coordinates[loc]
    folium.Marker([lat, lon], popup=f"Greedy: {loc}", icon=folium.Icon(color='red')).add_to(m)

# Save HTML map
os.makedirs("output", exist_ok=True)
m.save("output/a_star_greedy_paths.html")
print("\nMap saved to output/a_star_greedy_paths.html")

# Save graph structure as JSON
with open("output/graph.json", "w") as f:
    json.dump(graph, f, indent=2)
print("Graph saved to output/graph.json")