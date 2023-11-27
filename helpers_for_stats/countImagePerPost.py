import json
import os

def calculate_image_count_statistics(jsonl_file_path, image_directory):
    image_counts = {}

    with open(jsonl_file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            platform_id = data.get('platformId')

            # Count images starting with the platformId
            count = sum(1 for fname in os.listdir(image_directory) if fname.startswith(platform_id))
            image_counts[count] = image_counts.get(count, 0) + 1

    return image_counts

# Example usage
image_stats = calculate_image_count_statistics('../ig-covid19-frame-rel-v1_candidates_bak.jsonl', 
                                               '../instagram')
print(image_stats)

