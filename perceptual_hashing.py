from imagededup.methods import PHash
from shutil import move
import os

def log_entry(entry, log_file):
    print(entry)
    with open(log_file, 'a') as file:
        file.write(entry + '\n')

def find_and_move_duplicates(facebook_image_dir, duplicates_dir, log_file_path):
    phasher = PHash()

    if not os.path.exists(duplicates_dir):
        os.makedirs(duplicates_dir)

    encodings = phasher.encode_images(image_dir=facebook_image_dir)

    duplicates = phasher.find_duplicates(encoding_map=encodings)

    identified_duplicates = set()

    for original, dup_list in duplicates.items():
        if original not in identified_duplicates:
            filtered_dup_list = [dup for dup in dup_list if dup != original and dup not in identified_duplicates]

            if filtered_dup_list:
                for dup in filtered_dup_list:
                    original_path = os.path.join(facebook_image_dir, dup)
                    if os.path.exists(original_path):
                        duplicate_path = os.path.join(duplicates_dir, dup)
                        move(original_path, duplicate_path)
                        log_entry(f'Moved {dup} to duplicates folder.', log_file_path)
                        identified_duplicates.add(dup)
                log_entry(f'Original {original} retained with duplicates: {", ".join(filtered_dup_list)}.', log_file_path)
            else:
                log_entry(f'{original} has no duplicates.', log_file_path)

    remaining_images = os.listdir(facebook_image_dir)
    for image in remaining_images:
        log_entry(f'{image} remains in the Facebook folder.', log_file_path)


if __name__ == '__main__':
    facebook_image_dir = './facebook'  
    duplicates_dir = './facebook_duplicates'  
    log_file_path = 'duplicates_ig_log.txt'  
    find_and_move_duplicates(facebook_image_dir, duplicates_dir, log_file_path)
