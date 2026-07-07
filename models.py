from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
from pydantic import BaseModel, ConfigDict


class ZoneType(Enum):
    NORMAL="normal" #Normal zone type costs 1 turn
    RESTRICTED="restricted" #accessible but costs 2 turns
    BLOCKED = "blocked" #inaccessible zone type
    PRIORITY = "priority" #preferred zone. cost 1 turns

class Zone(BaseModel):
    """Zone class stores zone details. Once object is created the credentials cannot be changed(frozen!)"""
    model_config = ConfigDict(frozen=True)

    name: str
    x_coordinate: int
    y_coordinate: int
    zone: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = 1 


@dataclass
class Drone:
    """
    Drone object keep drone datasets. 
    field(default_factory=list) will create an empty list for each individual Drone object. 
    Without field() the list would have been shared, Error!.
    """
    drone_id: int
    current_zone: str
    path_index: int
    assigned_path: list = field(default_factory=list)


class Connections(BaseModel):
    """Connection class stores capacity and which two zons are connected. Once object is created the credentials cannot be changed(frozen!)"""
    model_config = ConfigDict(frozen=True)

    max_link_capacity: int = 1
    zone_1: str
    zone_2: str


class Graph:
    """Graph class stores all zones, all connections start zone, end zone and adjacency list
    Since we are not allowed to use networkx/graphlib.
    Parser will only read the file while Graph will understand the map.
    Graph knows what zone exist, which zones are connected, cost of mozing A to B, if the zone is blocked.
    """
    def __init__(self):
        self.all_zones: dict[str, Zone] = {}
        self.all_connections: list = []
        self.start_zone: str | None = None
        self.end_zone: str | None = None
        self.adjacency: dict[str, list[str]] = defaultdict(list)
    
    def add_zone(self, zone: Zone, is_start: bool = False, is_end: bool = False) -> None:
        if zone.name in self.all_zones:
            raise ValueError(f"Zone {zone.name} already added")
        self.all_zones[zone.name] = zone

        if is_start:
            if self.start_zone is not None:
                raise ValueError("Start zone already assigned")
            self.start_zone = zone.name
        
        if is_end:
            if self.end_zone is not None:
                raise ValueError("End zone alredy declared")
            self.end_zone = zone.name
    
    def add_connection(self, connection: Connections):
        if connection.zone_1 not in self.all_zones:
            raise ValueError(f"Unlnown zone: {connection.zone_1}")

        if connection.zone_2 not in self.all_zones:
            raise ValueError(f"Unknown zone: {connection.zone_2}")
        
        if self.connection_exist(connection):
            raise ValueError("Connection already exist")

        self.all_connections.append(connection)
        zone_1_neighbors: list[str] = self.adjacency[connection.zone_1]
        zone_1_neighbors.append(connection.zone_2)

        
        ## Dijkstra algorithm only work with undirected graphs
        zone_2_neighbors: list[str] = self.adjacency[connection.zone_2]
        zone_2_neighbors.append(connection.zone_1)

    def connection_exist(self, connection: Connections) -> bool:
        if connection.zone_2 in self.adjacency[connection.zone_1]:
            return True
        return False 
    
    def get_neighbors(self, zone_name: str) -> list[str]:
        return self.adjacency[zone_name]
    
    def movement_cost(self, destination_name: str) -> int:
        destination: Zone = self.all_zones[destination_name]
        if destination.zone == ZoneType.BLOCKED:
            raise ValueError(f"Cannot move into the blocked zone: {destination_name}")
        if destination.zone == ZoneType.RESTRICTED:
            return 2
        return 1
    
    def validate_start_end_exist(self):
        if self.start_zone is None:
            raise ValueError("Missing start_hub")

        if self.end_zone is None:
            raise ValueError("Missing end_hub")