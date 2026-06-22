from models import Graph, Zone, Connections, ZoneType
from dataclasses import dataclass
from typing import List

class ParseError(Exception):
    """Custom Exception for parse error"""
    pass


class MapParser():
    def __init__(self) -> None:
        self.graph = Graph()
        self.nb_drones: int | None = None

    def parse_map(self, map_path: str) -> None:
        """Parse config from map"""
        try:
            with open(map_path, "r") as file:
                for line_number, raw_line in enumerate(file, 1):
                    line:str = self.clean_line(raw_line)

                    if not line:
                        continue

                    if line.startswith("nb_drones:"):
                        self.parse_first_line(line)
                    else:
                        raise ParseError("No. of drones not declared! First meaningful line must be nb_drones")

                    if line.startswith("start_hub:"):
                        zone = self.parse_zone_line(line)
                        self.graph.add_zone(zone, is_start=True)

                    elif line.startswith("hub:"):
                        zone = self.parse_zone_line(line)
                        self.graph.add_zone(zone)
                    
                    elif line.startswith("end_hub:"):
                        zone = self.parse_zone_line(line)
                        self.graph.add_zone(zone, is_end=True)
                    
                    elif line.startswith("connection:"):
                        connection = self.parse_connection(line)
                        self.graph.add_connection(connection)
                    
                    else:
                        raise ParseError(f"Line {line_number}: unknown line type")

        except FileNotFoundError as err:
            print(f"File nor found!: {err}")
        
        return self.graph

    def clean_line(self, raw_line: str):
        return raw_line.split("#", 1)[0].strip()

    def parse_first_line(self, line:str):
        
        try: 
            nb_drones: int = int(line.strip().split(": ")[1])
        except ValueError as err:
            print(f"Invalid number of drones: {nb_drones}. Expected an integer!")
        
    def parse_zone_line(self, line: str):
        zone_data: dict = {}
        if "[" in line:
            metadata: str = line.strip().split("[")[1]
            metadata: List[str] = metadata.strip("]").split(" ")
            for something in metadata:
                zone_data[something.split("=")[0]] = something.split("=")[1]
        line: str = line.strip().split(": ", 1)[1].split(" ")
        zone_data['name'] = line[0]
        zone_data['x_coordinate'] = line[1]
        zone_data['y_coordinate'] = line[2]
        return Zone(**zone_data)

    def parse_connection(self, line: str):
        connection_data = {}
        if "[" in line:
            metadata: str = line.strip().split("[")[1]
            metadata = metadata.strip("]")
            connection_data[metadata.split("=")[0]] = metadata.split("=")[1]
        
        line = line.strip().split(" ",2)[1]
        connection_data['zone_1'] = line.split("-")[0]
        connection_data['zone_2'] = line.split("-")[1]
        return Connections(**connection_data)