# =============================================================================
# Word Guessing Game (Hangman) in Python using Tkinter
# Standard library only (no extra installs required)
# =============================================================================
import tkinter as tk
import random
import json
import os

# --- File Paths & Global State ---
WORDS_FILE = "words.txt"
HIGHSCORE_FILE = "highscore.json"

words_by_category = {}      # Loaded categories and their word lists
current_word = ""           # Secret word for current round
guessed_letters = []        # Letters guessed so far
lives_left = 6              # Lives remaining (starts at 6)
game_over = False           # True when round is won or lost
letter_buttons = {}         # Dictionary of button widgets for letters A-Z
stats = {"wins": 0, "current_streak": 0, "best_streak": 0}

# --- 1. File Handling Functions ---
def load_words():
    """Reads categories and words from words.txt into a dictionary."""
    global words_by_category
    words_by_category = {}
    with open(WORDS_FILE, "r") as file:
        for line in file:
            cleaned = line.strip()
            if cleaned and "," in cleaned:
                cat, word = cleaned.split(",", 1)
                cat, word = cat.strip(), word.strip().upper()
                if cat not in words_by_category:
                    words_by_category[cat] = []
                words_by_category[cat].append(word)

def load_highscores():
    """Loads scores from highscore.json if it exists, or creates default."""
    global stats
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as file:
            stats = json.load(file)
    else:
        save_highscores()

def save_highscores():
    """Saves current wins and streaks to highscore.json."""
    with open(HIGHSCORE_FILE, "w") as file:
        json.dump(stats, file, indent=4)

# --- 2. Drawing & UI Update Functions ---
def draw_hangman(lives):
    """Draws gallows and body parts on canvas based on remaining lives."""
    canvas.delete("all")  # Clear previous drawing
    # Always draw gallows (ground, pole, beam, rope)
    canvas.create_line(20, 200, 180, 200, width=4, fill="#5c3a21")  # Base
    canvas.create_line(60, 200, 60, 20, width=4, fill="#5c3a21")    # Pole
    canvas.create_line(60, 20, 140, 20, width=4, fill="#5c3a21")    # Top beam
    canvas.create_line(140, 20, 140, 50, width=3, fill="#8B4513")   # Rope
    # Draw body parts as lives decrease (6 -> 0)
    if lives <= 5: canvas.create_oval(125, 50, 155, 80, width=3, outline="#2c3e50")   # Head
    if lives <= 4: canvas.create_line(140, 80, 140, 135, width=3, fill="#2c3e50")    # Body
    if lives <= 3: canvas.create_line(140, 95, 115, 120, width=3, fill="#2c3e50")    # Left Arm
    if lives <= 2: canvas.create_line(140, 95, 165, 120, width=3, fill="#2c3e50")    # Right Arm
    if lives <= 1: canvas.create_line(140, 135, 120, 175, width=3, fill="#2c3e50")   # Left Leg
    if lives <= 0: canvas.create_line(140, 135, 160, 175, width=3, fill="#2c3e50")   # Right Leg

def update_display():
    """Updates word blanks, lives counter, and score text on screen."""
    display_letters = []
    for char in current_word:
        display_letters.append(char if char in guessed_letters else "_")
    word_label.config(text=" ".join(display_letters))
    lives_label.config(text="Lives Left: " + str(lives_left))
    score_text = "Wins: " + str(stats["wins"]) + " | Streak: " + str(stats["current_streak"]) + " | Best: " + str(stats["best_streak"])
    stats_label.config(text=score_text)

def make_button_action(letter):
    """Creates a button click function without using lambda."""
    def action():
        guess_letter(letter)
    return action

def disable_all_buttons():
    """Disables all letter buttons when round finishes."""
    for btn in letter_buttons.values():
        btn.config(state="disabled")

# --- 3. Core Game Logic Functions ---
def start_game():
    """Resets variables and starts a new game round."""
    global current_word, guessed_letters, lives_left, game_over
    cat = category_var.get()
    current_word = random.choice(words_by_category.get(cat, ["PYTHON"]))
    guessed_letters = []
    lives_left = 6
    game_over = False
    message_label.config(text="Pick a letter or use a hint!", fg="#333333")
    draw_hangman(lives_left)
    update_display()
    # Re-enable all letter buttons
    for btn in letter_buttons.values():
        btn.config(state="normal")

def guess_letter(letter):
    """Processes the letter guessed by player."""
    global lives_left, game_over
    if game_over or letter in guessed_letters:
        return
    guessed_letters.append(letter)
    letter_buttons[letter].config(state="disabled")

    # Correct vs incorrect guess
    if letter in current_word:
        message_label.config(text="Good guess! '" + letter + "' is in the word.", fg="#2e7d32")
    else:
        lives_left -= 1
        draw_hangman(lives_left)
        message_label.config(text="Oops! '" + letter + "' is not there.", fg="#c62828")

    update_display()
    check_game_status()

