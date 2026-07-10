from collections import deque
from models import Graph, ZoneType
from heapq import heappop, heappush

class PathFinder:

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
    
    def find_shortest_path(self) -> list[str]:
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
        """
        Using Dijkstra algorithm to find the cheapest path. It involves implementing heapq-
        also known as priority queue. For our project, we implement min-heap. Meaning,
        heappop() will pop the smallest element from the queue. For the records, to access left left = 2 * i
        and to access right leaf = 2*i + 1. Index starts from 1 for convenience.
        """
        
        self.graph.validate_start_end_exist()
        start: str = self.graph.start_zone
        end: str = self.graph.end_zone
        total_cost: int = 0

        queue: list[tuple[int, str]] = []
        heappush(queue, (0, start))
        distances: dict[str, int] = {start: 0}
        previous: dict[ str, str | None] = {start: None}

        while queue:
            current_cost, current_zone = heappop(queue)
            if current_zone == end:
                return self.rebuild_path(previous, end)
            

            if current_cost > distances[current_zone]: #if same route already exist but cheaper than skip this route
                continue

            for neighbor in self.graph.get_neighbors(current_zone):
                if self.graph.all_zones[neighbor].zone == ZoneType.BLOCKED:
                    continue
                
                move_cost: int = self.graph.movement_cost(neighbor)
                new_cost: int = current_cost + move_cost

                if neighbor not in distances or new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    previous[neighbor] = current_zone
                    heappush(queue, (new_cost, neighbor))
        
        raise ValueError("No Path Found!") 


    def find_multiple_paths(max_paths):
        ...


    def rebuild_path(self, previous: dict[str, str | None], end: str) -> list[str]:
        path: list[str] = []
        wokring_zone: str | None = end
        
        while wokring_zone is not None:
            path.append(wokring_zone)
            wokring_zone = previous[wokring_zone]
        path.reverse()
        return path