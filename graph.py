from collections import defaultdict

from models import Connections, Zone, ZoneType


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
        """Adds a zone to the list"""
        
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
        """ Adds connection to the connections list"""
        
        if connection.zone_1 not in self.all_zones:
            raise ValueError(f"Unlnown zone: {connection.zone_1}")

        if connection.zone_2 not in self.all_zones:
            raise ValueError(f"Unknown zone: {connection.zone_2}")
        
        if self.connection_exist(connection):
            raise ValueError("Connection already exist")

        self.all_connections.append(connection)
        zone_1_neighbors: list[str] = self.adjacency[connection.zone_1]
        zone_1_neighbors.append(connection.zone_2)

        
        zone_2_neighbors: list[str] = self.adjacency[connection.zone_2]
        zone_2_neighbors.append(connection.zone_1)

    def connection_exist(self, connection: Connections) -> bool:
        if connection.zone_2 in self.adjacency[connection.zone_1]:
            return True
        return False 
    
    def get_neighbors(self, zone_name: str) -> list[str]:
        return self.adjacency[zone_name]
    
    def get_connection(self, zone_a:str, zone_b:str):
        """Returns the connection object between two zones.
    
        Args:
            zone_1: Name of the first zone
            zone_2: Name of the second zone

        Returns:
            Connections object if connection exists

        Raises:
            ValueError: If no connection exists between the zones
        """
        
        for connection in self.all_connections:
            if(connection.zone_1 == zone_a and connection.zone_2 == zone_b) or\
              (connection.zone_2 == zone_a and connection.zone_1 == zone_b):
                return connection
        
        raise ValueError(f"No Conenction exist! between {zone_a} and {zone_b}")

    def movement_cost(self, destination_name: str) -> int | float:
        """Returns movement cost from a point to destination. 0.9 on priority
        since it will automatically return lower cost and that path is considered priority
        """

        destination: Zone = self.all_zones[destination_name]
        if destination.zone == ZoneType.BLOCKED:
            raise ValueError(f"Cannot move into the blocked zone: {destination_name}")
        if destination.zone == ZoneType.RESTRICTED:
            return 2
        elif destination.zone == ZoneType.PRIORITY:
            return 1
        return 1
    
    def validate_start_end_exist(self):
        if self.start_zone is None:
            raise ValueError("Missing start_hub")

        if self.end_zone is None:
            raise ValueError("Missing end_hub")