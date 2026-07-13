from parser import MapParser
from pathfinding import PathFinder

def main():

    file_path: str = "maps/hard/01_maze_nightmare.txt"

    map_parser = MapParser()
    graph = map_parser.parse_map(file_path)

    path_finder = PathFinder(graph)
    paths: list[str] = path_finder.find_multiple_paths()
    


if __name__ == "__main__":
    main()