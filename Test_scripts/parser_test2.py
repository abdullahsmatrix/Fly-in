"""Parser test for Hard Level 1 map."""

from pathlib import Path

from parser import MapParser
from models import ZoneType


MAP_TEXT = """
# Hard Level 1: Complex maze with multiple dead ends and loops
nb_drones: 8

start_hub: start 0 0 [color=green max_drones=8]
hub: maze_a1 1 0 [color=blue max_drones=2]
hub: maze_a2 2 0 [color=blue]
hub: maze_b1 1 1 [color=blue]
hub: maze_b2 2 1 [color=blue max_drones=2]
hub: maze_c1 1 2 [color=blue]
hub: maze_c2 3 1 [color=blue max_drones=2]
hub: dead_end1 0 1 [color=red max_drones=2]
hub: dead_end2 0 2 [color=red]
hub: dead_end3 2 -1 [color=red]
hub: trap_loop1 4 0 [zone=restricted color=orange]
hub: trap_loop2 4 2 [zone=restricted color=orange]
hub: bottleneck 5 1 [color=yellow max_drones=2]
hub: final_stretch1 6 0 [zone=priority color=cyan]
hub: final_stretch2 6 1 [zone=priority color=cyan]
hub: final_stretch3 6 2 [zone=priority color=cyan]
end_hub: goal 7 1 [color=green max_drones=8]

connection: start-maze_a1 [max_link_capacity=2]
connection: maze_a1-maze_a2
connection: maze_a1-maze_b1
connection: maze_b1-maze_b2
connection: maze_b2-maze_c2
connection: maze_c2-maze_a2
connection: maze_c2-bottleneck
connection: start-dead_end1 [max_link_capacity=2]
connection: dead_end1-dead_end2
connection: maze_a2-dead_end3
connection: maze_a2-trap_loop1
connection: trap_loop1-trap_loop2
connection: trap_loop2-maze_c1
connection: maze_b1-maze_c1
connection: maze_c1-maze_b2
connection: maze_b2-maze_a2
connection: bottleneck-final_stretch1
connection: bottleneck-final_stretch2
connection: bottleneck-final_stretch3
connection: final_stretch1-goal
connection: final_stretch2-goal
connection: final_stretch3-goal
"""


def test_hard_level_1_parser() -> None:
    path = Path("hard_level_1_test.map")
    path.write_text(MAP_TEXT.strip() + "\n")

    parser = MapParser()
    graph = parser.parse_map(str(path))

    assert parser.nb_drones == 8

    assert graph.start_zone == "start"
    assert graph.end_zone == "goal"

    assert len(graph.all_zones) == 17
    assert len(graph.all_connections) == 22

    assert graph.all_zones["start"].max_drones == 8
    assert graph.all_zones["maze_a1"].max_drones == 2
    assert graph.all_zones["bottleneck"].max_drones == 2
    assert graph.all_zones["goal"].max_drones == 8

    assert graph.all_zones["trap_loop1"].zone == ZoneType.RESTRICTED
    assert graph.all_zones["trap_loop2"].zone == ZoneType.RESTRICTED

    assert graph.all_zones["final_stretch1"].zone == ZoneType.PRIORITY
    assert graph.all_zones["final_stretch2"].zone == ZoneType.PRIORITY
    assert graph.all_zones["final_stretch3"].zone == ZoneType.PRIORITY

    assert graph.movement_cost("trap_loop1") == 2
    assert graph.movement_cost("final_stretch1") == 1

    assert "maze_a1" in graph.get_neighbors("start")
    assert "dead_end1" in graph.get_neighbors("start")
    assert "bottleneck" in graph.get_neighbors("maze_c2")
    assert "goal" in graph.get_neighbors("final_stretch1")
    assert "goal" in graph.get_neighbors("final_stretch2")
    assert "goal" in graph.get_neighbors("final_stretch3")

    first_connection = graph.all_connections[0]
    assert first_connection.zone_1 == "start"
    assert first_connection.zone_2 == "maze_a1"
    assert first_connection.max_link_capacity == 2

    print("✅ Hard Level 1 parser test passed!")


if __name__ == "__main__":
    test_hard_level_1_parser()