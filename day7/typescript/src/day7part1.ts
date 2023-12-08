import * as fs from "fs";
import { CardHand, HandComparator } from './CardHand'

const main = () => {
    let lineList: string[] = fs
        .readFileSync("../input.txt", "utf-8")
        .split("\n");

    const handList = lineList.map(it => new CardHand(it))
    const sorted = handList.sort(HandComparator)

    let acc = 0
    for (let index = 0; index < sorted.length; index++) {
        const hand = sorted[index];
        acc = acc + ((index+1) * hand.bet)
        // console.log(`hand: ${hand.handDefinitionString}, rank: ${index}, bet: ${hand.bet}, payout: ${((index+1) * hand.bet)}, acc: ${acc}`)
    }

    console.log(`Part 1 answer -> ${acc}`)
    sorted.length
}

main()