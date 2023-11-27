import os
import json

def check_images_and_log_missing(jsonl_file_path, image_directory, video_directory, log_file_path):
    with open(jsonl_file_path, 'r') as jsonl_file, open(log_file_path, 'w') as log_file:
        for line in jsonl_file:
            data = json.loads(line)
            platform_id = data.get('platformId')
            image_exists = any(fname.startswith(platform_id) for fname in os.listdir(image_directory))

            video_exists = any(fname.startswith(platform_id) and fname.endswith('.mp4') for fname in os.listdir(video_directory))

            if not (image_exists or video_exists):
                json.dump(data, log_file)
                log_file.write('\n')


check_images_and_log_missing('../fb-covid19-frame-rel-v1_candidates_bak.jsonl', '../facebook', '../facebook_videos', '../failedToDownload.jsonl')
