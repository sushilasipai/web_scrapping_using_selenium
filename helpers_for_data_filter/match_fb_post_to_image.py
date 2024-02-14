import os
import json

def find_missing_posts(jsonl_path, image_folder, output_file):
    missing_images = []

    # Get list of platformIds from the JSONL file
    platform_ids = set()
    with open(jsonl_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            platform_id = data.get('platformId')
            platform_ids.add(platform_id)

    # Get list of image filenames in the image_folder
    image_filenames = os.listdir(image_folder)

    # Check for images without corresponding posts
    for image_filename in image_filenames:
        # Extract platformId from image filename
        platform_id, extension = os.path.splitext(image_filename)
        if platform_id not in platform_ids:
            # Check if image filename matches the specific pattern
            if platform_id.endswith('_0') or platform_id.endswith('_1'):
                platform_id = platform_id.rsplit('_', 1)[0]  # Remove the '_0' or '_1' part
                if platform_id not in platform_ids:
                    missing_images.append(image_filename)

    # Write missing image filenames to output file
    with open(output_file, 'w') as output:
        for image_name in missing_images:
            output.write(image_name + '\n')

if __name__ == "__main__":
    jsonl_path = 'posts_without_images.jsonl'  # Replace with actual path to your JSONL file
    image_folder = 'facebook'  # Replace 'your_image_folder' with the path to your image folder
    output_file = 'missing_images.txt'  # Path to the output file to write the missing image names

    find_missing_posts(jsonl_path, image_folder, output_file)

    print("Missing image names written to:", output_file)
