import * as fs from "fs";
import { ParseGame } from "./game";

interface Round {
    roundEntries: RoundEntry[]
}

interface RoundEntry {
    colour: String,
    count: number
}

interface Game {
    id: number,
    rounds: Round[]
}

const maxValueByColour = (colour: String): number => {
    switch (colour) {
        case "red":
            return 12
        case "green":
            return 13
        case "blue":
            return 14
        default:
            throw Error(colour + " is not a valid colour")
    }
}

const roundWouldBePossible = (round: Round): Boolean => {
    return round.roundEntries.map(roundEntry => roundEntry.count <= maxValueByColour(roundEntry.colour)).every(it => it)
}

const gameWouldBePossible = (game: Game): Boolean => {
    return game.rounds.map(roundWouldBePossible).every(it => it)
}

const main = () => {
    let lineList: string[] = fs
        .readFileSync("../../input.txt", "utf-8")
        .split("\n");

    const sumOfValidIds = lineList
        .map(ParseGame) // parse the line to a game object
        .map(it => { return {"isPossible": gameWouldBePossible(it), "id": it.id }})  // check if game would have been possible
        .reduce((sum,result) => result.isPossible ? sum + result.id : sum, 0) // if game was possible, add it to total, otherwise just return current total

    console.log("Sum of valid IDs: " + sumOfValidIds)
}

main()