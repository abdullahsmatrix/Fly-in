from graph import Graph
from models import Connections, Zone, ZoneType

def main():
    home = Zone(name="home", x_coordinate=0, y_coordinate=0)
    roof1 = Zone(name="roof1", x_coordinate=3, y_coordinate=4, zone=ZoneType.RESTRICTED)
    roof2 = Zone(name="roof2", x_coordinate=5, y_coordinate=7, max_drones=2)
    goal = Zone(name="goal", x_coordinate=10, y_coordinate=10)
    corridorA = Zone(name="corridorA", x_coordinate=2, y_coordinate=6, zone=ZoneType.BLOCKED)

    home_roof = Connections(max_link_capacity=1, zone_1="home", zone_2="roof1")
    roof_roof2 = Connections(max_link_capacity=1, zone_1="roof1", zone_2="roof2")
    roof2_goal = Connections(max_link_capacity=1, zone_1="roof2", zone_2="goal")
    home_corridorA = Connections(max_link_capacity=1, zone_1="home", zone_2="corridorA")
    corridorA_home = Connections(max_link_capacity=1, zone_1="corridorA", zone_2="goal")

    graph = Graph()
    graph.add_zone(home, is_start=True)
    graph.add_zone(roof1)
    graph.add_zone(roof2)
    graph.add_zone(corridorA)
    graph.add_zone(goal, is_end=True)

    graph.add_connection(home_roof)
    graph.add_connection(roof_roof2)
    graph.add_connection(roof2_goal)
    graph.add_connection(home_corridorA)
    graph.add_connection(corridorA_home)

    print(graph.get_neighbors("roof1"))
    print(graph.movement_cost("roof1"))
    print(graph.get_neighbors("home"))
    print(graph.movement_cost("home"))
    print(graph.get_neighbors("roof2"))
    print(graph.movement_cost("roof2"))
    print(graph.get_neighbors("corridorA"))
    try:
        print(graph.movement_cost("corridorA"))
    except ValueError:
        print("blocked zone correctly raises ValueError")
    print(graph.get_neighbors("goal"))
    print(graph.movement_cost("goal"))
if __name__ == "__main__":
    main()