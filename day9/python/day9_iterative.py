import os

def generate_initial_number_list(numbers_str):
    # init
    numbers = numbers_str.split(" ")
    numbers = [int(x) for x in numbers]
    generated_lines = []
    generated_lines.append(numbers)

    # do
    generated_next_line = generate_next_number_list(numbers)
    generated_lines.append(generated_next_line)

    # while
    while( not line_is_all_zeros(generated_next_line) ):
        generated_next_line = generate_next_number_list(generated_next_line)
        generated_lines.append(generated_next_line)

    return generated_lines

def generate_next_number_list(number_list):
    generated_list = []
    for i in range(0,len(number_list) - 1):
        generated_list.append(number_list[i+1] - number_list[i])

    return generated_list

def line_is_all_zeros(numbers_list):
    numbers_list_as_set = set(numbers_list)
    if(len(numbers_list_as_set) == 1 and 0 in numbers_list_as_set):
        return True
    return False

def run_part1(line_list):
    cumulative_total = 0
    for line in line_list:
        # init
        generated_lines = generate_initial_number_list(line)

        # generated all lists by this point
        levels = len(generated_lines)

        # add placeholder zero to last row
        # row is all zeros. doesnt matter if append or prepend
        generated_lines[levels - 1].append(0) 

        #start from second to last row, then step backwards towards row 0
        for i in range(len(generated_lines)-2, -1, -1):
            # subtract the first item on the row below from the first item on this row, 
            # then insert result as first item on this row
            item_on_this_row = generated_lines[i][-1]
            item_on_row_below = generated_lines[i+1][-1]
            item_to_append = item_on_this_row + item_on_row_below
            generated_lines[i].insert(len(generated_lines[i]),item_to_append)

        # number we care about is the last item on the first line
        final_generated_number = generated_lines[0][-1]
        cumulative_total = cumulative_total + final_generated_number

    return cumulative_total

def run_part2(line_list):
    cumulative_total = 0
    for line in line_list:
        # init
        generated_lines = generate_initial_number_list(line)

        # generated all lists by this point
        levels = len(generated_lines)

        # add placeholder zero to last row
        # row is all zeros. doesnt matter if append or prepend
        generated_lines[levels - 1].append(0) 

        #start from second to last row, then step backwards towards row 0
        for i in range(len(generated_lines)-2, -1, -1):
            # subtract the first item on the row below from the first item on this row, 
            # then insert result as first item on this row
            item_on_this_row = generated_lines[i][0]
            item_on_row_below = generated_lines[i+1][0]
            item_to_append = item_on_this_row - item_on_row_below
            generated_lines[i].insert(0, item_to_append)

        # number we care about is the first item on the first line
        final_generated_number = generated_lines[0][0]
        cumulative_total = cumulative_total + final_generated_number

    return cumulative_total

def run_generic(line_list, index_we_care_about, combine_func, insert_position_func):
    cumulative_total = 0
    for line in line_list:
        # init
        generated_lines = generate_initial_number_list(line)

        # generated all lists by this point
        levels = len(generated_lines)

        # add placeholder zero to last row
        # row is all zeros. doesnt matter if append or prepend
        generated_lines[levels - 1].append(0) 

        #start from second to last row, then step backwards towards row 0
        for i in range(len(generated_lines)-2, -1, -1):
            # exec the combine function with the item at index we care about 
            # on the current line and line below it
            # then use the insert funct to put the result where we want in the current list
            item_on_this_row = generated_lines[i][index_we_care_about]
            item_on_row_below = generated_lines[i+1][index_we_care_about]
            item_to_append = combine_func(item_on_this_row, item_on_row_below)
            insert_position_func(generated_lines[i], item_to_append)

        # number we care about is the first item on the first line
        final_generated_number = generated_lines[0][index_we_care_about]
        cumulative_total = cumulative_total + final_generated_number

    return cumulative_total

def main():
    cwd = os.path.dirname(__file__)
    
    with(open(f"{cwd}/../input.txt", 'r') as fp):
        all_lines = fp.readlines()
    all_lines_trimmed = [x.strip() for x in all_lines]

    print(f"generic part 1 result -> {run_part1(all_lines_trimmed)}")
    print(f"generic part 1 result -> {run_part2(all_lines_trimmed)}")

    print(f"generic part 1 result -> {run_generic(all_lines_trimmed, -1, lambda x,y: x+y, lambda lst, item: lst.append(item))}")
    print(f"generic part 2 result -> {run_generic(all_lines_trimmed, 0, lambda x,y: x-y, lambda lst, item: lst.insert(0,item))}")

if __name__ == "__main__":
    main()