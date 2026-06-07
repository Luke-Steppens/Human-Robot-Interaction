from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json, queue, sys
import time




"""
==============================
  FUZZY LOGIC FUNCTIONS
==============================
"""

def triangular_membership(x, a, b, c):
    """
    Trianglualr membership
    a = left (beginning)
    b = peak (membership = 1)
    c = right (end)
    
    Return a value between 0 and 1
    """
    if x <= a or x >= c:
        return 0.0
    elif x == b:
        return 1.0
    elif x < b:
        return (x - a) / (b - a)
    else: # x > b
        return (c - x) / (c - b)
        

def get_wps_category(wps):
    """
    Takes a WPS value and returns membership values for slow, normal, and fast
    """
    slow = triangular_membership(wps, 0, 0.8, 1.5)
    normal = triangular_membership(wps, 1.3, 2.3, 3.2)
    fast = triangular_membership(wps, 2.8, 4.0, 5.0)
    return {"Slow": slow, "Normal": normal, "Fast": fast}

def wordtone_category(text):
    """
    check text return fuzzy tone scores
    """
    polite_words = ["please",
                    "could you",
                    "would you",
                    "thank you",
                    "excuse me",
                    "would you mind",
                    "would it be possible",
                    "Pretty please"]
    urgent_words = ["now",
                    "hurry",
                    "quickly",
                    "immediately",
                    "faster",
                    "hey",
                    "right away",
                    "come on",
                    "go",
                    "asap"]
    
    
    text = text.lower()
    polite = sum(1 for w in polite_words if w in text)
    urgent = sum(1 for w in urgent_words if w in text)
    
    # Context change "move" modifies words its with, makes urgent words more urgent etc
    if "move" in text and any(u in text for u in urgent_words):
        urgent += 1
        
        
    # Normalise keyword counts to fuzzy membership values in the range [0, 1]
    polite_score = min(polite / 2, 1.0)
    urgent_score = min(urgent / 2, 1.0)
    neutral_score = max(0.0, 1.0 - (polite_score + urgent_score))
    
    return {"polite": polite_score, "neutral": neutral_score, "urgent": urgent_score}

def map_wps_to_movement(dom_label):
    """
    Slow  +1 (forward)
    Normal 0 (still)
    Fast  -1 (backward)
    """
    if dom_label == "Slow":
        return +1
    elif dom_label == "Normal":
        return 0
    elif dom_label == "Fast":
        return -1
    return 0



"""
==============================
  AUDIO MODEL SETUP            (Choose laptop or desktop)
==============================
"""

# list of audio devices (keep this will need to change on laptop)
print("\nAvailable audio devices:\n")
print(sd.query_devices())


# address location Desktop
model_path = r"C:\Users\Luke\Desktop\HRI AUDIO\vosk-model-small-en-us-0.15"

# address location Laptop
# model_path = r"C:\Users\dubhe\Desktop\3rd Year Offline\vosk-model-small-en-us-0.15"


SAMPLE_RATE = 16000

model = Model(model_path)
rec = KaldiRecognizer(model, SAMPLE_RATE)
audio_q = queue.Queue()


"""
==============================
  SPEECH PROCESSING FUNCTIONS   (Choose laptop or desktop)
==============================
"""

def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    audio_q.put(bytes(indata))


#  Says how to stop recording and which device is being used
DEVICE_INDEX = 3      # 3 = Desktop Yeti mic, 5 = Laptop Mic
device_info = sd.query_devices(DEVICE_INDEX)
device_name = device_info["name"]
print(f"Listening via {device_name} (device {DEVICE_INDEX}). Press Ctrl+C to stop.")


# When speech starts and if currently speaking
speech_start_ms = None
speaking = False



"""
==============================
  MAIN PROGRAM LOOP
==============================
"""

