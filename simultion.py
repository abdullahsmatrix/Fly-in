from models import Drone, Zone, ZoneType, Connections
from graph import Graph

class Simulator:
    def __init__(self, drones: list[Drone], graph: Graph):
        self.active_drones = drones
        self.graph = graph
        self.current_turn = 0
        self.delivered_drones: list[Drone] = []
        self.zone_occupancy: dict[str, int] = {}
        self.connection_occupancy: dict[tuple[str, str], int] = {}

    def _connection_key(self, zone_a: str, zone_b: str) -> tuple[str, str]:
        """Create a direction-agnostic key for a bidirectional connection."""
        return tuple(sorted((zone_a, zone_b)))
    

    def initialize_occupancy(self) -> None:
        for zone in self.graph.all_zones:
            self.zone_occupancy[zone] = 0
        self.zone_occupancy[self.graph.start_zone] = len(self.active_drones)

        for connection in self.graph.all_connections:
            connection_key = self._connection_key(connection.zone_1, connection.zone_2)
            self.connection_occupancy[connection_key] = 0

    def get_next_move(self, drone: Drone) -> str:
        if drone.path_index + 1 >= len(drone.assigned_path):
            raise ValueError(f"Drone {drone.drone_id} has no next move left on assigned path")
        return drone.assigned_path[drone.path_index + 1]

    def can_move(self, drone: Drone) -> bool:
        next_zone = self.get_next_move(drone)
        connection_obj = self.graph.get_connection(drone.current_zone, next_zone)

        if self.graph.all_zones[next_zone].zone == ZoneType.BLOCKED:
            return False
        if self.zone_occupancy[next_zone] >= self.graph.all_zones[next_zone].max_drones:
            return False
        connection_key = self._connection_key(connection_obj.zone_1, connection_obj.zone_2)
        if self.connection_occupancy[connection_key] >= connection_obj.max_link_capacity:
            return False
        return True

    def move_drone(self, drone: Drone) -> None:
        next_zone = self.get_next_move(drone)
        self.zone_occupancy[drone.current_zone] -= 1
        self.zone_occupancy[next_zone] += 1
        
        connection_key = self._connection_key(drone.current_zone, next_zone)
        self.connection_occupancy[connection_key] += 1

        drone.current_zone = next_zone
        drone.path_index += 1
        
        if next_zone == self.graph.end_zone:
            self.delivered_drones.append(drone)
            self.active_drones.remove(drone)
        

    def run_turn(self) -> None:
        # Reset occupancy at start of turn
        for zone in self.graph.all_zones:
            self.zone_occupancy[zone] = 0
        for connection_key in self.connection_occupancy:
            self.connection_occupancy[connection_key] = 0
        
        # Recount drones in their current zones
        for drone in self.active_drones:
            self.zone_occupancy[drone.current_zone] += 1
        
        # Try to move each drone
        moves = []
        for drone in list(self.active_drones):  # Iterate over a copy (move_drone may remove drones)
            if self.can_move(drone):
                next_zone = self.get_next_move(drone)
                self.move_drone(drone)
                moves.append(f"D{drone.drone_id}-{next_zone}")
        
        # Output the turn
        if moves:
            print(' '.join(moves))
        
        # Increment turn counter
        self.current_turn += 1

    def run_simulation(self) -> None:
        self.initialize_occupancy()
    
        while self.active_drones:
            self.run_turn()
        print(f"All drones delivered in {self.current_turn} turns")
    

