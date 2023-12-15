import os 

def hash(input_str):
    current = 0
    for char in input_str:
        char_ascii_number = ord(char)
        current += char_ascii_number
        current *= 17
        current %= 256
    return current

def parse_step_again(step_str):
    return (step_str[:-1], '-', 0) if (step_str[-1] == '-') else (step_str[:-2], '=', int(step_str[-1]))

def ix_of_label_in_box(box_contents, label_to_find):
    found_indexes = [i for i,x in enumerate(box_contents) if x[0] == label_to_find]
    return -1 if len(found_indexes) != 1 else found_indexes[0]

def calculate_overall_box_power(box, box_power):
    return sum(map(lambda ix: box_power * (ix[0]+1) * ix[1][2], [x for x in enumerate(box)]))

def main():
    cwd = os.path.dirname(__file__)
    
    with(open(f"{cwd}/../input.txt", 'r') as fp):
        all_lines = fp.readlines()
    all_lines_trimmed = [x.strip() for x in all_lines]

    steps = all_lines_trimmed[0].split(",")
    parsed = list(map(lambda x: parse_step_again(x), steps))

    boxes = {}
    for i in range(0,256):
        boxes[i] = []

    for step in parsed:
        lens_label, step_operation, _ = step
        box_label = hash(lens_label)

        if(step_operation == '-'):
            matching_ix = ix_of_label_in_box(boxes[box_label], lens_label)
            if(matching_ix != -1):
                del boxes[box_label][matching_ix]
        else:
            matching_ix = ix_of_label_in_box(boxes[box_label], lens_label)
            if(matching_ix != -1 ):
                boxes[box_label][matching_ix] = step
            else:
                boxes[box_label].append(step)

    total_power = 0
    for i in range(0,256):
        box = boxes[i]
        box_power = i + 1
        total_power += calculate_overall_box_power(box, box_power)

    print(total_power)
if __name__ == "__main__":
    main()