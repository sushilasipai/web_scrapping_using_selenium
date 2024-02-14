import os
import json

def filter_posts_without_images(jsonl_path, image_folder, output_jsonl_without_images):
    # Get a list of image filenames in the image_folder
    image_filenames = os.listdir(image_folder)

    # Create a set of image names without extension
    image_names = {os.path.splitext(image)[0] for image in image_filenames}

    # Initialize a list to store posts without images
    posts_without_images = []

    # Filter out posts that have no corresponding images
    with open(jsonl_path, 'r') as jsonl_file:
        for line in jsonl_file:
            data = json.loads(line)
            platform_id = data.get('platformId')
            if platform_id not in image_names:
                posts_without_images.append(data)

    # Write posts without corresponding images to output file
    with open(output_jsonl_without_images, 'w') as output_file:
        for post in posts_without_images:
            output_file.write(json.dumps(post) + '\n')

if __name__ == "__main__":
    jsonl_path = 'fb-covid19-frame-rel-v1_candidates_bak.jsonl'
    image_folder = 'facebook'
    output_jsonl_without_images = 'posts_without_images.jsonl'

    filter_posts_without_images(jsonl_path, image_folder, output_jsonl_without_images)

    print("Filtered posts without corresponding images saved to:", output_jsonl_without_images)
