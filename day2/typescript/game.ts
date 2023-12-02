import { trim } from "lodash";

interface Round {
    roundEntries: RoundEntry[]
}

interface RoundEntry {
    colour: String,
    count: number
}

class Game{
    id: number
    rounds: Round[]

    constructor(gameString:String){
        const segments = gameString.split(':')
        this.id = Number.parseInt(segments[0].slice(5))
        this.rounds = segments[1].split(';').map(this.BuildRoundFromRoundString)
    }

    IsPossibleWithMaximumGivenCubes = (maxRed: number, maxGreen:number, maxBlue:number) : Boolean => {
        return this.rounds
            .map(it => this.RoundWouldBePossible(it, maxRed, maxGreen, maxBlue))
            .every(it => it)
    }

    ProductOfCubePowersForGame = (): number => {
        const allRoundEntriesForGame = this.rounds.reduce((accumulator, v) => accumulator.concat(v.roundEntries), Array<RoundEntry>())
    
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

    private RoundWouldBePossible = (round: Round, maxRed: number, maxGreen:number, maxBlue:number): Boolean => {
        return round.roundEntries
            .map(roundEntry => roundEntry.count <= this.MaxValueByColour(roundEntry.colour, maxRed, maxGreen, maxBlue))
            .every(it => it)
    }

    private MaxValueByColour = (colour: String, maxRed: number, maxGreen: number, maxBlue: number) : number => {
        switch(colour){
            case "red":
                return maxRed;
            case "green":
                return maxGreen;
            case "blue":
                return maxBlue;
            default:
                throw Error("Color " + colour + " is not one of red, green, or blue")
        }
    }

    private BuildRoundFromRoundString = (roundString: String): Round => {
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
}



export {Game, Round, RoundEntry}