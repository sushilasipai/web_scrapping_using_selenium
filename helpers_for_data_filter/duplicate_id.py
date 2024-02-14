import json

def check_for_duplicate_platformid(file_path):
    platform_ids = set()
    duplicates = set()
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            platform_id = data.get('platformId')
            if platform_id:
                if platform_id in platform_ids:
                    duplicates.add(platform_id)
                else:
                    platform_ids.add(platform_id)
    
    if duplicates:
        print(f"Duplicate platformIds found: {duplicates}")
        return True
    else:
        print("No duplicate platformIds found.")
        return False

# Replace 'yourfile.jsonl' with the path to your JSONL file
check_for_duplicate_platformid('annotated_fb_candidates.jsonl')
