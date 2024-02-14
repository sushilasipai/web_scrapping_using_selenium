import json

def count_labels_in_jsonl(file_path):
    # Initialize counters for each category including 'Not Relevant'
    counts = {
        "text": {"Accept": 0, "Reject": 0, "No Stance": 0, "Not Relevant": 0},
        "image": {"Accept": 0, "Reject": 0, "No Stance": 0, "Not Relevant": 0},
        "combined": {"Accept": 0, "Reject": 0, "No Stance": 0, "Not Relevant": 0}
    }

    # Read the JSONL file line by line
    with open(file_path, 'r') as file:
        for line in file:
            # Parse each line as a JSON object
            data = json.loads(line)

            # Check if 'labels' key exists in the JSON object
            if 'labels' in data:
                labels = data['labels']

                # Update counts for each category
                for category in ['text', 'image', 'combined']:
                    if category in labels:
                        label_value = labels[category]
                        if label_value in counts[category]:
                            counts[category][label_value] += 1

    return counts

# Example usage
file_path = 'annotated_ig_candidates.jsonl'
label_counts = count_labels_in_jsonl(file_path)
print(label_counts)
