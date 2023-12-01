import os

wordy_numbers = {
    "one": "1", 
    "two": "2", 
    "three": "3", 
    "four": "4", 
    "five": "5", 
    "six": "6", 
    "seven": "7", 
    "eight": "8", 
    "nine": "9"
    }

def line_to_list(line):
    parsed = []
    remaining_line = line
    while remaining_line != "":
        if remaining_line[0].isdigit():
            parsed.append(remaining_line[0])
            remaining_line = remaining_line[1:]
            continue

        # found_a_word = False
        for key in wordy_numbers:
            if remaining_line.startswith(key):
                parsed.append(wordy_numbers[key])
                break
        
        remaining_line = remaining_line[1:]
    return parsed
        
def combine_first_and_last(lst):
    return int(lst[0] + lst[-1])

def main():
    cwd = os.path.dirname(__file__)
    
    with(open(f"{cwd}/input.txt", 'r') as fp):
        all_lines = fp.readlines()

    all_lines_stripped = [line.strip() for line in all_lines]
    parsed_lines = [line_to_list(line) for line in all_lines_stripped]
    combined_first_and_last_digits = [combine_first_and_last(lst) for lst in parsed_lines]
    print(sum(combined_first_and_last_digits))
        

if(__name__ == "__main__"):
    main()