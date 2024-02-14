import os
import json

# Directory containing the image files
image_folder = 'facebook'

# Path to the input and output JSONL files
input_jsonl = 'fb-covid19-frame-rel-v1_candidates_bak.jsonl'
output_jsonl = 'fb-covid19-filtered_candidates.jsonl'

# Read the names of image files
image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

# Function to extract platform ID from image file name
def extract_platform_id(filename):
   return os.path.splitext(filename)[0]

# Set to keep track of processed platform IDs
processed_ids = set()

# Open the output file
with open(output_jsonl, 'w') as outfile:
    # Read the input JSONL file
    with open(input_jsonl, 'r') as infile:
        for line in infile:
            data = json.loads(line)
            # Assuming there's a field 'platform_id' in the JSON data
            platform_id = data.get('platformId')
            if platform_id and platform_id not in processed_ids:
                for image_file in image_files:
                    extracted_id = extract_platform_id(image_file)
                    if extracted_id == platform_id:
                        # Write the matching data to the output file and add to processed set
                        json.dump(data, outfile)
                        outfile.write('\n')
                        processed_ids.add(platform_id)
                        break  # Break the loop once a match is found