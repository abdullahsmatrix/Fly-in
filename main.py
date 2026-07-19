from parser import MapParser
from pathfinding import PathFinder
from drone_assignment import DroneAssignment
from simultion import Simulator

def main():

    file_path: str = "maps/challenger/01_the_impossible_dream.txt"

    map_parser = MapParser(file_path)
    graph = map_parser.parse_map()
    nb_drones = map_parser.nb_drones

    path_finder = PathFinder(graph)
    paths: list[list[str]] = path_finder.find_multiple_paths()

    assigned_drones = DroneAssignment(graph, paths, nb_drones)
    assigned_drones.build_drones()
    assigned_drones.assign_paths()

    # Create simulator and run
    simulator = Simulator(assigned_drones.drone_objects, graph)
    simulator.run_simulation()

if __name__ == "__main__":
    main()