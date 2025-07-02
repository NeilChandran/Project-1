# UNO Game with Organized Deck, Clear Instructions, and Draw Reveal

import random

COLORS = ['Red', 'Green', 'Blue', 'Yellow']
VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
          'Skip', 'Reverse', 'Draw Two']
WILD_CARDS = ['Wild', 'Wild Draw Four']

class Card:
    def __init__(self, color, value):
        self.color = color  # Can be None for wilds
        self.value = value

    def is_playable_on(self, top_card):
        return (self.color == top_card.color or 
                self.value == top_card.value or 
                self.color is None)  # Wild

    def __str__(self):
        return f"{self.color or 'Wild'} {self.value}"

class Deck:
    def __init__(self):
        self.cards = self.generate_deck()
        random.shuffle(self.cards)
        self.discards = []

    def generate_deck(self):
        deck = []
        for color in COLORS:
            deck.append(Card(color, '0'))
            for value in VALUES[1:]:
                deck.extend([Card(color, value), Card(color, value)])
        for _ in range(4):
            deck.append(Card(None, 'Wild'))
            deck.append(Card(None, 'Wild Draw Four'))
        return deck

    def draw_card(self):
        if not self.cards:
            self.reshuffle_discard()
        return self.cards.pop() if self.cards else None

    def reshuffle_discard(self):
        if len(self.discards) > 1:
            top = self.discards[-1]
            self.cards = self.discards[:-1]
            self.discards = [top]
            random.shuffle(self.cards)

class Player:
    def __init__(self, name, is_ai=False):
        self.name = name
        self.hand = []
        self.is_ai = is_ai

    def draw(self, deck, count=1):
        drawn_cards = []
        for _ in range(count):
            card = deck.draw_card()
            if card:
                self.hand.append(card)
                drawn_cards.append(card)
        return drawn_cards

    def has_playable_card(self, top_card):
        return any(card.is_playable_on(top_card) for card in self.hand)

    def choose_card(self, top_card):
        for card in self.hand:
            if card.is_playable_on(top_card):
                return card
        return None

    def play_turn(self, top_card, deck):
        print(f"\n===== {self.name.upper()}'S TURN =====")
        print(f"Top card in play: {top_card}")
        print(f"Your current hand: {', '.join(str(card) for card in self.hand)}")

        if not self.has_playable_card(top_card):
            print(f"{self.name} has no playable cards. Drawing one from the deck...")
            drawn = self.draw(deck)
            if drawn:
                print(f"You drew: {drawn[-1]}")
            return None, False

        card = self.choose_card(top_card) if self.is_ai else self.prompt_card(top_card)
        if card:
            self.hand.remove(card)
            print(f"{self.name} plays {card}")
            return card, True
        return None, False

    def prompt_card(self, top_card):
        playable = [card for card in self.hand if card.is_playable_on(top_card)]
        print("Playable cards:")
        for i, card in enumerate(playable):
            print(f"  {i+1}: {card}")
        choice = input("Enter the number of the card you want to play, or press Enter to draw: ")
        if choice.isdigit() and 1 <= int(choice) <= len(playable):
            return playable[int(choice) - 1]
        return None

    def __len__(self):
        return len(self.hand)

class UnoGame:
    def __init__(self, players):
        self.deck = Deck()
        self.players = players
        self.discard_pile = [self.deck.draw_card()]
        self.deck.discards = self.discard_pile
        self.direction = 1
        self.current = 0

        for player in self.players:
            player.draw(self.deck, 7)

    def next_player_index(self):
        return (self.current + self.direction) % len(self.players)

    def apply_card_effect(self, card):
        if card.value == 'Skip':
            print(f"{self.players[self.next_player_index()].name}'s turn is skipped!")
            self.current = self.next_player_index()
        elif card.value == 'Reverse':
            print("Direction reversed!")
            self.direction *= -1
        elif card.value == 'Draw Two':
            target = self.next_player_index()
            print(f"{self.players[target].name} draws two cards and is skipped!")
            self.players[target].draw(self.deck, 2)
            self.current = target
        elif card.value == 'Wild Draw Four':
            target = self.next_player_index()
            print(f"{self.players[target].name} draws four cards and is skipped!")
            self.players[target].draw(self.deck, 4)
            self.current = target

        if card.color is None:
            if self.players[self.current].is_ai:
                chosen_color = random.choice(COLORS)
                print(f"{self.players[self.current].name} chooses the color {chosen_color}")
            else:
                chosen_color = input(f"{self.players[self.current].name}, choose a color (Red, Green, Blue, Yellow): ")
            card.color = chosen_color.capitalize()

        self.discard_pile.append(card)

    def play(self):
        print("\n🃏 Welcome to UNO!")
        input("Press Enter to begin...")

        while True:
            player = self.players[self.current]
            top_card = self.discard_pile[-1]
            card, played = player.play_turn(top_card, self.deck)
            if played:
                self.apply_card_effect(card)
                if len(player) == 0:
                    print(f"\n🎉 {player.name} wins the game!")
                    break
                if len(player) == 1:
                    print(f"🔔 {player.name} says UNO!")
            else:
                self.current = self.next_player_index()
            self.current = self.next_player_index()

# Example game setup
players = [
    Player("You", is_ai=False),
    Player("Bot1", is_ai=True),
    Player("Bot2", is_ai=True),
    Player("Bot3", is_ai=True),
]

game = UnoGame(players)
game.play()

