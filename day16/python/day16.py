from enum import Enum
import os
import sys

class Direction(Enum):
    LEFT = 0,
    RIGHT = 1,
    UP = 2,
    DOWN = 3

def get_reflect_direction(mirror, incoming_direction):
    if(mirror == '\\'):
        if incoming_direction == Direction.LEFT:
            return Direction.UP
        if incoming_direction == Direction.RIGHT:
            return Direction.DOWN
        if incoming_direction == Direction.UP:
            return Direction.LEFT
        if incoming_direction == Direction.DOWN:
            return Direction.RIGHT
    elif( mirror == '/'):
        if incoming_direction == Direction.LEFT:
            return Direction.DOWN
        if incoming_direction == Direction.RIGHT:
            return Direction.UP
        if incoming_direction == Direction.UP:
            return Direction.RIGHT
        if incoming_direction == Direction.DOWN:
            return Direction.LEFT

def get_new_posiiton(row, col, direction):
    if(direction == Direction.LEFT):
        row = row
        col = col - 1
    elif(direction == Direction.RIGHT):
        row = row
        col = col + 1
    elif(direction == Direction.UP):
        row = row - 1
        col = col
    elif(direction == Direction.DOWN):
        row = row + 1
        col = col

    return (row,col)

def solve_rec(current_row, current_col, beam_direction, lines, seen_beam_direction_map):
    rows = len(lines)
    cols = len(lines[0])

    # input args are current position and beam pointing direction.
    # need to work out the next coordinate and what direction beam will face when there

    if(beam_direction in seen_beam_direction_map[current_row][current_col]):
        # a beam on a square will ALWAYS follow the same path it did the first time if travelling same direction
        # so we can bail immediately if we have landed on this square, from this direction before
        return

    # store the direction we came in to this square
    seen_beam_direction_map[current_row][current_col].append(beam_direction)

    # must be a list as sometimes we split the beam and there are two to process
    beams_to_process = []

    if(lines[current_row][current_col] == '.'):
        updated_row, updated_col = get_new_posiiton(current_row, current_col, beam_direction)
        beams_to_process.append((updated_row,updated_col,beam_direction))
        # check if we hit a wall
    elif(lines[current_row][current_col] in "\\/"):
        new_beam_direction = get_reflect_direction(lines[current_row][current_col], beam_direction)
        updated_row, updated_col = get_new_posiiton(current_row, current_col, new_beam_direction)
        beams_to_process.append((updated_row,updated_col,new_beam_direction))
    elif lines[current_row][current_col] in "-|":
        if(lines[current_row][current_col] == '-' and beam_direction in [Direction.LEFT, Direction.RIGHT]):
            # straight through '-'
            updated_row, updated_col = get_new_posiiton(current_row, current_col, beam_direction)
            beams_to_process.append((updated_row,updated_col,beam_direction))
        elif(lines[current_row][current_col] == '|' and beam_direction in [Direction.UP, Direction.DOWN]):
            # straight through '|'
            updated_row, updated_col = get_new_posiiton(current_row, current_col, beam_direction)
            beams_to_process.append((updated_row,updated_col,beam_direction))
        elif(lines[current_row][current_col] == '-' and beam_direction in [Direction.UP, Direction.DOWN]):
            # hitting '-' side-on
            # doesnt matter what incoming direction was because outgoing is alway left AND right
            updated_left_row, updated_left_col = get_new_posiiton(current_row, current_col, Direction.LEFT)
            updated_right_row, updated_right_col = get_new_posiiton(current_row, current_col, Direction.RIGHT)

            beams_to_process.append((updated_left_row,updated_left_col,Direction.LEFT))
            beams_to_process.append((updated_right_row,updated_right_col,Direction.RIGHT))
        elif(lines[current_row][current_col] == '|' and beam_direction in [Direction.LEFT, Direction.RIGHT]):
            # hitting '|' side-on
            # doesnt matter what incoming direction was because outgoing is always up AND DOWN
            updated_up_row, updated_up_col = get_new_posiiton(current_row, current_col, Direction.UP)
            updated_down_row, updated_down_col = get_new_posiiton(current_row, current_col, Direction.DOWN)

            beams_to_process.append((updated_up_row,updated_up_col,Direction.UP))
            beams_to_process.append((updated_down_row,updated_down_col,Direction.DOWN))

    for beam_def in beams_to_process:
        # check for hitting a wall
        if (beam_def[1] < 0 or beam_def[1] >= cols or beam_def[0] < 0 or beam_def[0] >= rows):
            pass # new location would be outside the bounds. end current beam here
        else:
            # didnt hit anything, can continue
            solve_rec(beam_def[0], beam_def[1], beam_def[2], lines, seen_beam_direction_map)

def build_blank_seen_transitions_map(row_count, col_count):
    seen_transitions_map = []
    for i in range(0,row_count):
        seen_transitions_map.append([])
        for j in range(0,col_count):
            seen_transitions_map[i].append([])
    return seen_transitions_map

def count_energized_in_seen_transitions_map(seen_transitions_map):
    count = 0
    for seen_map_row in seen_transitions_map:
        for cell in seen_map_row:
            if cell != []:
                count+=1
    return count

def main():
    part_two = True
    # need slightly more recursion limit than standard
    sys.setrecursionlimit(10000)

    cwd = os.path.dirname(__file__)
    with(open(f"{cwd}/../input.txt", 'r') as fp):
        all_lines = fp.readlines()
    all_lines_trimmed = [x.strip() for x in all_lines]

    starting_positions = []
    row_count = len(all_lines_trimmed)
    col_count = len(all_lines_trimmed[0])

    if(part_two == False):
        starting_positions.append((0,0,Direction.RIGHT))
    else:
        for i in range(0, row_count):
            #add all row-aligned items
            starting_positions.extend([(i, 0, Direction.RIGHT), (i, col_count - 1, Direction.LEFT)])
            
        for i in range(0, col_count):
            #add all col-aligned items
            starting_positions.extend([(0, i, Direction.DOWN), (row_count - 1, i, Direction.UP)])

    best_count = 0
    for starting_position in starting_positions:
        # new blank transition map each time
        seen_transitions_map = build_blank_seen_transitions_map(row_count, col_count)

        # complete the transition map
        solve_rec(starting_position[0], starting_position[1], starting_position[2], all_lines_trimmed, seen_transitions_map)

        # count the non-empty cells in the transition map
        count = count_energized_in_seen_transitions_map(seen_transitions_map)
        
        if(count > best_count):
            best_count = count

    print(f"best count: {best_count}")

if __name__ == "__main__":
    main()