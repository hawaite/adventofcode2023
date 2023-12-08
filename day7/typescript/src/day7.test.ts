import { CardComparator, CardHand, HandComparator, HandType } from "./CardHand"

test("Card Hands construct correctly", () => {
    const hand = new CardHand("12345 67")
    expect(hand.handDefinitionString).toBe("12345")
    expect(hand.bet).toBe(67)
})

test.each(
    [
        ["22222", HandType.FiveOfAKind], 
        ["33332", HandType.FourOfAKind], 
        ["11122", HandType.FullHouse], 
        ["11123", HandType.ThreeOfAKind], 
        ["12233", HandType.TwoPair], 
        ["12344", HandType.OnePair], 
        ["87654", HandType.HighCard]
    ]
)("Card Hand types are correctly parsed: %s - %s", (testInput, expectedHandType) => {
    const hand = new CardHand(testInput + " 67")
    
    expect(hand.type).toBe(expectedHandType)
    expect(hand.handDefinitionString).toBe(testInput)
    expect(hand.bet).toBe(67)
})

test.each([
    [['2', '3'], ['2', '3']],
    [['3', '2'], ['2', '3']],
    [['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'], ['2','3','4','5','6','7','8','9','T','J','Q','K','A']],
])("card comparitor orders correctly", (inputList, expectedList)=>{
    expect(inputList.sort(CardComparator)).toEqual(expectedList)
})

test.each([
    // these should reverse
    [new CardHand("77777 7"), new CardHand("67777 7"), "77777"], // 5 of a kind - 4 of a kind
    [new CardHand("67777 7"), new CardHand("66777 7"), "67777"], // 4 of a kind - full house
    [new CardHand("66777 7"), new CardHand("66627 7"), "66777"], // full house - three of a kind
    [new CardHand("66627 7"), new CardHand("66277 7"), "66627"], // three of a kind - two pair
    [new CardHand("66277 7"), new CardHand("66723 7"), "66277"], // two pair - one pair
    [new CardHand("66723 7"), new CardHand("67234 7"), "66723"], // one pair - high card

    // these should remain in order
    [new CardHand("67777"), new CardHand("77777"), "77777"], // 5 of a kind - 4 of a kind
    [new CardHand("66777"), new CardHand("67777"), "67777"], // 4 of a kind - full house
    [new CardHand("66627"), new CardHand("66777"), "66777"], // full house - three of a kind
    [new CardHand("66277"), new CardHand("66627"), "66627"], // three of a kind - two pair
    [new CardHand("66723"), new CardHand("66277"), "66277"], // two pair - one pair
    [new CardHand("67234"), new CardHand("66723"), "66723"], // one pair - high card

    [new CardHand("77777"), new CardHand("22222"), "77777"], // both 5 of a kind
    [new CardHand("22222"), new CardHand("77777"), "77777"], // both 5 of a kind

    [new CardHand("77723"), new CardHand("72322"), "77723"], // both 3 of a kind
    [new CardHand("72322"), new CardHand("77723"), "77723"], // both 3 of a kind


])('hand comparitor orders correctly', (handA, handB, expectedHighestItem) => {
    const sorted = Array.of(handA, handB).sort(HandComparator)
    console.log(Array.of(handA, handB))
    console.log(sorted)
    expect(sorted[1].handDefinitionString).toBe(expectedHighestItem)
})