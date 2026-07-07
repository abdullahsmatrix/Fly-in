from models import Graph, Connections, Zone, ZoneType

def main():
    home = Zone("home", 0, 0)
    roof1 = Zone("roof1", 3, 4, "restricted")
    roof2 = Zone("roof2", 5, 7, max_drones=2)
    goal = Zone("goal", 10, 10)
    corridorA = Zone("corridorA", 2, 6, "blocked")

    home_roof = Connections(1, "home", "roof1")
    roof_roof2 = Connections(1, "roof1", "roof2")
    roof2_goal = Connections(1, "roof2", "goal")
    home_corridorA = Connections(1, "home", "corridorA")
    corridorA_home = Connections(1, "corridorA", "goal")

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

    print(graph.get_neighhbors("roof1"))
    print(graph.movement_cost("roof1"))
    print(graph.get_neighhbors("home"))
    print(graph.movement_cost("home"))
    print(graph.get_neighhbors("roof2"))
    print(graph.movement_cost("roof2"))
    print(graph.get_neighhbors("corridorA"))
    print(graph.movement_cost("corridorA"))
    print(graph.get_neighhbors("goal"))
    print(graph.movement_cost("goal"))
if __name__ == "__main__":
    main()