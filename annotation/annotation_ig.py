import json
import os
import platform

# Path to the input JSONL file
input_jsonl = 'ig-covid19-filtered_candidates_to_match_image.jsonl'
output_jsonl = 'annotated_ig_candidates_new.jsonl'

# Directory containing the image files
image_folder = 'instagram'

# Stance mapping
stances = {
    '1': 'Accept',
    '2': 'Reject',   
    '3': 'No Stance',
    '4': 'Not Relevant',
}

# Function to get stance input
def get_stance_input(platform_id, label_type):
    while True:
        print("\nStances: 1 - Accept, 2 - Reject, 3 - No Stance, 4 - Not Relevant")
        stance_choice = input(f"Enter stance number for {label_type} of platformId {platform_id}: ").strip()
        if stance_choice in stances:
            return stances[stance_choice]
        else:
            print("Invalid input. Please enter a valid stance number (1, 2, 3, 4).")

# Function to get reason input
def get_reason_input(platform_id, label_type):
    reason = input(f"Enter reason for {label_type} stance of platformId {platform_id}: ").strip()
    return reason

# Function to open image
def open_image(image_path):
    os.system(f'open "{image_path}"')

# Function to open image with possible suffixes
def open_image_with_suffix(image_folder, platform_id):
    suffixes = ['', '_0', '_1']
    for suffix in suffixes:
        image_name = f"{platform_id}{suffix}.jpg"
        image_path = os.path.join(image_folder, image_name)
        if os.path.exists(image_path):
            print(f"Opening image for platformId {platform_id}:", image_name)
            open_image(image_path)
            return
    print(f"No image found for platformId: {platform_id}")


# Find the last annotated platformId
def find_last_annotated_platform_id():
    last_platform_id = None
    if os.path.exists(output_jsonl):
        with open(output_jsonl, 'r') as file:
            for line in file:
                data = json.loads(line)
                last_platform_id = data.get('platformId', None)
    return last_platform_id

# Main annotation function
def annotate_data():
    last_platform_id = find_last_annotated_platform_id()
    start_annotating = False if last_platform_id else True

    with open(input_jsonl, 'r') as infile, open(output_jsonl, 'a') as outfile:
        for line in infile:
            data = json.loads(line)
            platform_id = data.get('platformId', 'Unknown')

            if platform_id == last_platform_id:
                start_annotating = True
                continue  # Skip the last annotated entry

            if not start_annotating or 'labels' in data:
                # Skip already annotated entries
                continue

            # Display the text
            print("\nText for platformId", platform_id, ": ", data.get('text', 'No text available'))

            open_image_with_suffix(image_folder, platform_id)

            # Get stance and reason input
            text_stance = get_stance_input(platform_id, "text")
            text_reason = get_reason_input(platform_id, "text")
            image_stance = get_stance_input(platform_id, "image")
            image_reason = get_reason_input(platform_id, "image")
            combined_stance = get_stance_input(platform_id, "combined text and image")
            combined_reason = get_reason_input(platform_id, "combined text and image")

            # Append labels and reasons to data and write to file
            data['labels_rakshita'] = {
                "text": text_stance,
                "image": image_stance,
                "combined": combined_stance
            }
            data['labels_reason_rakshita'] = {
                "text": text_reason,
                "image": image_reason,
                "combined": combined_reason
            }
            json.dump(data, outfile)
            outfile.write('\n')

# Run the annotation process
try:
    annotate_data()
    print("Annotation session completed.")
except KeyboardInterrupt:
    print("\nAnnotation session interrupted. Progress saved up to this point.")
