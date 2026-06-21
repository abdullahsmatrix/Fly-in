from models import Graph, Zone, Connections, ZoneType


class ParseError(Exception):
    """Custom Exception for parse error"""
    pass

class ParseMap():
    def __init__(self) -> None:
        self.graph = Graph()
        self.nb_drones: int | None = None
        self.first_meaningful_line_seen = False

    def parse_map(self, map_path: str) -> None:
        """Parse config from map"""
        raw_data:dict = {}

        try:
            with open(map_path, "r") as f:
                for line_number, line in enumerate(f, 1):
                    if not line or line.startswith("#"):
                        continue
                    if not self.first_meaningful_line_seen:
                        if not line.startswith("nb_drones:"):
                            raise ParseError("No. of drones not declared! First meaningful line must be nb_drones")
                    
                    if line.startswith("nb_drones:"):
                        nb_drones: list = line.split(":")
                        self.nb_drones = int(nb_drones[1].strip())
                        self.first_meaningful_line_seen = True

                    if line.startswith("start_hub:"):
                        start_zone: str = line.split("[")[0]
                        metadata: str = line.split("[")[1]
                        self.graph.add_zone(self.parse_zone_metadata(start_zone, metadata))
                    
                    if line.startswith("hub:"):
                        zone: str = line.split("[")[0]
                        metadata: str = line.split("[")[1]
                        self.graph.add_zone(self.parse_zone_metadata(zone, metadata))
                    
                    if line.startswith("end_hub:"):
                        end_zone: str = line.split("[")[0]
                        metadata: str = line.split("[")[1]
                        self.graph.add_zone(self.parse_zone_metadata(end_zone, metadata))
                    
                    if line.startswith("connection:"):
                        line = line.strip(" ]")
                        connection: str = line.split("[")[0].strip()
                        zone_1: str = connection.split("-")[0]
                        zone_2: str = connection.split("-")[1]
                        max_link_capacity = line.split("[")[1]
                        self.graph.add_connection(Connections(max_link_capacity, zone_1, zone_2))
        except FileNotFoundError as err:
            print(f"File nor found!: {err}")

    def parse_zone_metadata(self, splitted_string: str, metadata: str) -> Zone:
        splitted_string = splitted_string.strip()
        splitted_string = splitted_string.split(" ")

        metadata = metadata.strip(" ]")
        metadata = metadata.split(" ")
        metadata_dict: dict = {}
        
        for metadatas in metadata:
            metadata_dict[metadatas.split("=")[0]] = metadatas.split("=")[1]


        data: dict = {}
        data["name"] = splitted_string[1]
        data["x_coordinate"] = int(splitted_string[2])
        data["y_coordinate"] = int(splitted_string[3])
        if "zone" in metadata_dict:
            try:
                data["zone_type"] = ZoneType.metadata_dict["zone"].upper()
            except AttributeError as err:
                print("Invalid zone type!")
        if "color" in metadata_dict:
            data["color"] = metadata_dict["color"]
        if "max_drones" in metadata_dict:
            data["max_drones"] = metadata_dict["max_drones"]
        
        return Zone(**metadata_dict)


def parse_map(path: str) -> None:
    parser = MapParser()
    return parser.graph