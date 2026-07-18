from parser import MapParser
from pathfinding import PathFinder
from drone_assignment import DroneAssignment

def main():

    file_path: str = "maps/hard/01_maze_nightmare.txt"

    map_parser = MapParser(file_path)
    graph = map_parser.parse_map()
    nb_drones = map_parser.nb_drones

    path_finder = PathFinder(graph)
    paths: list[list[str]] = path_finder.find_multiple_paths()


    assigned_drones = DroneAssignment(graph, paths, nb_drones)
    assigned_drones.build_drones()

    
    print(f"{assigned_drones.drone_objects}")

if __name__ == "__main__":
    main()