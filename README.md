## Word Guessing Game (Hangman)

A simple Hangman-style word guessing game built with **Python** and **Tkinter**. I made this as a beginner project to learn GUI programming, functions, and file handling.

## Features
- Choose a category: Animals, Fruits, or Countries
- Words are shown as blanks, like `_ _ _ _ _`
- Clickable A-Z letter buttons (used letters get disabled)
- 6 lives, and the hangman is drawn on a canvas with each wrong guess
- Hint button that reveals one letter at the cost of one life
- Win/lose message with a "Play Again" button
- Wins and best streak are saved between sessions

## Requirements
- Python 3.8 or newer
- Tkinter (comes built into Python, no installation needed)

## How to Run
bash
git clone https://github.com/swatidixit04/Hangman-py-tkinter.git
cd Hangman-py-tkinter
python hangman.py

## Project Structure
```
word-guessing-game/
├── hangman.py       # main game code
├── words.txt        # word list (format: category,word)
├── highscore.json   # saved wins and best streak (auto-created)
└── README.md
```

## How to Play
1. Pick a category and click **New Game**.
2. Click letters to guess the secret word.
3. Each wrong guess costs a life and adds a part to the hangman.
4. Guess the word before you run out of lives!

## Adding Your Own Words
Open `words.txt` and add a new line in this format:
```
Animals,elephant
```

## What I Learned
- Building windows with Tkinter (Labels, Buttons, Canvas)
- Handling button clicks (events)
- Reading and writing files (text and JSON)
- Organizing code into small functions

## Future Ideas
- [ ] Difficulty levels
- [ ] Timer mode
- [ ] Two-player mode
- [ ] Sound effects

## License
MIT License. Free to use and modify.
