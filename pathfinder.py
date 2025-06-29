import json
import heapq
from math import radians, sin, cos, sqrt, atan2
import folium

# --- Load Coordinates and Adjacency ---
with open("data/coordinates.json", "r") as f:
    coordinates = json.load(f)
coordinates = {k: tuple(v) for k, v in coordinates.items()}

with open("data/adjacency.json", "r") as f:
    adjacency = json.load(f)

# --- Haversine Distance Function ---
def haversine(coord1, coord2):
    R = 6371  # Earth radius in km
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

# --- Heuristic for A* and Greedy ---
def heuristic(city1, city2):
    return haversine(coordinates[city1], coordinates[city2])

# --- Graph Builder ---
def build_graph(adjacency, coordinates):
    graph = {}
    for city in adjacency:
        graph[city] = {}
        for neighbor in adjacency[city]:
            graph[city][neighbor] = haversine(coordinates[city], coordinates[neighbor])
    return graph

graph = build_graph(adjacency, coordinates)

# --- A* Search ---
def a_star_search(start, goal, graph, heuristic):
    frontier = [(heuristic(start, goal), 0, start, [start])]
    visited = set()

    while frontier:
        f, g, current, path = heapq.heappop(frontier)
        if current == goal:
            return path, round(g, 2)
        if current in visited:
            continue
        visited.add(current)
        for neighbor, cost in graph[current].items():
            if neighbor not in visited:
                new_g = g + cost
                new_f = new_g + heuristic(neighbor, goal)
                heapq.heappush(frontier, (new_f, new_g, neighbor, path + [neighbor]))

    return None, float("inf")

# --- Greedy Search ---
def greedy_search(start, goal, graph, heuristic):
    frontier = [(heuristic(start, goal), start, [start])]
    visited = set()

    while frontier:
        h, current, path = heapq.heappop(frontier)
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        for neighbor in graph[current]:
            if neighbor not in visited:
                heapq.heappush(frontier, (heuristic(neighbor, goal), neighbor, path + [neighbor]))

    return None

# --- Path Cost Calculator ---
def path_cost(path, graph):
    return round(sum(graph[path[i]][path[i + 1]] for i in range(len(path) - 1)), 2)

# --- Execute Searches ---
start = "Biratnagar"
goal = "Pokhara"
 
path_a_star, cost_a_star = a_star_search(start, goal, graph, heuristic)
path_greedy = greedy_search(start, goal, graph, heuristic)
cost_greedy = path_cost(path_greedy, graph) if path_greedy else None

# --- Print Results ---
print("A* Search:")
print(f" Path: {' → '.join(path_a_star)}")
print(f" Distance: {cost_a_star} km\n")

print("Greedy Best-First Search:")
if path_greedy:
    print(f" Path: {' → '.join(path_greedy)}")
    print(f" Distance: {cost_greedy} km")
else:
    print(" No path found.")

# --- Decision Logic ---
if path_a_star and path_greedy:
    if cost_a_star < cost_greedy:
        print(f"A* found a shorter path ({cost_a_star} km) than Greedy ({cost_greedy} km). A* is better.")
    elif cost_greedy < cost_a_star:
        print(f"Greedy found a shorter path ({cost_greedy} km) than A* ({cost_a_star} km). Greedy is better.")
    else:
        print("Both algorithms found equally optimal paths.")
elif path_a_star:
    print("Only A* found a valid path. A* is better.")
elif path_greedy:
    print("Only Greedy found a valid path. Greedy is better.")
else:
    print("No valid path found by either algorithm.")

# --- Map Visualization ---
m = folium.Map(location=coordinates[goal], zoom_start=7)

# Markers
for city, coord in coordinates.items():
    if city == start:
        folium.Marker(coord, tooltip=city, popup="Start", icon=folium.Icon(color="green")).add_to(m)
    elif city == goal:
        folium.Marker(coord, tooltip=city, popup="Goal", icon=folium.Icon(color="red")).add_to(m)
    else:
        folium.Marker(coord, tooltip=city, icon=folium.Icon(color="blue")).add_to(m)

# A* Path (solid green)
if path_a_star:
    folium.PolyLine([coordinates[city] for city in path_a_star],
                    color="green", weight=5, opacity=0.8, tooltip="A* Path").add_to(m)

# Greedy Path (dashed orange)
if path_greedy:
    folium.PolyLine([coordinates[city] for city in path_greedy],
                    color="orange", weight=4, opacity=0.8,
                    dash_array="10,10", tooltip="Greedy Path").add_to(m)

m.save("astar_vs_greedy_map.html")
print("Map saved as 'astar_vs_greedy_map.html'")
