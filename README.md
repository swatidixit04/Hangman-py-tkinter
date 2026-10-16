# Word Guessing Game (Hangman) in Python & Tkinter

A simple, beginner-friendly desktop Hangman game built with Python's built-in `tkinter` library. No third-party packages or installs needed!

---

## 📁 Project Structure

```text
├── hangman.py        # The main game script with GUI and game logic
├── words.txt         # Word list grouped by category (category,word)
├── highscore.json    # Auto-created file that stores wins and streaks
└── README.md         # Instructions and documentation
```

---

## 🚀 How to Run the Game

1. Open your terminal or Command Prompt in this folder:
   ```powershell
   cd "path\to\this\folder"
   ```
2. Run the game using Python:
   ```powershell
   py hangman.py
   ```
   *(or `python hangman.py` if python is directly on your PATH)*

---

## 🎮 Game Features

- **Category Selection**: Choose from **Animals**, **Fruits**, or **Countries** using the dropdown at the top.
- **Visual Hangman Canvas**: A wooden gallows is drawn, and body parts appear one by one as you make wrong guesses.
- **6 Lives**: You start each round with 6 lives.
- **On-Screen Keyboard**: Click buttons **A** through **Z**. Clicked buttons are disabled automatically to prevent duplicate guesses.
- **Hint System**: Click the **💡 Hint** button to reveal one hidden letter at the cost of 1 life (only available when you have more than 1 life).
- **Persistent High Scores**: Automatically tracks and saves your total **Wins**, **Current Streak**, and **Best Streak** in `highscore.json`.
- **New Game / Play Again**: Start a new round anytime with the **New Game** button.

---

## 🧠 How the Code Works (Plain English)

The code is organized into 4 clear sections:

### 1. Global Game State
Simple variables and dictionaries store the current game information:
- `words_by_category`: A dictionary storing words grouped by their category.
- `current_word`: The word chosen at random for the current game.
- `guessed_letters`: A list that remembers every letter you clicked or revealed.
- `lives_left`: Number of lives remaining (starts at `6`).
- `game_over`: Set to `True` when you win or lose so clicks are stopped.
- `letter_buttons`: Stores the 26 button widgets so they can be disabled or re-enabled.
- `stats`: A dictionary storing `wins`, `current_streak`, and `best_streak`.

### 2. File Handling Functions
- **`load_words()`**: Reads `words.txt` line by line, splits each line at the comma into category and word, and groups them into `words_by_category`.
- **`load_highscores()`**: Reads `highscore.json` to load your previous score. If the file doesn't exist yet, it creates one.
- **`save_highscores()`**: Writes updated wins and streak records back to `highscore.json` using Python's `json.dump()`.

### 3. Core Logic & Display Functions
- **`draw_hangman(lives)`**: Uses Tkinter Canvas commands (`create_line` and `create_oval`) to draw the gallows, head, body, arms, and legs based on how many lives remain.
- **`update_display()`**: Builds the text shown on screen. If a letter has been guessed, it shows that letter; otherwise, it shows `_`. It also updates the lives and highscore labels.
- **`make_button_action(letter)`**: A clean helper function that creates a unique click action for each letter button without needing advanced lambda expressions.
- **`start_game()`**: Picks a random word from the selected category, resets lives to 6, clears guessed letters, re-enables all 26 buttons, and resets the hangman drawing.
- **`guess_letter(letter)`**: Checks if the guessed letter is inside `current_word`. If correct, reveals it; if wrong, subtracts 1 life and adds a limb to the drawing.
- **`give_hint()`**: Finds unguessed letters, reveals one at random, deducts 1 life, and updates the board.
- **`check_game_status()`**: Checks if you won (all letters discovered) or lost (lives hit 0). Saves scores and displays a celebratory or game-over message.

### 4. GUI Window Setup
- Initializes the main `tk.Tk()` window.
- Creates the top control bar with the category dropdown, New Game button, and Hint button.
- Adds the Canvas, word blanks label, message banner, and a 3-row grid of letter buttons.
- Starts the game and opens the window using `root.mainloop()`.
