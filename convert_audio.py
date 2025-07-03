import os
import sys
import json
from elevenlabs import ElevenLabs
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Set the API key from the environment variable
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    print("Please set the ELEVENLABS_API_KEY environment variable.")
    sys.exit(1)

# Initialize the ElevenLabs client with the API key
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def parse_dialog_ids(input_str):
    input_str = input_str.strip()
    if '-' in input_str:
        try:
            start, end = input_str.split('-')
            start, end = int(start.strip()), int(end.strip())
            return list(range(start, end + 1))
        except ValueError:
            print("Invalid range input.")
            sys.exit(1)
    elif ',' in input_str:
        try:
            return [int(x.strip()) for x in input_str.split(',')]
        except ValueError:
            print("Invalid list input.")
            sys.exit(1)
    else:
        try:
            return [int(input_str)]
        except ValueError:
            print("Invalid input.")
            sys.exit(1)

def convert_dialog_to_audio(dialog_text, voice_id, stability=0.5, similarity_boost=0.5):
    if not dialog_text:
        print("There is no dialog in this section.")
        return None
    try:
        
    
        audio_generator = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format="mp3_44100_128",
            text=dialog_text,
            model_id="eleven_multilingual_v2"
        )
        return audio_generator
    except Exception as e:
        print(f"Error during audio generation: {e}")
        return None

def main():
    try:
        with open("combined_script.json", "r", encoding="utf-8") as f:
            dialogs = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)

    ids_input = input("Enter the dialog ids to convert (e.g. '1-10' or '1,3,4,7'): ")
    dialog_ids = parse_dialog_ids(ids_input)

    selected_dialogs = [d for d in dialogs if d.get("id") in dialog_ids]
    if not selected_dialogs:
        print("No matching dialog ids found in the JSON file.")
        sys.exit(1)

    characters = set(d.get("character", "").strip() for d in selected_dialogs if d.get("character"))

    voice_mapping = {}
    for character in characters:
        env_var_name = f"VOICE_ID_{character.upper().replace(' ', '_')}"
        voice_id = os.getenv(env_var_name)
        if not voice_id:
            print(f"Please set the environment variable '{env_var_name}' for character '{character}'.")
            sys.exit(1)
        voice_mapping[character] = voice_id

    try:
        stability = float(input("Enter stability (default 0.3): ") or 0.3)
        similarity_boost = float(input("Enter similarity boost (default 0.5): ") or 0.5)
    except ValueError:
        print("Invalid parameter value. Using default values: stability=0.3, similarity_boost=0.5")
        stability = 0.3
        similarity_boost = 0.5

    for dialog in selected_dialogs:
        dialog_text = dialog.get("dialog", "").strip()
        dialog_id = dialog.get("id")
        character = dialog.get("character", "").strip()

        voice_id = voice_mapping.get(character)

        print(f"Processing dialog id {dialog_id} for character '{character}'...")
        audio_data = convert_dialog_to_audio(dialog_text, voice_id, stability, similarity_boost)
        if audio_data:
            output_dir = "generated_audio"
            os.makedirs(output_dir, exist_ok=True)
            file_path = os.path.join(output_dir, f"{dialog_id}_{character.replace(' ', '_')}.mp3")
            with open(file_path, "wb") as audio_file:
                for chunk in audio_data:
                    audio_file.write(chunk)
            print(f"Audio saved to {file_path}")
        else:
            print(f"Audio generation failed for dialog id {dialog_id}.")

if __name__ == "__main__":
    main()
