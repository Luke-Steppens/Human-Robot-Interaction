import tkinter as tk
import time
import queue
from arduino_control import ArduinoController


# Each game lasts 2 minutes then has game over
GAME_LENGTH = 120  # 2 minutes

arduino = None


ARDUINO_PORT = "COM4"  # check this every session !!!!!



"""
==============================
  SHARED GAME STATE VARIABLES
==============================
"""

# test variables
heard_text = "Listening..."
final_movement = 0
final_score = 0.0

# start time
session_start = None


game_running = False

game_over = False

status_msg = ""

update_q = queue.Queue()

# for final scoring
corner_pos = 0
laps = 0


"""
==============================
  HELPER FUNCTIONS
==============================
"""

# movement labels
def movement_label(movement):
    return {
        2: "Very Polite",
        1: "Polite",
        0: "Neutral",
        -1: "Urgent",
        -2: "Very Urgent",
    }.get(movement, "Unknown")

# corners labelled for point scoring purposes
def corner_label(pos):
    return {
        0: "A",
        1: "B",
        2: "C",
    }.get(pos, "?")




"""
==============================
  SCREEN CHANGE FUNCTIONS
==============================
"""

def tabula_rasa():
    global session_start, heard_text, final_movement, final_score, status_msg, laps, corner_pos

    session_start = None
    heard_text = "Listening..."
    final_movement = 0
    final_score = 0.0
    laps = 0
    corner_pos = 0
    step_progress = 0
    status_msg = "Previous session data cleared (Not Stored)"

def start_screen():
    start_status.config(text=status_msg)
    start_frame.tkraise()

def start_game():
    global session_start, game_running, game_over, status_msg, arduino

    if game_running:
        return  # space no longer starts game as its already running
    
    status_msg =""
    game_over = False
    game_running = True
    session_start = time.time()
    
    if arduino is None:
        arduino = ArduinoController(ARDUINO_PORT)
    
    game_frame.tkraise()
    update_ui() # Start updating the UI


def on_space(e):
    global game_over

    if game_over:
        tabula_rasa()
        start_screen()
        game_over = False
    else:
        start_game()


"""
==============================
  UI UPDATE & TIMER
==============================
"""


# Update the UI with current game state
def update_ui():
    if session_start is None:
        return  # Game hasn't started yet
    global heard_text, final_movement, final_score, corner_pos, laps

    elapsed = time.time() - session_start
    remaining = max(0, GAME_LENGTH - elapsed)
    mins = int(remaining // 60)
    secs = int(remaining % 60)

    screen_text = (
        f"Game Time Remaining: {mins:02}:{secs:02}\n\n"
        f"Heard:\n{heard_text}\n\n"
        f"Polite State: {movement_label(final_movement)}\n"
        f"Sentence score: {final_score:.2f}\n\n"
        f"Laps Completed: {laps}\n\n"
        f"Ball Position: Corner {corner_label(corner_pos)}\n\n"
        f"Tip: Please speak one sentence at a time to receive a score."

    )


    # update the text until time runs out
    label.config(text=screen_text)

    if remaining > 0:
        root.after(100, update_ui)
    else:
        label.config(text= "Game Over!\n\n"
        f" High Score this round: {laps} laps!!\n\n"
        "Congratulations!\n\n"
        "Thank you for playing\n\n Press SPACE to return to the start screen.")
        global game_running, game_over
        game_running = False
        game_over = True

def poll_updates():
    
    """
    - UI update loop
    - reads movement commands from speach thread (update_q)
    - sends to arduino to move the plate
    """
    global heard_text, final_movement, final_score, laps, corner_pos

    while True:
        try:
            msg = update_q.get_nowait()
        except queue.Empty:
            break
        if game_running:
            heard_text = msg.get("text", heard_text)
            final_movement = msg.get("final_movement", final_movement)
            final_score = msg.get("final_score", final_score)

            
            mv = final_movement
            
            
            # send mv (-2 to +2) to arduino
            # arduino then moves the plate
            global arduino
            if arduino is not None and mv in (2, 1, -1, -2):
                arduino.send_cmd(mv)

            
            if mv != 0:
                direction = 1 if mv > 0 else -1
                steps = abs(mv)

                for _ in range(steps):
                    prev = corner_pos
                    corner_pos = (corner_pos + direction) % 3

                    # laps for mirroring physical circuit
                    # score only when arriving or passing corner A
                    if direction == 1 and (prev == 2 and corner_pos == 0):
                        laps += 1
            update_ui()
    root.after(50, poll_updates)

"""
==============================
  DEMO / TEST FUNCTIONS
==============================
"""
# demo for when no access to arduino

# make sure update for speech changes
def demo_test():
    global heard_text, final_movement, final_score
    heard_text = "would you mind moving the ball please"
    final_movement = 2
    final_score = 1.5







"""
==============================
      TKINTER UI SETUP 
==============================
"""
def init_ui():
    global root, start_frame, game_frame, start_status, label

    root = tk.Tk()
    root.title("COMP304 Screen UI")
    root.attributes("-fullscreen", True)
    root.configure(bg="white")

    container = tk.Frame(root, bg="white")
    container.pack(fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    start_frame = tk.Frame(container, bg="white")
    start_frame.grid(row=0, column=0, sticky="nsew")

    game_frame = tk.Frame(container, bg="white")
    game_frame.grid(row=0, column=0, sticky="nsew")

    start_title = tk.Label(
        start_frame,
        text="Welcome to the Politeness Machine",
        font=("Arial Rounded MT Bold", 34),
        fg="#1B7F5A",
        bg="white",
        justify="center",
    )
    start_title.pack(pady=(60, 30))

    start_rules = tk.Label(
        start_frame,
        text=(
            "Instructions:\n\n"
            "1. Move the ball around the circuit with your voice.\n"
            "   Each full lap scores one point.\n\n"

            "2. How you speak matters.\n"
            "   The calmer and more polite you speak,\n"
            "   the further you will move.\n\n"

            "3. Speak one sentence at a time.\n\n"

            "4. Microphone will activate when you start the game.\n\n"

            "5. You have two minutes, good luck!"

        ),
        font=("Arial Rounded MT Bold", 24),
        fg="#444444",
        bg="white",
        justify="left",
    )
    start_rules.pack(padx=80, pady=20)

    start_prompt = tk.Label(
        start_frame,
        text="Press SPACE to begin",
        font=("Arial Rounded MT Bold", 28),
        fg="#1B7F5A",
        bg="white",
    )
    start_prompt.pack(pady=(30, 0))

    start_status = tk.Label(
        start_frame,
        text="",
        font=("Arial Rounded MT Bold", 18),
        fg="blue",
        bg="white",
    )
    start_status.pack(pady=(10, 0))

    label = tk.Label(
        game_frame,
        text="",
        font=("Arial Rounded MT Bold", 30),
        fg="green",
        bg="white",
        justify="left",
        anchor="nw",
    )
    label.pack(fill="both", expand=True, padx=50, pady=50)
    
    root.bind("<Escape>", lambda e: root.destroy()) # escape to exit
    root.bind("<space>", on_space)  # advance through screens with space
    root.bind("<d>", lambda e: demo_test()) # d to demo test






