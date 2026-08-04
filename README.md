# COMP304 - Human Robot Interaction

<p align="center">
  <img src="COMP304-Human-Robot-Interaction-main/Documentation/Photo & Diagrams/assembly.png" width="600">
</p>

<p align="center">
  <img src="COMP304-Human-Robot-Interaction-main/Documentation/Photo & Diagrams/SV.jpeg" width="600">
</p>

## Overview

This repository contains all the resources, source code, and documentation for my COMP304 Human-Robot Interaction project.
The project uses a custom robotic system in conjunction with soft computing techniques to create an adaptive interaction between human and machine, where the machine can adapt to the human interlocutor's behaviour and respond. This will be implemented by focusing on affective computing and emotional engagement. 

The system presents a timed game in which users move a ball around a triangular circuit using spoken key words. Speech is analysed in real-time locally to assess politeness and pacing. The calmer and more polite speech results in greater movement and higher scores.



## Objectives

- To design and build a moving platform that is able to manipulate a triangular-shaped plate upon it.
- Control the position of the plate to allow the ball to move from point to point.
- Enable voice interaction so the system can listen to user instructions.
- Apply fuzzy logic to evaluate politeness cues.
- Show the adaptability of the system.

## Repository Structure

/code
- Arduino control code
- Speech recognition and fuzzy logic evaluation
- User interface code

/construction
- CAD files
- Technical Drawings

/documentation
- Photos & Diagrams
- Video Link

/Poster
- Poster PDF


## System Setup

### Python Dependencies

Python 3.11.9 is recommended.

Install the required Python packages using pip:

pip install vosk
pip install pyaudio
pip install numpy

## Hardware

- Laptop / Desktop PC
- Arduino
- Universal joints
- PLA
- Table Tennis Ball
- Microphone
- MG-996R Servos

  
## Software

- **Arduino IDE** – Used for programming the Arduino microcontrollers  
  https://www.arduino.cc/en/software/

- **Visual Studio Code** – Primary code editor used for development  
  https://code.visualstudio.com/download

- **Vosk Speech Recognition Models** – Offline speech recognition models used for voice input  (English 0.15)
  https://alphacephei.com/vosk/models

- **Autodesk Fusion 360** – Used for CAD design   
  https://www.autodesk.com/uk/products/fusion-360/overview


## How to Run

- Check the Arduino serial port and assign it in `screen_ui.py` (e.g., COM4).
- Under SPEECH PROCESSING FUNCTIONS in `speech_test_1.py` assign your microphone and computer
- Use the run button run_system.py to begin the program.

## Gamepley Instruction
- Press the space bar to start the game.
- The game runs for a total of 2 minutes.
- Speak simple sentences to move the ball counterclockwise around the triangular circuit.
- Polite and calm speech will result in higher movement amounts and higher lap counts.
- Impolite and urgent speech will result in the ball moving backwards (clockwise), losing the user's time.
- Complete as many laps as you can in the time frame.
- Escape will exit the UI.

## Scoring System

- Spoken utterances are evaluated for politeness and pacing using fuzzy logic.
- Each utterance will create a movement score netting a movement of -2, -1, 0, 1, 2 places on the circuit.
- Positive scores move the ball forward.
- Negative scores move the ball backward.
- Travel around the circuit one whole time equals one lap.



## Cybersecurity

- This project uses VOSK with Python. All processing is done at runtime locally and does not require a connection to the internet. No files or sound data are stored on the user's computer or online by VOSK, as the raw speech data is accessed within RAM and then overwritten with each new transcription.
- The user does not provide any personal data to the system. The voice is used to create a short sentence, which is immediately abstracted into a numerical politeness score between -2.0 and +2.0. The final score is given in laps and bears no resemblance to the original voice input.
- The speech recognition software uses pre-trained models loaded from the disk and does not create any logs during use. The recogniser processes voice data as a live stream. After the score has been given, the RAM is released and ready for reuse.


## Limitations

- Politeness is evaluated using a small and limited, rule-based set of linguistic cues.
- The interaction is intentionally simplified and does not reflect the full complexity of real-world HRI.
- The system can be gamed, although this still reinforces polite speech behaviour.
- The version of VOSK used for this project traded precision transcription for speed of output, leading to inaccurate conversions of speech to text.






## License

© 2026 Luke Steppens. All rights reserved except where otherwise noted.

This project is licensed under the Creative Commons 
Attribution–NonCommercial 4.0 International License (CC BY-NC 4.0).

You may share and adapt the material for non-commercial purposes, 
provided appropriate credit is given.
