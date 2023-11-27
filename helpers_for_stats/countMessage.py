import json
import numpy as np

def calculate_message_length_statistics(jsonl_file_path):
    message_lengths = []

    with open(jsonl_file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            message = data.get('message', '')
            message_lengths.append(len(message))

    if not message_lengths:
        return {
            "min_length": None,
            "max_length": None,
            "avg_length": None,
            "quartiles": None
        }

    min_length = min(message_lengths)
    max_length = max(message_lengths)
    avg_length = np.mean(message_lengths)
    quartiles = np.percentile(message_lengths, [25, 50, 75])

    return {
        "min_length": min_length,
        "max_length": max_length,
        "avg_length": avg_length,
        "quartiles": quartiles
    }

# Example usage
stats = calculate_message_length_statistics('../fb-covid19-frame-rel-v1_candidates_bak.jsonl')
print(stats)

