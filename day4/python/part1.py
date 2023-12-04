import math
import os

def main():
    cwd = os.path.dirname(__file__)
    
    with(open(f"{cwd}/../input.txt", 'r') as fp):
        all_lines = fp.readlines()


    total_points = 0
    for line in all_lines:
        stripped = line.strip()
        segments = stripped.split(":")
        numbers_segment = segments[1].split('|')

        winning_numbers = set(filter(str.isdigit, numbers_segment[0].split(' ')))
        your_numbers = set(filter(str.isdigit, numbers_segment[1].split(' ')))

        matched_numbers = your_numbers & winning_numbers
        points = math.floor(pow(2, len(matched_numbers)-1))

        total_points = total_points + points
    
    print(total_points)


if __name__ == "__main__":
    main()