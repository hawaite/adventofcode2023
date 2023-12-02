import { trim } from "lodash";

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

const ParseGame = (game: String): Game => {
    const segments = game.split(':')
    const id = Number.parseInt(segments[0].slice(5))
    const roundsSegments = segments[1].split(';')
    const rounds = roundsSegments.map(BuildRoundFromRoundString)

    return { id: id, rounds: rounds }
}

const BuildRoundFromRoundString = (roundString: String): Round => {
    const roundEntries = roundString.split(',').map(trim)

    const parsedRoundEntries = roundEntries.map(roundEntry => {
        const matches = roundEntry.match(/^(\d+) (.*)$/)
        if (matches?.length == 3) {
            const count = matches[1]
            const colour = matches[2]
            const roundEntry: RoundEntry = { colour: colour, count: Number.parseInt(count) }
            return roundEntry
        }
        else {
            throw Error("Cant parse round: " + roundEntry)
        }
    })

    return {
        roundEntries: parsedRoundEntries
    }
}

export {Game, Round, RoundEntry, ParseGame}