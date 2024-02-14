import json

def read_jsonl_file(file_path):
    """Read a JSONL file and return a list of JSON objects."""
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data

def extract_platform_ids(data):
    """Extract 'platformId' from each JSON object in the list."""
    return {d['platformId'] for d in data if 'platformId' in d}

def compare_jsonl_files_and_write(file1, file2, output_file):
    """Compare 'platformId' in two JSONL files and write unique rows from file1 to a new file."""
    data1 = read_jsonl_file(file1)
    data2 = read_jsonl_file(file2)

    ids1 = extract_platform_ids(data1)
    ids2 = extract_platform_ids(data2)

    unique_ids = ids1 - ids2

    with open(output_file, 'w') as file:
        for item in data1:
            if item.get('platformId') in unique_ids:
                file.write(json.dumps(item) + '\n')


# Paths to your JSONL files
file1 = './annotated_fb_candidates.jsonl'
file2 = './fb_selected_for_annotation_new.jsonl'
output_file ="./fb_diff_annotated_not_needed"

compare_jsonl_files_and_write(file1, file2, output_file)
