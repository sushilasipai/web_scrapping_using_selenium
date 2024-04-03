from docx import Document
import json

# File paths
verification_data_file = 'verification_data.jsonl'
word_file = 'verification_data.docx'

# Create a new Document
doc = Document()

# Open the .jsonl file and read lines
with open(verification_data_file, 'r') as file:
    for line in file:
        # Parse JSON line
        data = json.loads(line)
        
        # Write content to the Word document
        doc.add_paragraph(f"Frame Text: {data['frame_text']}")
        doc.add_paragraph(f"Post Text: {data['post_text']}")
        doc.add_paragraph(f"Annotation: {data['annotation']}")
        doc.add_paragraph(f"Rationale: {data['rationale']}")
        doc.add_paragraph(f"Input IDs: {data['input_ids'][:10]}... (truncated)")
        doc.add_paragraph(f"Attention Mask: {data['attention_mask'][:10]}... (truncated)")
        
        # Add a page break after each entry for readability, except for the last one
        doc.add_page_break()

# Save the document
doc.save(word_file)
