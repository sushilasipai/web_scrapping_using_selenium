import os
import json

def filter_posts_with_images(jsonl_path, image_folder, output_jsonl):
    # Get a list of image filenames in the image_folder
    image_filenames = os.listdir(image_folder)

    # Create a set of image names without extension
    image_names = {os.path.splitext(image)[0] for image in image_filenames}

    # Filter out posts that have corresponding images
    with open(jsonl_path, 'r') as jsonl_file, open(output_jsonl, 'w') as output_file:
        for line in jsonl_file:
            data = json.loads(line)
            platform_id = data.get('platformId')
            if platform_id in image_names:
                output_file.write(json.dumps(data) + '\n')

if __name__ == "__main__":
    jsonl_path = 'fb-covid19-frame-rel-v1_candidates_bak.jsonl'
    image_folder = 'facebook'
    output_jsonl = 'posts_with_images.jsonl'

    filter_posts_with_images(jsonl_path, image_folder, output_jsonl)

    print("Filtered posts with corresponding images saved to:", output_jsonl)
