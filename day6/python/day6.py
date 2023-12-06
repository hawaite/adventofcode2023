import os
import functools
import math

def main(partTwo):
    cwd = os.path.dirname(__file__)
    
    with(open(f"{cwd}/../input.txt", 'r') as fp):
        all_lines = fp.readlines()

    times = [ x for x in all_lines[0].strip().split(" ") if x != ""][1:]
    distances = [ x for x in all_lines[1].strip().split(" ") if x != ""][1:]
    
    if partTwo:
        times = [ ''.join(times) ]
        distances = [ ''.join(distances) ]

    potential_wins_per_race = []

    for race_number in range(0, len(times)):
        race_time = int(times[race_number])
        race_record_distance = int(distances[race_number])

        for i in range(0, math.floor((race_time+1)/2)): # check up to half
            distance_per_ms = i
            time_left_to_travel_ms = race_time - i
            total_distance = time_left_to_travel_ms * distance_per_ms
            if ( total_distance > race_record_distance):
                # we found the point where we start beating the record and can infer the total
                potential_wins_per_race.append( race_time - (2 * i) + 1)
                break

    print(f"multiplied: {functools.reduce(lambda x,y: x*y, potential_wins_per_race)}")

if(__name__ == "__main__"):
    # main(partTwo=False)
    main(partTwo=True)