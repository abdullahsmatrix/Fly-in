from collections import deque
from models import Graph, ZoneType


class PathFinder:

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
    
    def find_shortest_path(self) -> list[str]:
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
    
    def rebuild_path(self, previous: dict[str, str | None], end: str) -> str:
        path: list[str] = []
        current_zone: str | None = end
        
        while current_zone is not None:
            path.append(current_zone)
            current_zone = previous[current_zone]
        path.reverse()
        return path

