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
    restricted_exit_turn: int | None = None
    assigned_path: list = field(default_factory=list)


class Connections(BaseModel):
    """Connection class stores capacity and which two zons are connected. Once object is created the credentials cannot be changed(frozen!)"""
    model_config = ConfigDict(frozen=True)

    max_link_capacity: int = 1
    zone_1: str
    zone_2: str