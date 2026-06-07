import threading
import screen_ui
import speech_test_1



"""
System flow

- run_voice_loop()  runs in the background, listens for speech
- fuzzy logic added to final_movement (-2 to +2)
- final_movement sent to ui using a queue
- poll_updates() reads the queue and sends movement instruction to the arduino
- Arduino recives cmd and moves the ball
"""



def main():

    # initalise all UI elements
    screen_ui.init_ui()


    # run speech to text in separate thread
    t = threading.Thread(
        target=speech_test_1.run_voice_loop,
        args=(screen_ui.update_q,),
        daemon=True
    )
    t.start()
    
    # start polling for updates to UI
    screen_ui.start_screen()
    screen_ui.poll_updates()

    # start the tkinter main loop
    screen_ui.root.mainloop()

# for testing ui only
def run_ui():
    screen_ui.start_screen()
    screen_ui.poll_updates()
    screen_ui.root.mainloop()

if __name__ == "__main__":
    main()