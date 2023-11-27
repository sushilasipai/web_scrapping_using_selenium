import json
import numpy as np

def move_data_between_jsonl_files(source_file_path, destination_file_path, reference_file_path):
    with open(reference_file_path, 'r') as reference_file:
        reference_entries = [json.loads(line) for line in reference_file]


    reference_ids = {entry['platformId'] for entry in reference_entries}

    moved_entries = []
    remaining_entries = []


    with open(source_file_path, 'r') as source_file:
        for line in source_file:
            entry = json.loads(line)
            if entry['platformId'] in reference_ids:
                moved_entries.append(entry)        
            else:
                remaining_entries.append(entry)


    with open(destination_file_path, 'a') as destination_file:
        for entry in moved_entries:
            json.dump(entry, destination_file)
            destination_file.write('\n')


    with open(source_file_path, 'w') as source_file:
        for entry in remaining_entries:
            json.dump(entry, source_file)
            source_file.write('\n')



move_data_between_jsonl_files('../fb-covid19-frame-rel-v1_candidates_bak.jsonl', 
                              '../fb-covid19-frame-rel-v1_candidates_error.jsonl', 
                              '../failedToDownload.jsonl')
