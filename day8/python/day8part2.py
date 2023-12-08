import os
import math

def all_current_nodes_end_in_z(positionList):
    for pos in positionList:
        if pos[-1] != "Z":
            return False
    return True

def get_path_length_to_z(start_node, graph, move_list):
    move_count = 0
    current_node = start_node
    
    #do
    move_to_take = move_list[move_count % len(move_list)]
    current_node_paths = graph[current_node]
    
    if move_to_take == "L":
        current_node = current_node_paths[0]
    elif move_to_take == "R":
        current_node = current_node_paths[1]

    move_count = move_count + 1

    # while
    while(current_node[-1] != 'Z'):
        move_to_take = move_list[move_count % len(move_list)]
        current_node_paths = graph[current_node]
        
        if move_to_take == "L":
            current_node = current_node_paths[0]
        elif move_to_take == "R":
            current_node = current_node_paths[1]

        move_count = move_count + 1

    print(f"Got a path to {current_node} in {move_count} moves")
    return move_count


def main():
    cwd = os.path.dirname(__file__)
    
    with(open(f"{cwd}/../input.txt", 'r') as fp):
        all_lines = fp.readlines()

    graph = {}
    all_lines_trimmed = [x.strip() for x in all_lines]
    moves = all_lines_trimmed[0]
    graph_def = all_lines_trimmed[2:]
    start_nodes = []
    for row in graph_def:
        segments = row.split(" = ")
        graph[segments[0]] = segments[1].replace("(", "").replace(")","").replace(" ", "").split(",") 
        if segments[0][-1] == "A":
            start_nodes.append(segments[0])

    print(start_nodes)
    print(len(start_nodes))

    # solution only really works because all start nodes are on cycles in the graph with only 1 node ending in Z
    # means you can find out what the distance is from the start node to the single Z-ending node
    # then use LCM to get the lowest distance number common to all path lengths
    path_lengths = list(map(lambda x: get_path_length_to_z(x,graph,moves), start_nodes))
    print(f"min path length list: {path_lengths}")
    print(f"lcm: {math.lcm(*path_lengths)}")

if __name__ == "__main__":
    main()