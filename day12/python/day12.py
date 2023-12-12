from functools import cache
import os

@cache
def calculate_valid_options(spring, group_defs):
    # if we ran out of spring string, and we also ran out of groups, return 1 match
    # if we ran out of spring string, and we have remaining groups, return 0 match
    if(len(spring) == 0):
        return 1 if(len(group_defs) == 0) else 0
        
    # if we ran out of groups, and there are no '#' matches left, return 1 match as all empty string, '.' and '?' are valid
    # if we ran out of groups, and we have have remaining spring string, return 0 match
    if(len(group_defs) == 0):
        return 1 if ('#' not in spring) else 0
    
    # can safely drop all preceeding '.' symbols
    if(spring[0] == '.'):
        return calculate_valid_options(spring.lstrip('.'), group_defs)

    # if the symbol is a '?' then we need to test what happens if we make that symbol '.' or '#'
    if(spring[0] == '?'):
        return calculate_valid_options('.' + spring[1:], group_defs) + calculate_valid_options('#' + spring[1:], group_defs)

    if(spring[0] == '#'):
        # return 0 if there are not enough chars left to service the group
        if(len(spring) < group_defs[0]):
            return 0 
        
        # return 0 if there is a . where we would like to place the current group
        if('.' in spring[0:group_defs[0]]):
            return 0

        # return 0 if the symbol immediately following this hypothetical group placement is a '#', as that would create a group 1 too big
        if(spring[group_defs[0]] == '#'):
            return 0

        # if the start of the spring string is all '#' or '?' symbols, we can consume those chars, consume that first group, and continue

        if(all(map(lambda x: x!='.', spring[0:group_defs[0]]))):
            # remove the group length prefix, remove the next char, be it '.' or '?' as both can count as group ends
            # re-run with the remaining string and groups
            return calculate_valid_options(spring[group_defs[0]+1:], group_defs[1:])
        else:
            # there was a '.' in the area where we wanted to put the group, so return 0
            return 0
        
def main():
    cwd = os.path.dirname(__file__)
    with(open(f"{cwd}/../input.txt", 'r') as fp):
        all_lines = fp.readlines()
    all_lines_stripped = [line.strip() for line in all_lines]

    part1_rows = [(x.split(" ")[0] + ".", tuple(map(int, x.split(" ")[1].split(",")))) for x in all_lines_stripped]
    part2_rows = [
            (
                "?".join([x.split(" ")[0]]*5) + ".", 
                tuple(map(int, ",".join([x.split(" ")[1]] * 5).split(",")))
            ) for x in all_lines_stripped]


    print(f"part 1 -> {sum(list(map(lambda x: calculate_valid_options(x[0],x[1]), part1_rows)))}")
    print(f"part 2 -> {sum(list(map(lambda x: calculate_valid_options(x[0],x[1]), part2_rows)))}")

if __name__ == "__main__":
    main()