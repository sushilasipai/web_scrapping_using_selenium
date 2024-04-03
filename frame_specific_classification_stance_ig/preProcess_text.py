import json
from transformers import RobertaTokenizer

# Specify the file paths
frames_file = '../annotation/frames.json'
input_jsonl = 'manually_annotated_ig_data.jsonl'
verification_data_file = 'verification_data.jsonl'  # File to store verification data

# Load the frames data from JSON
with open(frames_file, 'r') as f:
    frames = json.load(f)

# Initialize the Roberta tokenizer from the pre-trained model
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

def process_entry(data, frames, tokenizer):
    """Process each entry by combining frame text and post text, tokenizing, and preparing for Roberta."""
    # Extract the frame text using the frame number from the data entry
    frame_number = list(data.get('candidates', {}).keys())[0]
    frame_text = frames.get(frame_number, {}).get('text', 'No Frame Text')
    
    # Extract the post text and annotation information
    post_text = data.get('description', 'No Post Text')
    label_text = data.get('labels', {}).get('text', 'No Stance')  
    rationale = data.get('labels_reason', {}).get('text', '')
    
    # Combine the frame text and post text for contextual processing
    combined_text = f"Frame: {frame_text} Post: {post_text}"
    
    # Tokenize the combined text for Roberta
    inputs = tokenizer.encode_plus(
        combined_text,
        add_special_tokens=True,
        max_length=512,
        truncation=True,
        padding='max_length',
        return_attention_mask=True,
        return_tensors='pt'
    )
    
    # Return the processed data including original and tokenized information
    return {
        "frame_text": frame_text,
        "post_text": post_text,
        "annotation": label_text,
        "rationale": rationale,
        "input_ids": inputs['input_ids'].squeeze(0).tolist(),  # Convert tensor to list for JSON compatibility
        "attention_mask": inputs['attention_mask'].squeeze(0).tolist(),
    }

# Open the file to save verification data and read the input data
with open(verification_data_file, 'w') as vfile, open(input_jsonl, 'r') as infile:
    for line in infile:
        data = json.loads(line)
        processed_entry = process_entry(data, frames, tokenizer)
        
        # Save the processed entry for verification, now including combined text processing
        json.dump(processed_entry, vfile)
        vfile.write('\n')
