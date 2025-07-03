import speech_recognition as sr
import json
import threading
import pygame
import time

# Initialize pygame mixer for audio playback.
pygame.mixer.init()

def play_response_audio(audio_file):
    try:
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        # Wait for the audio to finish playing.
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print(f"Error playing sound: {e}")

def main():
    # Load the full play script JSON.
    with open("script_example.json", "r", encoding="utf-8-sig") as f:
        play_script = json.load(f)
    
    selected_character = "LOUISE"
    
    # Find the first event in the full script for the selected character with a non-empty trigger.
    current_index_full = None
    for i, event in enumerate(play_script):
        if event.get("character", "").strip().upper() == selected_character.upper() and event.get("trigger", "").strip() != "":
            current_index_full = i
            break
    if current_index_full is None:
        print(f"No events found for character {selected_character} with triggers.")
        return

    # Function to display the current event's expected dialog and trigger.
    def display_current_event():
        if current_index_full is not None and current_index_full < len(play_script):
            event = play_script[current_index_full]
            print(f"\nNext dialog for {selected_character}:")
            print(f"    Dialog: {event['dialog']}")
            print(f"    (Say the trigger word: '{event['trigger']}')\n")
        else:
            print("\nAll events have been triggered!\n")
    
    # Display the first event prompt.
    display_current_event()
    
    # Set up the recognizer and microphone.
    r = sr.Recognizer()
    mic = sr.Microphone()
    
    # A list to store recognized audio chunks (if needed).
    transcript_list = []
    
    # This function plays subsequent audio files until it finds the next event for the chosen character.
    def play_next_audios():
        nonlocal current_index_full
        i = current_index_full + 1
        while i < len(play_script):
            event = play_script[i]
            # If the event does not belong to the chosen character, play its audio.
            if event.get("character", "").strip().upper() != selected_character.upper():
                char_name = event['character'].upper().replace(" ", "_")
                audio_file = f"generated_audio\{event['id']}_{char_name}.mp3"
                print(f"Playing audio: {audio_file}")
                play_response_audio(audio_file)
                i += 1
            else:
                # Reached an event for the chosen character.
                current_index_full = i
                display_current_event()
                return
        # No further events for the chosen character.
        current_index_full = len(play_script)
        print("\nAll events have been triggered!\n")
    
    # Callback function for background listening.
    def callback(recognizer, audio):
        nonlocal current_index_full
        try:
            text = recognizer.recognize_google(audio)
            print("Chunk transcription:", text)
            transcript_list.append(text)
            text_lower = text.lower()
            
            # Only check the trigger for the current event.
            if current_index_full is not None and current_index_full < len(play_script):
                current_trigger = play_script[current_index_full]["trigger"].lower()
                if current_trigger in text_lower:
                    event = play_script[current_index_full]
                    print("\n--- Trigger Detected for Current Event ---")
                    print("Dialog:", event["dialog"])
                    print("Actions:", event["actions"])
                    print("------------------------------------------\n")
                    
                    # Construct the audio file name for the current event.
                    char_name = event['character'].upper().replace(" ", "_")
                    audio_file = f"generated_audio\{event['id']}_{char_name}.mp3"
                    
                    print(f"Playing audio: {audio_file}")
                    threading.Thread(
                        target=play_response_audio, 
                        args=(audio_file,), 
                        daemon=True
                    ).start()
                    
                    # Now play subsequent audios (for non-chosen characters) until reaching the next event for the chosen character.
                    threading.Thread(target=play_next_audios, daemon=True).start()
                    
                    transcript_list.clear()
        except sr.UnknownValueError:
            print("Could not understand audio chunk.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
    
    input("Press Enter to start recording...")
    stop_listening = r.listen_in_background(mic, callback)
    print("Recording... Press Enter to stop recording.")
    input()
    stop_listening(wait_for_stop=False)
    print("Stopped recording.")

if __name__ == "__main__":
    main()
