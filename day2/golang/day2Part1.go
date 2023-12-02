package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type round struct {
	red   int
	green int
	blue  int
}

func parseRound(roundStr string) round {
	round_entries := strings.Split(roundStr, ",")
	var parsed_round round

	for i := 0; i < len(round_entries); i++ {
		// trim spaces
		trimmed := strings.TrimSpace(round_entries[i])
		r := regexp.MustCompile(`^(\d+) (.*)$`)
		matches := r.FindStringSubmatch(trimmed)
		count, _ := strconv.Atoi(matches[1])
		colour := matches[2]

		if colour == "red" {
			parsed_round.red = count
		} else if colour == "green" {
			parsed_round.green = count
		} else if colour == "blue" {
			parsed_round.blue = count
		}
	}

	return parsed_round
}

func parseRoundList(roundList []string) []round {
	parsedRounds := make([]round, 0)

	for i := 0; i < len(roundList); i++ {
		parsedRounds = append(parsedRounds, parseRound(roundList[i]))
	}

	return parsedRounds
}

func main() {
	MAX_RED := 12
	MAX_GREEN := 13
	MAX_BLUE := 14

	dat, err := os.ReadFile("../input.txt")

	if err != nil {
		panic("Could not open file")
	}

	lines := strings.Split(string(dat), "\n")

	validGameIds := make([]int, 0)

	// for each game
	for i := 0; i < len(lines); i++ {
		current_game := lines[i]
		segments := strings.Split(current_game, ":")

		game_id, _ := strconv.Atoi(strings.Split(segments[0], " ")[1])
		rounds_list_str := strings.Split(segments[1], ";")

		rounds_list := parseRoundList(rounds_list_str)

		found_max_red := 0
		found_max_green := 0
		found_max_blue := 0

		// for each round, get the highest count for each colour
		for i := 0; i < len(rounds_list); i++ {
			if rounds_list[i].red > found_max_red {
				found_max_red = rounds_list[i].red
			}

			if rounds_list[i].green > found_max_green {
				found_max_green = rounds_list[i].green
			}

			if rounds_list[i].blue > found_max_blue {
				found_max_blue = rounds_list[i].blue
			}
		}

		// if the highest found number is below the allowed maximums, add it to the valid list
		if found_max_red <= MAX_RED && found_max_green <= MAX_GREEN && found_max_blue <= MAX_BLUE {
			validGameIds = append(validGameIds, game_id)
		}
	}

	// sum the valid ids list
	total := 0
	for i := 0; i < len(validGameIds); i++ {
		total += validGameIds[i]
	}

	fmt.Printf("Sum of Valid IDs -> %d\n", total)
}
