import os

# recursively generate the initial list containing the generated rows
def generate_initial_rows_list(numbers: [int]):
    def internal(numbers, output_lines):
        if ( row_is_all_zeros(numbers) ):
            return output_lines
        else:
            next_row = generate_next_row(numbers)
            return internal(next_row, output_lines + [next_row])
        
    return internal(numbers, [numbers])

# recursively generate the next row, given the current row
def generate_next_row(input_row: [int]):
    def internal(input_row, output_row):
        # only 1 item you cant subtract the next one
        if(len(input_row) == 1):
            return output_row
        else:
            output_row.append(input_row[1] - input_row[0])
            
            return internal(input_row[1:], output_row)
        
    return internal(input_row, [])

# test if very item in this row is 0
def row_is_all_zeros(row):
    row_as_set = set(row)
    if(len(row_as_set) == 1 and 0 in row_as_set):
        return True
    return False

# updates the rows with new generated values and returns the new row list
def generate_new_row_items(rows, part2_rules):
    def internal(rows, output_rows, part2_rules):
        if(len(rows) == 0):
            return output_rows
        else:
            # if last input row is all zeros, add another one.
            last_input_row = rows[-1]
            item_to_add_to_row = 0

            if(not row_is_all_zeros(last_input_row)):
                # get last row of input list and first line of output list.
                first_output_line = output_rows[0]
                # do part-specific maths
                item_to_add_to_row = (last_input_row[0] - first_output_line[0]) if part2_rules else (last_input_row[-1] + first_output_line[-1])
                
            # append result to input row and throw it on the output pile
            new_row = [[item_to_add_to_row] + last_input_row ] if part2_rules else [last_input_row +[item_to_add_to_row] ]
            return internal(rows[:-1], new_row + output_rows, part2_rules)

    return internal(rows, [], part2_rules)

def run(line_list, part2_rules):
    def internal(line_list, running_total, part2_rules):
        index_to_sum = 0 if part2_rules else -1

        if(len(line_list) == 0):
            return running_total
        else:
            numbers = line_list[0].split(" ")
            numbers = [int(x) for x in numbers]

            return internal(
                line_list[1:], 
                running_total + generate_new_row_items(generate_initial_rows_list(numbers), part2_rules)[0][index_to_sum], 
                part2_rules
            ) 

    return internal(line_list, 0, part2_rules)

def main():
    cwd = os.path.dirname(__file__)
    
    with(open(f"{cwd}/../input.txt", 'r') as fp):
        all_lines = fp.readlines()
    all_lines_trimmed = [x.strip() for x in all_lines]

    print(f"part 1 result -> {run(all_lines_trimmed, part2_rules=False)}")
    print(f"part 2 result -> {run(all_lines_trimmed, part2_rules=True)}")

if __name__ == "__main__":
    main()