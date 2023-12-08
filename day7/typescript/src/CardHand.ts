enum HandType{
    FiveOfAKind = 1,
    FourOfAKind = 2,
    FullHouse = 3,
    ThreeOfAKind = 4,
    TwoPair = 5,
    OnePair = 6,
    HighCard = 7,
    Unknown = 8
}

const cardOrder = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

const CardComparator = (a:String, b:String): number => {
    const aIndex = cardOrder.indexOf(a.toString())
    const bIndex = cardOrder.indexOf(b.toString())

    if(aIndex<bIndex)
        return 1
    if(aIndex>bIndex)
        return -1
    return 0
}

const HandComparator = (a:CardHand, b:CardHand):number => {
    // primary compare based on hand type
    if(a.type < b.type){
        return 1
    }
    if(a.type > b.type){
        return -1
    }

    // secondary compare based in hand string 
    for (let index = 0; index < a.handDefinitionString.length; index++) {
        const cardComparison = CardComparator(a.handDefinitionString[index],b.handDefinitionString[index])
        if(cardComparison != 0)
            return cardComparison
    }

    return 0
}

class CardHand{
    handDefinitionString:String;
    bet: number;
    type: HandType

    constructor(definitionString:String){
        const segments = definitionString.split(" ")
        this.handDefinitionString = segments[0]
        this.bet = Number.parseInt(segments[1])
        this.type = this.calculateType(this.handDefinitionString)
    }

    private calculateType(handDefinitionString:String): HandType{
        const cardCountMap = new Map<String, number>()
        handDefinitionString.split('').forEach( card => {
            cardCountMap.set(card, (cardCountMap.get(card) ?? 0) + 1)
        })

        /*
            map size of 1 can only be 5 of a kind
            map size of 2 can be four of a kind or full house
            map size of 3 can be three of a kind or two pair
            map size of 4 can only be one pair
            map size of 5 can only be high card
        */
        switch(cardCountMap.size){
            case 1:
                return HandType.FiveOfAKind
            case 2:
                return (Array.from(cardCountMap.values()).filter(it => it==4).length > 0) ? HandType.FourOfAKind : HandType.FullHouse
            case 3:
                return (Array.from(cardCountMap.values()).filter(it => it==3).length > 0) ? HandType.ThreeOfAKind : HandType.TwoPair
            case 4:
                return HandType.OnePair
            case 5:
                return HandType.HighCard
            default:
                return HandType.Unknown
        }
    }

    public toString = () : string => {
        return `CardHand { handDefinitionString: ${this.handDefinitionString}, bet: ${this.bet}, type: ${HandType[this.type]} }`;
    }
}

export {CardHand, HandType, CardComparator, HandComparator};