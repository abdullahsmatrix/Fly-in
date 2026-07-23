from typing import Any

from graph import Graph
from models import Connections, Zone, ZoneType


class ParseError(Exception):
    """Custom Exception for parse error"""
    pass


class MapParser:
    """Parse and validate Fly-in map files."""

    def __init__(self, path: str) -> None:
        self.path = path
        self.graph = Graph()
        self.nb_drones: int | None = None
        self.connection_keys: set[tuple[str, str]] = set()

    def parse_map(self) -> Graph:
        """Parse config from map"""
        first_line_checked: bool = False
        try:
            with open(self.path, "r") as file:
                for line_number, raw_line in enumerate(file, 1):
                    line: str = self.clean_line(raw_line)

                    if not line:
                        continue

                    if not first_line_checked:
                        if not line.startswith("nb_drones:"):
                            raise ParseError(
                                f"Line {line_number}: first meaningful line "
                                "must be nb_drones"
                            )
                        self.parse_first_line(line, line_number)
                        first_line_checked = True
                        continue

                    if line.startswith("start_hub:"):
                        zone = self.parse_zone_line(
                            line, line_number, is_start_or_end=True
                        )
                        self.add_zone_or_raise(
                            zone, line_number, is_start=True
                        )

                    elif line.startswith("hub:"):
                        zone = self.parse_zone_line(line, line_number)
                        self.add_zone_or_raise(zone, line_number)

                    elif line.startswith("end_hub:"):
                        zone = self.parse_zone_line(
                            line, line_number, is_start_or_end=True
                        )
                        self.add_zone_or_raise(zone, line_number, is_end=True)

                    elif line.startswith("connection:"):
                        connection = self.parse_connection(line, line_number)
                        self.add_connection_or_raise(connection, line_number)

                    else:
                        raise ParseError(
                            f"Line {line_number}: unknown line type"
                        )

        except FileNotFoundError as err:
            raise ParseError(f"Could not open map file: {err}") from err

        if not first_line_checked:
            raise ParseError("Line EOF: missing nb_drones")

        try:
            self.graph.validate_start_end_exist()
        except ValueError as err:
            raise ParseError(f"Line EOF: {err}") from err
        
        if not self.graph.is_connected():
            raise ParseError("No valid path exist from start zone to end!")

        return self.graph

    def clean_line(self, raw_line: str) -> str:
        return raw_line.split("#", 1)[0].strip()

    def parse_first_line(self, line: str, line_number: int) -> None:
        if line.count(":") != 1:
            raise ParseError(
                f"Line {line_number}: nb_drones must use "
                "'nb_drones: <positive_integer>'"
            )

        key = line.split(":", 1)[0].strip()
        if key != "nb_drones":
            raise ParseError(f"Line {line_number}: expected nb_drones")

        value = line.split(":", 1)[1].strip()
        if not value:
            raise ParseError(f"Line {line_number}: nb_drones value is missing")

        self.nb_drones = self.parse_positive_int(
            value, "nb_drones", line_number
        )

    def parse_zone_line(
        self,
        line: str,
        line_number: int,
        is_start_or_end: bool = False,
    ) -> Zone:
    
        body, metadata = self.split_metadata(line, line_number)
        zone_data: dict[str, Any] = {}

        if ":" not in body:
            raise ParseError(f"Line {line_number}: zone line is missing ':'")

        zone_parts = body.split(":", 1)[1].strip().split()
        if len(zone_parts) != 3:
            raise ParseError(
                f"Line {line_number}: zone must use '<name> <x> <y>'"
            )

        name, x_value, y_value = zone_parts
        self.validate_zone_name(name, line_number)

        zone_data["name"] = name
        zone_data["x_coordinate"] = self.parse_int(
            x_value, "x coordinate", line_number
        )
        zone_data["y_coordinate"] = self.parse_int(
            y_value, "y coordinate", line_number
        )

        self.validate_metadata_keys(
            metadata, {"zone", "color", "max_drones"}, line_number
        )

        if "zone" in metadata:
            try:
                zone_data["zone"] = ZoneType(metadata["zone"])
            except ValueError as err:
                raise ParseError(
                    f"Line {line_number}: invalid zone type "
                    f"'{metadata['zone']}'"
                ) from err

        if "color" in metadata:
            if not metadata["color"]:
                raise ParseError(f"Line {line_number}: color value is missing")
            zone_data["color"] = metadata["color"]

        if "max_drones" in metadata:
            zone_data["max_drones"] = self.parse_positive_int(
                metadata["max_drones"], "max_drones", line_number
            )

        return Zone(**zone_data)

    def parse_connection(self, line: str, line_number: int) -> Connections:
        body, metadata = self.split_metadata(line, line_number)
        self.validate_metadata_keys(
            metadata, {"max_link_capacity"}, line_number
        )

        if ":" not in body:
            raise ParseError(
                f"Line {line_number}: connection line is missing ':'"
            )

        connection_text = body.split(":", 1)[1].strip()
        if not connection_text:
            raise ParseError(
                f"Line {line_number}: connection value is missing"
            )

        if len(connection_text.split()) != 1:
            raise ParseError(
                f"Line {line_number}: connection must use '<zone1>-<zone2>'"
            )

        if connection_text.count("-") != 1:
            raise ParseError(
                f"Line {line_number}: connection must contain exactly one '-'"
            )

        zone_1, zone_2 = connection_text.split("-", 1)
        self.validate_zone_name(zone_1, line_number)
        self.validate_zone_name(zone_2, line_number)

        if zone_1 == zone_2:
            raise ParseError(
                f"Line {line_number}: connection cannot link a zone to itself"
            )

        if zone_1 not in self.graph.all_zones:
            raise ParseError(f"Line {line_number}: unknown zone '{zone_1}'")

        if zone_2 not in self.graph.all_zones:
            raise ParseError(f"Line {line_number}: unknown zone '{zone_2}'")

        connection_data: dict[str, Any] = {
            "zone_1": zone_1,
            "zone_2": zone_2,
        }
        if "max_link_capacity" in metadata:
            connection_data["max_link_capacity"] = self.parse_positive_int(
                metadata["max_link_capacity"],
                "max_link_capacity",
                line_number,
            )

        return Connections(**connection_data)

    def split_metadata(
        self, line: str, line_number: int
    ) -> tuple[str, dict[str, str]]:
        if "[" not in line and "]" not in line:
            return line, {}

        if line.count("[") != 1 or line.count("]") != 1:
            raise ParseError(
                f"Line {line_number}: metadata must use one '[...]' block"
            )

        start = line.index("[")
        end = line.index("]")
        if end < start:
            raise ParseError(f"Line {line_number}: malformed metadata block")

        trailing = line[end + 1:].strip()
        if trailing:
            raise ParseError(
                f"Line {line_number}: unexpected text after metadata"
            )

        metadata_text = line[start + 1:end].strip()
        if not metadata_text:
            raise ParseError(f"Line {line_number}: empty metadata block")

        metadata: dict[str, str] = {}
        for token in metadata_text.split():
            if token.count("=") != 1:
                raise ParseError(
                    f"Line {line_number}: invalid metadata token '{token}'"
                )

            key, value = token.split("=", 1)
            if not key or not value:
                raise ParseError(
                    f"Line {line_number}: invalid metadata token '{token}'"
                )

            if key in metadata:
                raise ParseError(
                    f"Line {line_number}: duplicate metadata key '{key}'"
                )

            metadata[key] = value

        return line[:start].strip(), metadata

    def validate_metadata_keys(
        self,
        metadata: dict[str, str],
        allowed_keys: set[str],
        line_number: int,
    ) -> None:
        for key in metadata:
            if key not in allowed_keys:
                raise ParseError(
                    f"Line {line_number}: unknown metadata key '{key}'"
                )

    def validate_zone_name(self, name: str, line_number: int) -> None:
        if not name:
            raise ParseError(f"Line {line_number}: zone name is missing")

        if "-" in name:
            raise ParseError(
                f"Line {line_number}: zone names cannot contain dashes"
            )

        if any(character.isspace() for character in name):
            raise ParseError(
                f"Line {line_number}: zone names cannot contain spaces"
            )

    def parse_int(self, value: str, label: str, line_number: int) -> int:
        try:
            return int(value)
        except ValueError as err:
            raise ParseError(
                f"Line {line_number}: {label} must be an integer"
            ) from err

    def parse_positive_int(
        self, value: str, label: str, line_number: int
    ) -> int:
        parsed_value = self.parse_int(value, label, line_number)
        if parsed_value <= 0:
            raise ParseError(
                f"Line {line_number}: {label} must be a positive integer"
            )
        return parsed_value

    def add_zone_or_raise(
        self,
        zone: Zone,
        line_number: int,
        is_start: bool = False,
        is_end: bool = False,
    ) -> None:
        try:
            self.graph.add_zone(zone, is_start=is_start, is_end=is_end)
        except ValueError as err:
            raise ParseError(f"Line {line_number}: {err}") from err

    def add_connection_or_raise(
        self, connection: Connections, line_number: int
    ) -> None:
        connection_key = tuple(sorted((connection.zone_1, connection.zone_2)))
        if connection_key in self.connection_keys:
            raise ParseError(
                f"Line {line_number}: duplicate connection "
                f"'{connection.zone_1}-{connection.zone_2}'"
            )

        try:
            self.graph.add_connection(connection)
        except ValueError as err:
            raise ParseError(f"Line {line_number}: {err}") from err

        self.connection_keys.add(connection_key)
