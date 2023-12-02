import * as fs from "fs";
import { Game, RoundEntry, ParseGame } from "./game";

const getProductOfCubePowersForGame = (game: Game): number => {
    const allRoundEntriesForGame = game.rounds.reduce((accumulator, v) => accumulator.concat(v.roundEntries), Array<RoundEntry>())
    
    const maxRed = allRoundEntriesForGame.filter(entry => entry.colour == "red").reduce((acc, entry) => entry.count > acc ? entry.count : acc, 0)
    const maxGreen = allRoundEntriesForGame.filter(entry => entry.colour == "green").reduce((acc, entry) => entry.count > acc ? entry.count : acc, 0)
    const maxBlue = allRoundEntriesForGame.filter(entry => entry.colour == "blue").reduce((acc, entry) => entry.count > acc ? entry.count : acc, 0)

    // prevent zeros from nuking the multiplication
    // zeros can occur if for example a game never draws a red cube in any round
    // this doesnt appear to happen in any of the given input, but still...
    const clampedRed = Math.max(maxRed, 1)
    const clampedGreen = Math.max(maxGreen, 1)
    const clampedBlue = Math.max(maxBlue, 1)

    return clampedRed * clampedBlue * clampedGreen
}

const main = () => {
    let lineList: string[] = fs
        .readFileSync("../../input.txt", "utf-8")
        .split("\n");

    const power = lineList.map(ParseGame).map(getProductOfCubePowersForGame).reduce((acc, pow) => acc + pow, 0);

    console.log("total power -> " + power)
}

main()