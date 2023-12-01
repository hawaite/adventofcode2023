import os

wordy_numbers = dict(zip(["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"], range(1, 10)))

# consumes a line from the beginning, returning a list of all digits it finds
def line_to_list(line):
    parsed = []
    remaining_line = line
    while remaining_line != "":
        if remaining_line[0].isdigit():
            parsed.append(remaining_line[0])
            remaining_line = remaining_line[1:]
            continue

        # wasnt a digit, check if we are at the start of a word-number
        for key in wordy_numbers:
            if remaining_line.startswith(key):
                parsed.append(str(wordy_numbers[key]))
                break
        
        remaining_line = remaining_line[1:]
    return parsed
        
def main():
    cwd = os.path.dirname(__file__)
    
    with(open(f"{cwd}/input.txt", 'r') as fp):
        all_lines = fp.readlines()

    all_lines_stripped = [line.strip() for line in all_lines]
    parsed_lines = [line_to_list(line) for line in all_lines_stripped]
    combined_first_and_last_digits = [int(lst[0] + lst[-1]) for lst in parsed_lines]
    print(sum(combined_first_and_last_digits))
        

if(__name__ == "__main__"):
    main()