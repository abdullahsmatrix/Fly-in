# AI Notes for Fly-in

This file stores project context for future AI/Codex sessions. Read this before giving implementation advice.

## Project

- Project name: Fly-in
- Subject PDF: `/Users/abdullah/Downloads/en.subject.pdf`
- Main task: route multiple drones through a graph of connected zones while respecting movement, occupancy, capacity, scheduling, and output constraints.
- Current working directory: `/Users/abdullah/Desktop/42 WAW/Core Carriculum/Fly-in`

## Current Phase

The project is currently around Phase 3: simple pathfinding.

Planned phases:

1. Models + Graph
2. Parser
3. Pathfinding
4. Weighted Pathfinding
5. Multiple Paths
6. Simulation
7. Capacity Rules
8. Scheduling
9. Output + Visuals
10. Optimization + README

## Existing Structure

- `models.py`
  - Contains `ZoneType`, `Zone`, `Drone`, `Connections`, and `Graph`.
  - `Graph` stores zones, connections, start/end zones, and an adjacency list.
- `parser.py`
  - Contains `MapParser`.
  - Reads map files and builds a `Graph`.
  - Stores `nb_drones` separately from `Graph`.
- `pathfinding.py`
  - Contains `PathFinder`.
  - Intended to implement BFS for Phase 3.

## Important Design Notes

- `Graph` and `MapParser` should remain separate classes.
  - `Graph` represents the parsed map in memory.
  - `MapParser` reads a file and builds a graph.
- `nb_drones` is simulation/config data, not graph data.
- The parser can temporarily own parsing state, but the rest of the program should mainly use the returned `Graph`.

## Graph / Adjacency

`Graph.adjacency` is a dictionary mapping a zone name to the list of directly connected neighboring zones.

Example:

```python
{
    "hub": ["roof1", "roof2"],
    "roof1": ["hub", "goal"],
    "goal": ["roof1"],
}
```

Connections in the subject are bidirectional. Therefore, when adding a connection `A-B`, both directions must be stored:

```python
self.adjacency["A"].append("B")
self.adjacency["B"].append("A")
```

Good temporary variable names in `add_connection`:

```python
zone_1_neighbors = self.adjacency[connection.zone_1]
zone_2_neighbors = self.adjacency[connection.zone_2]
```

## Pathfinding Phase 3

For Phase 3, keep pathfinding simple:

- Ignore restricted zones.
- Ignore priority zones.
- Ignore blocked zones.
- Ignore capacities.
- Ignore multiple drones.
- Find one valid route from `start_zone` to `end_zone`.

Use BFS because the graph is currently unweighted. BFS finds the shortest path by number of connections.

Core BFS state:

- `queue`: zones waiting to be explored.
- `visited`: zones already discovered.
- `previous`: maps each discovered zone to the zone it came from, so the final path can be rebuilt.

Expected behavior:

- Call `graph.validate_start_end_exist()` before using `start_zone` and `end_zone`.
- Return `list[str]` for the path.
- Raise `ValueError` if no path exists.

Useful shape:

```python
def find_shortest_path(self) -> list[str]:
    self.graph.validate_start_end_exist()

    start = self.graph.start_zone
    end = self.graph.end_zone

    queue = deque([start])
    visited = {start}
    previous: dict[str, str | None] = {start: None}

    while queue:
        current_zone = queue.popleft()

        if current_zone == end:
            return self.rebuild_path(previous, end)

        for neighbor in self.graph.get_neighbors(current_zone):
            if neighbor not in visited:
                visited.add(neighbor)
                previous[neighbor] = current_zone
                queue.append(neighbor)

    raise ValueError("No path found from start to end")
```

`rebuild_path` should return `list[str]`, not `str`.

## Subject Requirements Already Noted

- `normal`: movement cost 1.
- `restricted`: movement cost 2.
- `blocked`: inaccessible; drones must not enter or pass through.
- `priority`: movement cost 1, but should be preferred in pathfinding.
- `connection: <name1>-<name2> [metadata]` defines a bidirectional edge.
- Zone names cannot contain dashes because dashes separate connection endpoints.

## Collaboration Preference

The user is learning and wants explanations while building the project step by step.

- Do not jump too far ahead unless asked.
- Prefer conceptual explanations tied to the current phase.
- Avoid making code changes unless explicitly requested.
- When reviewing code, point out type issues, missing edge cases, and project-alignment problems clearly.
