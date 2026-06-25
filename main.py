from parser import MapParser
from pathfinding import PathFinder

def main():

    file_path: str = "maps/easy/01_linear_path.txt"

    map_parser = MapParser()
    graph = map_parser.parse_map(file_path)

    path_finder = PathFinder(graph)
    print(path_finder.find_shortest_path())

if __name__ == "__main__":
    main()