import json
import os
from docx import Document
from docx.shared import Inches
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

# Paths and filenames
input_jsonl = 'annotated_ig_candidates_new.jsonl'
frames_json = 'frames.json'
output_docx = 'annotated_data_2.docx'
image_folder = '../instagram'

# Define colors
post_background_color = "d4f0fb"  # Blue background for post text
platform_id_shading_color = "7cc47c"  # Dark green
frame_shading_color = "ffd966"  # Orange
annotation_color ="FBDFD4" #pink

# Read frames data from frames.json file
with open(frames_json, 'r') as f:
    frames_data = json.load(f)

# Create a new Word document
doc = Document()

# Function to add a heading with underline and background color
def add_heading(text, shading_color=None):
    paragraph = doc.add_paragraph()
    run = paragraph.add_run(text)
    run.font.underline = True
    if shading_color:
        shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{shading_color}"/>')
        paragraph._element.get_or_add_pPr().append(shading_elm)

# Function to add a paragraph with background color
def add_paragraph(text, shading_color=None):
    paragraph = doc.add_paragraph(text)
    if shading_color:
        shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{shading_color}"/>')
        paragraph._element.get_or_add_pPr().append(shading_elm)

# Function to add an image with error handling
def add_image(image_path):
    if os.path.exists(image_path):
        doc.add_picture(image_path, width=Inches(4.5))
    else:
        add_paragraph(f"Image not found: {image_path}")

# Read JSONL file and extract data for each post
with open(input_jsonl, 'r') as file:
    for line in file:
        data = json.loads(line)
        platform_id = data.get('platformId', '')
        text = data.get('text', '')
        labels = data.get('labels', {})
        labels_reason = data.get('labels_reason', {})
        frame_number = next(iter(data.get('candidates', {})), None)
        frame_text = frames_data.get(frame_number, {}).get('text', '')
        image_0_path = os.path.join(image_folder, f"{platform_id}_0.jpg")
        image_1_path = os.path.join(image_folder, f"{platform_id}_1.jpg")

        # Add data to the document with titles underlined and shaded background
        add_heading(f"Platform ID: {platform_id}", platform_id_shading_color)
        add_heading(f"Frame {frame_number}:", frame_shading_color)
        add_paragraph(frame_text, frame_shading_color)
        add_heading("Post Text:", post_background_color)
        add_paragraph(text, post_background_color)
        add_heading("Post Text Annotation:", annotation_color)
        add_paragraph(labels.get('text', ''), annotation_color)
        add_heading("Post Text Annotation Reason:", post_background_color)
        add_paragraph(labels_reason.get('text', ''), post_background_color)

        if os.path.exists(image_0_path):
            add_heading("Image 0:", post_background_color)
            add_image(image_0_path)
            add_heading("Image 0 Annotation:", annotation_color)
            add_paragraph(labels.get('image_0', ''), annotation_color)
            add_heading("Image 0 Annotation Reason:", post_background_color)
            add_paragraph(labels_reason.get('image_0', ''), post_background_color)
        
        # Add Image 1 data if available
        if os.path.exists(image_1_path):
            add_heading("Image 1:", post_background_color)
            add_image(image_1_path)
            add_heading("Image 1 Annotation:", annotation_color)
            add_paragraph(labels.get('image_1', ''), annotation_color)
            add_heading("Image 1 Annotation Reason:", post_background_color)
            add_paragraph(labels_reason.get('image_1', ''), post_background_color)

        # Add combined text and image annotation and reason
        add_heading("Combined Text and Image Annotation:", annotation_color)
        add_paragraph(labels.get('combined', ''), annotation_color)
        add_heading("Combined Annotation Reason:", post_background_color)
        add_paragraph(labels_reason.get('combined', ''), post_background_color)

        # Add spacing between entries
        doc.add_paragraph()

# Save the document
doc.save(output_docx)
