# 🃏 UNO Python Game

A simple terminal-based implementation of the classic card game **UNO**, written in Python. This version supports up to 4 players, including both human and AI players.

## 🎮 How to Play

- Players take turns playing cards from their hand that match the **color** or **value** of the top card on the discard pile.
- If a player cannot play, they draw one card.
- First player to get rid of all their cards wins.
- When a player has one card left, they must say "UNO!" (automatically announced in this version).

## 🔧 Features

- ✅ Supports up to 4 players
- 🧠 AI players make legal moves automatically
- 🔄 Handles all standard UNO cards:
  - Number cards (0–9)
  - Action cards: **Skip**, **Reverse**, **Draw Two**
  - Wild cards: **Wild**, **Wild Draw Four**
- 🎨 Wild color selection (random for AI, manual for human)
- ⏩ Skip and Reverse functionality
- ❗ Declares "UNO" when a player has one card left

## 🖥️ How to Run

Make sure you have Python 3 installed. Then run:

```bash
python Uno.py
