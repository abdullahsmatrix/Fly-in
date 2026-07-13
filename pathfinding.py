from collections import deque
from heapq import heappop, heappush
from typing import Final

from graph import Graph
from models import ZoneType


PRIORITY_BONUS: Final[float] = 0.001
PENALTY_STEP: Final[float] = 2.0


class PathFinder:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.all_paths: list[list[str]] = []

    def find_shortest_path(self) -> list[str]:
        """Implementing BFS to experiment finding the shortest path"""
        self.graph.validate_start_end_exist()
        start: str = self.graph.start_zone
        end: str = self.graph.end_zone

        queue = deque([start])
        visited = {start}
        previous: dict[str, str | None] = {start: None}

        while queue:
            current_zone = queue.popleft()
            if current_zone == end:
                return self.rebuild_path(previous, end)

            current_zone_neighbors: list[str] = self.graph.get_neighbors(current_zone)
            for neighbor in current_zone_neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    previous[neighbor] = current_zone
                    queue.append(neighbor)

        raise ValueError("No path found!")

    def find_cheapest_path(self) -> list[str]:
        """Use Dijkstra to find the cheapest valid path."""

        self.graph.validate_start_end_exist()
        start: str = self.graph.start_zone
        end: str = self.graph.end_zone

        queue: list[tuple[float, str]] = []
        heappush(queue, (0.0, start))
        distances: dict[str, float] = {start: 0.0}
        previous: dict[str, str | None] = {start: None}

        while queue:
            current_cost, current_zone = heappop(queue)

            if current_zone == end:
                return self.rebuild_path(previous, end)

            if current_cost > distances[current_zone]:
                continue

            for neighbor in self.graph.get_neighbors(current_zone):
                neighbor_zone = self.graph.all_zones[neighbor]
                if neighbor_zone.zone == ZoneType.BLOCKED:
                    continue

                move_cost: float = float(self.graph.movement_cost(neighbor))
                if neighbor_zone.zone == ZoneType.PRIORITY:
                    move_cost -= PRIORITY_BONUS

                new_cost: float = current_cost + move_cost

                if neighbor not in distances or new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    previous[neighbor] = current_zone
                    heappush(queue, (new_cost, neighbor))

        raise ValueError("No Path Found!")

    def find_multiple_paths(self, max_paths: int = 3) -> list[list[str]]:
        """Find several candidate paths by repeatedly penalizing used routes."""

        self.graph.validate_start_end_exist()
        self.all_paths = []

        penalties: dict[str, float] = {}
        attempts: int = 0
        max_attempts: int = max_paths * max(1, len(self.graph.all_zones))

        while len(self.all_paths) < max_paths and attempts < max_attempts:
            attempts += 1

            try:
                path = self._find_penalized_path(penalties)
            except ValueError:
                break

            if path not in self.all_paths:
                self.all_paths.append(path)

            for zone_name in path[1:-1]:
                penalties[zone_name] = penalties.get(zone_name, 0.0) + PENALTY_STEP

        return self.all_paths

    def _find_penalized_path(self, penalties: dict[str, float]) -> list[str]:
        start: str = self.graph.start_zone
        end: str = self.graph.end_zone

        queue: list[tuple[float, int, str]] = []
        heappush(queue, (0.0, 0, start))
        distances: dict[str, float] = {start: 0.0}
        previous: dict[str, str | None] = {start: None}

        while queue:
            current_cost, current_hops, current_zone = heappop(queue)

            if current_zone == end:
                return self.rebuild_path(previous, end)

            if current_cost > distances[current_zone]:
                continue

            for neighbor in self.graph.get_neighbors(current_zone):
                neighbor_zone = self.graph.all_zones[neighbor]
                if neighbor_zone.zone == ZoneType.BLOCKED:
                    continue

                move_cost: float = float(self.graph.movement_cost(neighbor))
                if neighbor_zone.zone == ZoneType.PRIORITY:
                    move_cost -= PRIORITY_BONUS

                move_cost += penalties.get(neighbor, 0.0)
                new_cost: float = current_cost + move_cost

                if neighbor not in distances or new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    previous[neighbor] = current_zone
                    heappush(queue, (new_cost, current_hops + 1, neighbor))

        raise ValueError("No Path Found!")

    def path_cost(self, path: list[str]) -> int | float:
        """Calculates total cost required for moving from start to end in a path."""

        total_cost = 0
        for zone_name in path[1:]:
            total_cost += self.graph.movement_cost(zone_name)
        return total_cost

    def rebuild_path(self, previous: dict[str, str | None], end: str) -> list[str]:
        path: list[str] = []
        working_zone: str | None = end

        while working_zone is not None:
            path.append(working_zone)
            working_zone = previous[working_zone]

        path.reverse()
        return path