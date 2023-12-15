import os 

def hash(input_str):
    current = 0

    for char in input_str:
        char_ascii_number = ord(char)
        current += char_ascii_number
        current *= 17
        current %= 256

    return current

def main():
    cwd = os.path.dirname(__file__)
    
    with(open(f"{cwd}/../input.txt", 'r') as fp):
        all_lines = fp.readlines()
    all_lines_trimmed = [x.strip() for x in all_lines]

    steps = all_lines_trimmed[0].split(",")

    hashed = map(lambda x: hash(x), steps)

    print(sum(hashed))

if __name__ == "__main__":
    main()