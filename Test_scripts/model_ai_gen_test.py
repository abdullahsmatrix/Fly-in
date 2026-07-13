"""Manual tester for Phase 1 models and Graph."""

from graph import Graph
from models import Connections, Zone, ZoneType


def test_zone_creation() -> None:
    zone = Zone(
        name="roof1",
        x_coordinate=3,
        y_coordinate=4,
        zone=ZoneType.RESTRICTED,
        color="red",
        max_drones=1,
    )

    assert zone.name == "roof1"
    assert zone.x_coordinate == 3
    assert zone.y_coordinate == 4
    assert zone.zone == ZoneType.RESTRICTED
    assert zone.color == "red"
    assert zone.max_drones == 1

    print("✅ Zone creation works")


def test_connection_creation() -> None:
    connection = Connections(
        zone_1="home",
        zone_2="roof1",
        max_link_capacity=2,
    )

    assert connection.zone_1 == "home"
    assert connection.zone_2 == "roof1"
    assert connection.max_link_capacity == 2

    print("✅ Connection creation works")


def test_graph_zone_storage() -> None:
    graph = Graph()

    graph.add_zone(Zone(name="home", x_coordinate=0, y_coordinate=0), is_start=True)
    graph.add_zone(Zone(name="goal", x_coordinate=10, y_coordinate=10), is_end=True)

    assert "home" in graph.all_zones
    assert "goal" in graph.all_zones
    assert graph.start_zone == "home"
    assert graph.end_zone == "goal"

    print("✅ Graph stores zones, start, and end correctly")


def test_graph_connections_and_neighbors() -> None:
    graph = Graph()

    graph.add_zone(Zone(name="home", x_coordinate=0, y_coordinate=0), is_start=True)
    graph.add_zone(Zone(name="roof1", x_coordinate=3, y_coordinate=4))
    graph.add_zone(Zone(name="goal", x_coordinate=10, y_coordinate=10), is_end=True)

    graph.add_connection(Connections(max_link_capacity=1, zone_1="home", zone_2="roof1"))
    graph.add_connection(Connections(max_link_capacity=1, zone_1="roof1", zone_2="goal"))

    assert "roof1" in graph.get_neighbors("home")
    assert "home" in graph.get_neighbors("roof1")
    assert "goal" in graph.get_neighbors("roof1")
    assert "roof1" in graph.get_neighbors("goal")

    print("✅ Graph connections and neighbors work")


def test_movement_costs() -> None:
    graph = Graph()

    graph.add_zone(Zone(name="home", x_coordinate=0, y_coordinate=0), is_start=True)
    graph.add_zone(Zone(name="normal_zone", x_coordinate=1, y_coordinate=1))
    graph.add_zone(Zone(name="priority_zone", x_coordinate=2, y_coordinate=2, zone=ZoneType.PRIORITY))
    graph.add_zone(Zone(name="restricted_zone", x_coordinate=3, y_coordinate=3, zone=ZoneType.RESTRICTED))
    graph.add_zone(Zone(name="blocked_zone", x_coordinate=4, y_coordinate=4, zone=ZoneType.BLOCKED))
    graph.add_zone(Zone(name="goal", x_coordinate=10, y_coordinate=10), is_end=True)

    assert graph.movement_cost("normal_zone") == 1
    assert graph.movement_cost("priority_zone") == 1
    assert graph.movement_cost("restricted_zone") == 2

    try:
        graph.movement_cost("blocked_zone")
    except ValueError:
        print("✅ Blocked zone correctly raises an error")
    else:
        raise AssertionError("Blocked zone should raise ValueError")

    print("✅ Movement costs work")


def test_duplicate_zone_error() -> None:
    graph = Graph()

    graph.add_zone(Zone(name="home", x_coordinate=0, y_coordinate=0))

    try:
        graph.add_zone(Zone(name="home", x_coordinate=1, y_coordinate=1))
    except ValueError:
        print("✅ Duplicate zone correctly raises an error")
    else:
        raise AssertionError("Duplicate zone should raise ValueError")


def test_unknown_connection_zone_error() -> None:
    graph = Graph()

    graph.add_zone(Zone(name="home", x_coordinate=0, y_coordinate=0))

    try:
        graph.add_connection(Connections(max_link_capacity=1, zone_1="home", zone_2="missing_zone"))
    except ValueError:
        print("✅ Connection to unknown zone correctly raises an error")
    else:
        raise AssertionError("Connection to unknown zone should raise ValueError")


def test_duplicate_connection_error() -> None:
    graph = Graph()

    graph.add_zone(Zone(name="home", x_coordinate=0, y_coordinate=0))
    graph.add_zone(Zone(name="roof1", x_coordinate=3, y_coordinate=4))

    graph.add_connection(Connections(max_link_capacity=1, zone_1="home", zone_2="roof1"))

    try:
        graph.add_connection(Connections(max_link_capacity=1, zone_1="roof1", zone_2="home"))
    except ValueError:
        print("✅ Duplicate reversed connection correctly raises an error")
    else:
        raise AssertionError("Duplicate reversed connection should raise ValueError")


def run_all_tests() -> None:
    test_zone_creation()
    test_connection_creation()
    test_graph_zone_storage()
    test_graph_connections_and_neighbors()
    test_movement_costs()
    test_duplicate_zone_error()
    test_unknown_connection_zone_error()
    test_duplicate_connection_error()

    print("\n🎉 All Phase 1 tests passed!")


if __name__ == "__main__":
    run_all_tests()