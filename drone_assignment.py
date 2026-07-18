from models import Drone
from graph import Graph
from pathfinding import PathFinder

class DroneAssignment:
    def __init__(self, graph: Graph, paths: list[list[str]], nb_drones: int) -> None:
        self.graph = graph
        self.path_finder = PathFinder(self.graph)
        self.paths = paths
        self.nb_drones = nb_drones
        self.drone_objects: list[Drone] = []
        self.path_usage: list[int] = [0] * len(self.paths)
    
    def build_drones(self) -> None:
        """Build and store drone objects"""
        self.drone_objects = []
        self.path_usage = [0] * len(self.paths)
        for i in range(self.nb_drones):
            drone = Drone(i, self.graph.start_zone, 0)
            self.drone_objects.append(drone)


    
    def assign_paths(self) -> None:
        """Assign paths to each drone"""

        for i in range(len(self.drone_objects)):

            best_path_index: int | None = None
            best_score = float('inf')
            for j in range(len(self.paths)):
                path_cost: int = self.path_finder.path_cost(self.paths[j])
                congestion_penalty: int = self.path_usage[j] * 3
                score: float = path_cost + congestion_penalty
                if score < best_score:
                    best_score = score
                    best_path_index = j
            
            self.drone_objects[i].assigned_path =  self.paths[best_path_index]
            self.drone_objects[i].path_index = best_path_index
            self.path_usage[best_path_index] += 1 


