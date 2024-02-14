import json

# Load the JSONL file
with open('ig-covid19-filtered_candidates_to_match_image.jsonl', 'r') as file:
    data = [json.loads(line) for line in file]

# Select candidates for each frame
selected_candidates = {}
for frame in range(1, 31):  # F1 to F30
    frame_id = f'F{frame}'
    frame_candidates = [d for d in data if frame_id in d.get('candidates', {})]
    frame_candidates.sort(key=lambda x: x['candidates'][frame_id]['rank'])
    selected_candidates[frame_id] = frame_candidates[:3]  # Selecting top 4 with lowest ranks

# Save the selected candidates to a new JSONL file
with open('ig_selected_for_annotation_new1.jsonl', 'w') as outfile:
    for frame, candidates in selected_candidates.items():
        for candidate in candidates:
            # Add frame info to each candidate for clarity
            candidate['selected_for_frame'] = frame
            json.dump(candidate, outfile)
            outfile.write('\n')
