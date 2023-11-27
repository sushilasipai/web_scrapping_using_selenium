import json
import numpy as np

def calculate_video_length_statistics(jsonl_file_path):

    video_lengths = []

    with open(jsonl_file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            video_length = data.get('videoLengthMS', 0)
            if video_length:  # Ensure that the video length is not None or 0
                video_lengths.append(video_length)

    if not video_lengths:
        return {
            "min_length": None,
            "max_length": None,
            "avg_length": None,
            "quartiles": None
        }

    min_length = min(video_lengths)
    max_length = max(video_lengths)
    avg_length = np.mean(video_lengths)
    quartiles = np.percentile(video_lengths, [25, 50, 75])

    return {
        "min_length": min_length,
        "max_length": max_length,
        "avg_length": avg_length,
        "quartiles": quartiles
    }

# Example usage
video_stats = calculate_video_length_statistics('../ig-covid19-frame-rel-v1_candidates_bak.jsonl')
print(video_stats)

