# Rewriting the UNO game with improved readability, structure, and inline comments

import random

# Constants for card types
COLORS = ['Red', 'Green', 'Blue', 'Yellow']
VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
          'Skip', 'Reverse', 'Draw Two']
WILD_CARDS = ['Wild', 'Wild Draw Four']


# Represents a single UNO card
class Card:
    def __init__(self, color, value):
        self.color = color  # Can be None for wild cards
        self.value = value

    # Determines if a card is playable on top of another
    def is_playable_on(self, top_card):
        return (
            self.color == top_card.color or
            self.value == top_card.value or
            self.color is None  # Wild cards can be played any time
        )

    def __str__(self):
        return f"{self.color or 'Wild'} {self.value}"


# The deck that holds cards to draw
class Deck:
    def __init__(self):
        self.cards = self._generate_full_deck()
        random.shuffle(self.cards)
        self.discards = []

    # Creates a full UNO deck with all cards
    def _generate_full_deck(self):
        deck = []

        # Add number and action cards for each color
        for color in COLORS:
            deck.append(Card(color, '0'))
            for value in VALUES[1:]:
                deck.extend([Card(color, value), Card(color, value)])

        # Add wild cards
        for _ in range(4):
            deck.append(Card(None, 'Wild'))
            deck.append(Card(None, 'Wild Draw Four'))

        return deck

    # Draw a card, reshuffle if needed
    def draw_card(self):
        if not self.cards:
            self._reshuffle()
        if not self.cards:
            raise ValueError("No cards left to draw!")
        return self.cards.pop()

    # Reshuffle the discard pile into the draw deck
    def _reshuffle(self):
        if len(self.discards) <= 1:
            return
        top = self.discards[-1]
        self.cards = self.discards[:-1]
        self.discards = [top]
        random.shuffle(self.cards)


# Represents each player in the game
class Player:
    def __init__(self, name, is_ai=False):
        self.name = name
        self.hand = []
        self.is_ai = is_ai

    # Draw specified number of cards from deck
    def draw(self, deck, count=1):
        for _ in range(count):
            self.hand.append(deck.draw_card())

    # Check if the player can play any card
    def has_playable_card(self, top_card):
        return any(card.is_playable_on(top_card) for card in self.hand)

    # Choose a card (AI version picks the first legal one)
    def choose_card(self, top_card):
        for card in self.hand:
            if card.is_playable_on(top_card):
                return card
        return None

    # Executes player's full turn
    def play_turn(self, top_card, deck):
        print(f"\n{self.name}'s turn. Top card: {top_card}")
        print(f"Hand: {', '.join(str(card) for card in self.hand)}")

        if not self.has_playable_card(top_card):
            print(f"{self.name} has no playable cards. Drawing one...")
            self.draw(deck)
            return None, False

        card = self.choose_card(top_card)
        if card:
            self.hand.remove(card)
            print(f"{self.name} plays {card}")
            return card, True

        return None, False

    def __len__(self):
        return len(self.hand)


# Controls the overall flow of the UNO game
class UnoGame:
    def __init__(self, players):
        self.deck = Deck()
        self.players = players
        self.discard_pile = [self.deck.draw_card()]
        self.deck.discards = self.discard_pile
        self.direction = 1
        self.current = 0
        self.skip_next = False

        # Deal initial cards
        for player in self.players:
            player.draw(self.deck, 7)

    def next_player_index(self):
        return (self.current + self.direction) % len(self.players)

    # Handle effects of action cards
    def apply_card_effect(self, card):
        if card.value == 'Skip':
            self.skip_next = True
        elif card.value == 'Reverse':
            self.direction *= -1
        elif card.value == 'Draw Two':
            target = self.next_player_index()
            self.players[target].draw(self.deck, 2)
            self.skip_next = True
        elif card.value == 'Wild Draw Four':
            target = self.next_player_index()
            self.players[target].draw(self.deck, 4)
            self.skip_next = True

        # Handle wild card color selection
        if card.color is None:
            card.color = random.choice(COLORS)

        self.deck.discards.append(card)

    # Main game loop
    def play(self):
        while True:
            player = self.players[self.current]
            top_card = self.deck.discards[-1]

            card, played = player.play_turn(top_card, self.deck)

            if played:
                self.apply_card_effect(card)

                # Check for win
                if len(player) == 0:
                    print(f"\n🎉 {player.name} wins!")
                    break
                if len(player) == 1:
                    print(f"🔔 {player.name} says UNO!")

            # Skip logic
            if self.skip_next:
                print(f"{self.players[self.next_player_index()].name}'s turn is skipped.")
                self.current = (self.current + 2 * self.direction) % len(self.players)
                self.skip_next = False
            else:
                self.current = self.next_player_index()


# Setup game with 4 AI players (for notebook-friendly use)
players = [
    Player("Alice", is_ai=True),
    Player("Bob", is_ai=True),
    Player("Carol", is_ai=True),
    Player("Dave", is_ai=True),
]

# Create and run the game
game = UnoGame(players)
game.play()
