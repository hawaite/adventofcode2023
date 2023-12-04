import os

class ScratchCard:
    def __init__(self, game_id, winning_numbers, your_numbers):
        self.game_id = game_id
        self.winning_numbers = winning_numbers
        self.your_numbers = your_numbers
        self.win_count = len(self.winning_numbers & self.your_numbers)
    
class ScratchCards:
    def __init__(self, scratchCard):
        self.scratchCard = scratchCard
        self.unprocessed_copies = 1
        self.processed_copies = 0

def main():
    cwd = os.path.dirname(__file__)
    
    scratchcards = {}

    with(open(f"{cwd}/../input.txt", 'r') as fp):
        all_lines = fp.readlines()

    # init the scratchcard map
    for line in all_lines:
        stripped = line.strip()
        segments = stripped.split(":")
        numbers_segment = segments[1].split('|')

        game_id = segments[0].split(" ")[-1]
        winning_numbers = set(filter(str.isdigit, numbers_segment[0].split(' ')))
        your_numbers = set(filter(str.isdigit, numbers_segment[1].split(' ')))
        
        scratchcards[game_id] = ScratchCards(ScratchCard(game_id, winning_numbers, your_numbers))
    
    # process cards forever until we run out of unprocessed cards
    while True:
        no_cards_left = True
        for game_id in scratchcards:
            current_card:ScratchCards = scratchcards[game_id]
            if current_card.unprocessed_copies != 0:
                no_cards_left = False

                cards_to_add_one_to = range(int(current_card.scratchCard.game_id)+1, int(current_card.scratchCard.game_id) + current_card.scratchCard.win_count + 1)

                # add 1 unprocessed to each card
                for card in cards_to_add_one_to:
                    scratchcards[str(card)].unprocessed_copies = scratchcards[str(card)].unprocessed_copies + 1
                

                # mark this card as processed
                current_card.unprocessed_copies = current_card.unprocessed_copies - 1
                current_card.processed_copies = current_card.processed_copies + 1
        
        if no_cards_left == True:
            break
    
    total_card_count = 0
    for card in scratchcards:
        total_card_count = total_card_count + scratchcards[card].processed_copies

    print(f"Total card count -> {total_card_count}")

if __name__ == "__main__":
    main()