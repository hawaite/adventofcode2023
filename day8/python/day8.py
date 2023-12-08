import os

def main():
    cwd = os.path.dirname(__file__)
    
    with(open(f"{cwd}/../input.txt", 'r') as fp):
        all_lines = fp.readlines()

    graph = {}
    all_lines_trimmed = [x.strip() for x in all_lines]
    moves = all_lines_trimmed[0]
    graph_def = all_lines_trimmed[2:]
    start_node = "AAA"
    end_node = "ZZZ"
    for row in graph_def:
        segments = row.split(" = ")
        graph[segments[0]] = segments[1].replace("(", "").replace(")","").replace(" ", "").split(",") 

    current_node = start_node
    move_count = 0
    while current_node != end_node:
        move_to_take = moves[move_count % len(moves)]
        current_node_paths = graph[current_node]

        if move_to_take == "L":
            current_node = current_node_paths[0]
        elif move_to_take == "R":
            current_node = current_node_paths[1]

        move_count = move_count + 1

    print(f"final move count: {move_count}")

if __name__ == "__main__":
    main()