def give_hint():
    """Reveals one random hidden letter at the cost of 1 life."""
    global lives_left
    if game_over:
        return
    if lives_left <= 1:
        message_label.config(text="Not enough lives for a hint! (Costs 1 life)", fg="#d84315")
        return

    remaining = []
    for char in current_word:
        if char not in guessed_letters and char not in remaining:
            remaining.append(char)

    if remaining:
        chosen = random.choice(remaining)
        lives_left -= 1
        draw_hangman(lives_left)
        message_label.config(text="Hint revealed: '" + chosen + "' (-1 life)", fg="#e65100")
        guessed_letters.append(chosen)
        letter_buttons[chosen].config(state="disabled")
        update_display()
        check_game_status()

def check_game_status():
    """Checks for win or loss conditions and updates scores."""
    global game_over
    # Check if all letters in current_word are guessed (Win)
    has_won = True
    for ch in current_word:
        if ch not in guessed_letters:
            has_won = False
            break

    if has_won:
        game_over = True
        stats["wins"] += 1
        stats["current_streak"] += 1
        if stats["current_streak"] > stats["best_streak"]:
            stats["best_streak"] = stats["current_streak"]
        save_highscores()
        update_display()
        message_label.config(text="🎉 You Won! Great job!", fg="#1b5e20")
        disable_all_buttons()
        return

    # Check if lives reached 0 (Loss)
    if lives_left <= 0:
        game_over = True
        stats["current_streak"] = 0
        save_highscores()
        update_display()
        word_label.config(text=" ".join(list(current_word)))
        message_label.config(text="💀 Game Over! The word was: " + current_word, fg="#b71c1c")
        disable_all_buttons()

def on_category_change(selected):
    """Starts a new game when user picks another category."""
    start_game()

# --- 4. GUI Window Setup & Layout ---
root = tk.Tk()
root.title("Word Guessing Game (Hangman)")
root.geometry("640x670")
root.resizable(False, False)
root.configure(bg="#f4f6f9")
load_words()
load_highscores()

# Top control bar: Category dropdown, New Game, and Hint button
top_frame = tk.Frame(root, bg="#e3e8ee", pady=8, padx=10)
top_frame.pack(fill="x")
tk.Label(top_frame, text="Category:", font=("Arial", 11, "bold"), bg="#e3e8ee").pack(side="left", padx=5)
categories = list(words_by_category.keys())
category_var = tk.StringVar(root, value=categories[0] if categories else "Animals")
category_menu = tk.OptionMenu(top_frame, category_var, *categories, command=on_category_change)
category_menu.config(font=("Arial", 10), bg="#ffffff")
category_menu.pack(side="left", padx=5)

new_game_btn = tk.Button(top_frame, text="New Game", font=("Arial", 10, "bold"),
                         bg="#1976d2", fg="white", padx=10, command=start_game)
new_game_btn.pack(side="right", padx=5)

hint_btn = tk.Button(top_frame, text="💡 Hint (-1 Life)", font=("Arial", 10),
                     bg="#ffb300", fg="#212121", padx=8, command=give_hint)
hint_btn.pack(side="right", padx=5)

# High scores & Lives status bar
stats_label = tk.Label(root, text="", font=("Arial", 10, "bold"), bg="#f4f6f9", fg="#455a64")
stats_label.pack(pady=(6, 0))

lives_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#f4f6f9", fg="#d32f2f")
lives_label.pack(pady=3)

# Canvas to draw Hangman figure
canvas = tk.Canvas(root, width=200, height=220, bg="#ffffff", highlightthickness=1, highlightbackground="#cfd8dc")
canvas.pack(pady=5)

# Display secret word blanks / letters
word_label = tk.Label(root, text="", font=("Consolas", 26, "bold"), bg="#f4f6f9", fg="#1a237e")
word_label.pack(pady=8)

# Result & feedback message
message_label = tk.Label(root, text="", font=("Arial", 11, "bold"), bg="#f4f6f9")
message_label.pack(pady=4)

# Keyboard buttons frame (A-Z)
keyboard_frame = tk.Frame(root, bg="#f4f6f9")
keyboard_frame.pack(pady=8)

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
row, col = 0, 0
for letter in letters:
    btn = tk.Button(keyboard_frame, text=letter, font=("Arial", 11, "bold"),
                    width=4, height=1, bg="#ffffff", fg="#263238",
                    activebackground="#90caf9", command=make_button_action(letter))
    btn.grid(row=row, column=col, padx=3, pady=3)
    letter_buttons[letter] = btn
    col += 1
    if col >= 9:
        col = 0
        row += 1

# Start the game and launch the event loop
start_game()
root.mainloop()