# runs vosk loop and sends results to out_q
def run_voice_loop(out_q):
    
    """
    - This part runs in the background
    - converts live speech into movement commands (-2  to +2) and sends to UI via the queue
    """
    
    global speaking, speech_start_ms
    try:
        with sd.RawInputStream(device=DEVICE_INDEX, samplerate=SAMPLE_RATE, blocksize=8000,
                            dtype='int16', channels=1, callback=audio_callback):
            while True:
                data = audio_q.get()
                
                # mark speaking starts
                if not speaking:
                    speech_start_ms = time.time_ns() // 1_000_000 # current time milliseconds
                    speaking = True
                
                # call waveform once    
                got_final = rec.AcceptWaveform(data)
                
                if got_final:
                    result = json.loads(rec.Result())
                    text = result.get("text","")
                    
                    # mark end of speech
                    end_ts_ms = time.time_ns() // 1_000_000
                    speaking = False # this resets ready for next speech
                    
                    # calculate how long speech lasted
                    duration_ms = end_ts_ms - speech_start_ms
                    
                    # fix casing and spacing of words
                    text = " ".join(text.strip().lower().split())
                    
                    # stop undefined variables
                    final_score = 0.0
                    final_movement = 0
                    tone_score = 0.0
                    wps_score = 0.0
                    
                    # removes short sounds
                    min_duration_ms = 400  # tweak if needed
                    
                    
                    # show results
                    if text and duration_ms >= min_duration_ms:
                        
                        # split the text into words and count them
                        word_count = len(text.split())
                        
                        # convert into seconds then calculate words per second
                        duration_s = duration_ms / 1000
                        wps = word_count / duration_s if duration_s > 0 else 0 
                        
                        
                        # get fuzzy memberships
                        categories = get_wps_category(wps)
                        
                        # get tone/meaning
                        tone = wordtone_category(text)

                        # combined score (tone weighted more than speed)
                        # WPS score (-1 to +1) Slow = +1, Normal = 0, Fast = -1
                        wps_score = (
                            categories["Slow"] * 1 +
                            categories["Normal"] * 0 +
                            categories["Fast"] * -1
                        )

                        # Tone score (-1 to +1) Polite = +1, Neutral = 0, Urgent = -1
                        tone_score = (
                            tone["polite"] * 1 +
                            tone["neutral"] * 0 +
                            tone["urgent"] * -1
                        )

                        # fused final score
                        final_score = (1.5 * tone_score) + (0.5 * wps_score)

                        # mapped to movement
                        if final_score >= 1.0:
                            final_movement = 2 # very polite
                        elif final_score >= 0.3:
                            final_movement = 1 #polite
                        elif final_score > -0.3:
                            final_movement = 0 # neutral
                        elif final_score > -1.0:
                            final_movement = -1 # urgent
                        else:
                            final_movement = -2 # very urgent
                        

                        if out_q is not None:
                            out_q.put({
                                "text": text,
                                "final_score": final_score,
                                "final_movement": final_movement,
                            })


                        # find dominant fuzzy label and map it to movement
                        dom_label, dom_value = max(categories.items(), key=lambda kv: kv[1])
                        wps_movement = map_wps_to_movement(dom_label)
                        
                        # send movement instructions to arduino
                        #arduino.write(movement.encode())               #<<<<<<


                        # print in a column not horizontal
                        print("\n--- Spoken Input ---")
                        print(f"Text: {text}")
                        print(f"Start (ms): {speech_start_ms}")
                        print(f"End (ms): {end_ts_ms}")
                        print(f"Duration (ms): {duration_ms}")
                        print(f"Word count: {word_count}")
                        print(f"WPS: {wps:.2F}") # to 2 decimal points
                        
                        print("\nFuzzy WPS Categories:")
                        for label, value in categories.items():
                            print(f"  {label}: {value:.2f}")
                            
                        print(f"\nSpeech speed (dominant): {dom_label} ({dom_value:.2f})")
                        print(f"\nFinal movement: {final_movement}  #+2 very Polite, +1 Polite, 0 Neutral, -1 Impolite, -2 very Impolite")
                        print(f"WPS-only movement (debug): {wps_movement}  # + forward, - backward")
                        print(f"final_score: {final_score:.2f}  (tone_score={tone_score:.2f}, wps_score={wps_score:.2f})")


                        print("\nWord Tone analysis:")
                        for label, value in tone.items():
                            print(f"  {label}: {value:.2f}")
                        print("-----------------\n")
                        
                        


    except KeyboardInterrupt:
        print("\nStopped.")
