import json

def count_types_in_jsonl(file_path):
    type_counts = {}

    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            type_value = data.get('type', 'Unknown')
            type_counts[type_value] = type_counts.get(type_value, 0) + 1

    return type_counts

type_counts = count_types_in_jsonl('../ig-covid19-frame-rel-v1_candidates_error.jsonl')
print(type_counts)
