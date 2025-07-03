import fitz  # PyMuPDF
import base64
import json
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

def convert_pdf_to_images(pdf_document):
    """
    Converts a PDF file into a list of image file paths (one per page).
    """
    doc = fitz.open(pdf_document)
    image_paths = []
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        pix = page.get_pixmap(dpi=200)
        output = f"page_{page_number+1}.png"
        pix.save(output)
        print(f"Saved {output}")
        image_paths.append(output)
    return image_paths

def encode_image(image_path):
    """
    Encodes an image file to a base64 string.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def extract_json_from_image(image_path, client, squence_boolean):
    """
    Sends an image to the OpenAI vision endpoint and returns the extracted JSON.
    The prompt instructs the model to extract the character name, action, and dialog
    from the play script image.
    """
    base64_image = encode_image(image_path)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""This is a png file of a play script, you are tasked to extract the character name, the action and the dialog and convert it into a json output under a list name "lines", each roll of the script represent the sequence of the line, when one roll have two characters and lines run in parallel, it indicate the two characters will speak at the same time. Add "squence" to the data output with a boolean "1" and "0", each roll will switch betwern 1 and 0, if two or more people speak together, they share the same number to indicate they should speak together, the sequence start with "{squence_boolean}" 
                                   The following is an example of the output:
    
      "squence": "",
      "character": "",
      "action": "",
      "dialog": ""
    
                        """
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )
    
    # Assuming the model returns a JSON string in response.choices[0].message.content.
    
    json_output = response.choices[0].message.content
    
    try:
        page_json = json.loads(json_output)
    except json.JSONDecodeError:
        print(f"Error decoding JSON for {image_path}")
        page_json = []
    return page_json

def combine_page_json(page_json_list):
    """
    Combines a list of page JSON outputs (each being a dictionary with a "lines" key)
    into a single JSON object containing all lines.
    """
    combined_json = []
    for page_json in page_json_list:
        lines = page_json.get("lines", [])
        combined_json.extend(lines)
    return {"lines": combined_json}

def add_ids_and_cues_to_json(input_json, client):
    """
    Uses the OpenAI API to process the JSON output and add an "id" field (with continuous numbering)
    before the "character" field and also add a "cue" field. The "cue" is determined by extracting trigger words
    from the end of the "dialog" field. If the last word appears elsewhere in the dialog, include the preceding word(s)
    until a unique trigger is found. Trivial words such as "huh", "wow", and "ha ha" should be avoided.
    """
    system_prompt = (
        """You are an expert at processing play scripts. 
        Given the following JSON input which contains a 'lines' array, update each entry as follows:\n"
        1. Add an 'id' field before "character" with a number starting at 1, incrementing by 1 for each entry, placed before the 'character' field.\n"
        2. Add a new 'emotion' field after the "dialog" , based on the scene and the story, assign an emotion adjective to describe the voice of that line (such as angrily, peacefully, happyily etc)
        3. Add a new field called 'cue' at the end. The 'cue' is a trigger word or phrase extracted from the end of the 'dialog'.\n"
        "   The cue should normally be the last word of the dialog. However, if that word appears elsewhere in the dialog (at the start or in the middle), "
        "append the preceding word until a unique trigger phrase is found. If two words are not enough, add three and so on. "
        "The cue should not be a name , punctuation mark or a trivial word such as 'huh', 'wow', or 'ha ha'.\n"
        "The cue should be all in lower case"
        "Return the updated JSON output with the new fields for each line.
        """
    )
    
    user_message = f"Input JSON:\n```json\n{json.dumps(input_json, indent=2)}\n```"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        response_format={"type": "json_object"},
        messages=[
            {  "role": "developer",
               "content": system_prompt
               },
            {
                "role": "user",
                "content":  user_message
                }
                    
                ],
            
    )
    
    output_json_str = response.choices[0].message.content
    
    try:
        output_json = json.loads(output_json_str)
    except Exception as e:
        print("Error decoding JSON output:", e)
        output_json = output_json_str
    return output_json


def main():
    # Path to your PDF file
    pdf_document = "TECHNICIAN.pdf"
    
    # Initialize the OpenAI client (ensure proper configuration)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Convert PDF pages to images
    image_paths = convert_pdf_to_images(pdf_document)
    
    # Process each image to extract JSON data
    all_page_json = []
    squence_boolean = 0
    for image_path in image_paths:
        page_json = extract_json_from_image(image_path, client, squence_boolean)
        all_page_json.append(page_json)
        if squence_boolean == 0:
            squence_boolean = 1
        else:
            squence_boolean = 0
    
    # Combine the JSON outputs from all pages into one list with continuous IDs
    combined_json = combine_page_json(all_page_json)

    # Process the JSON outputs to add ids, emotion and cues
    updated_json = add_ids_and_cues_to_json(combined_json, client)
    
    # Save the combined JSON to a file
    output_filename = "combined_script.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(updated_json, f, indent=4)
    
    print(f"Saved combined JSON to {output_filename}")

if __name__ == "__main__":
    main()
