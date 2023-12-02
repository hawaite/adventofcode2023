import * as fs from "fs";
import { Game } from "./game";

const main = () => {
    let lineList: string[] = fs
        .readFileSync("../input.txt", "utf-8")
        .split("\n");

    const gameList = lineList.map(it => new Game(it))

    // Part 1
    const maxRed = 12
    const maxGreen = 13
    const maxBlue = 14

    const sumOfValidIds = gameList
        .map(it => { return { "isPossible": it.IsPossibleWithMaximumGivenCubes(maxRed, maxGreen, maxBlue), "id": it.id } })
        .reduce((sum, result) => result.isPossible ? sum + result.id : sum, 0) // if game was possible, add it to total, otherwise just return current total

    console.log("Part 1: Sum of valid IDs -> " + sumOfValidIds)

    // Part 2
    const power = gameList
        .map(it => it.ProductOfCubePowersForGame())
        .reduce((acc, pow) => acc + pow, 0);

    console.log("part 2: total power -> " + power)
}

main()