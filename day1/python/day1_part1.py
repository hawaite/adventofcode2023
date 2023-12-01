import os

def get_first_digit(line):
    for char in line:
        if char.isdigit():
            return char

def main():
    cwd = os.path.dirname(__file__)
    
    with(open(f"{cwd}/input.txt", 'r') as fp):
        all_lines = fp.readlines()

    all_lines_stripped = [line.strip() for line in all_lines]
    first_and_last_digits = [int(get_first_digit(line) + get_first_digit(line[::-1])) for line in all_lines_stripped]
    print(sum(first_and_last_digits))
        

if(__name__ == "__main__"):
    main()