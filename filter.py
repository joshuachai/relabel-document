"""
Script Purpose:
    1. Remove all .png files from a specified folder, leaving only .raw files.
    2. Build a mapping from data in an Excel file:
       (Participant ID, Instrument, Retinal Layer, Image Size) -> Image ID.
    3. Use that mapping to batch-rename matching .raw files in the folder.

Prerequisites:
    - pandas installed (with openpyxl or xlrd to read Excel).
    - Directory path and Excel file location correctly set.
    - The Excel file must contain columns:
        Study participant ID, Instrument, Retinal Layer, Image size [mm], Image ID

Usage:
    - Update FOLDER_PATH and LABELS_XLSX with your paths.
    - Run the script. All .png files in the folder will be removed, 
      and .raw files will be renamed according to the Excel data.

Note:
    - Files without a matching record in Excel will be skipped (with a warning).
    - If you need to retain any .png files, back them up first.
"""

import os
import glob
import pandas as pd

# -----------------------
# Configuration
# -----------------------
FOLDER_PATH = '/Users/joshua/JINHOtest/AVANTI'
LABELS_XLSX = '/Users/joshua/JINHOtest/2025_OCTA_HARMONISATION_LABELS.xlsx'

COL_PARTICIPANT_ID = 'Study participant ID'
COL_INSTRUMENT     = 'Instrument'
COL_LAYER          = 'Retinal Layer'
COL_SIZE           = 'Image size [mm]'
COL_IMAGE_ID       = 'Image ID'

INSTRUMENT_MAP = {'A': 'Angiovue'}
LAYER_MAP = {'S': 'Superficial', 'D': 'Deep', 'R': 'Retina'}
SIZE_MAP = {'3': '3x3', '6': '6x6'}

# -----------------------
# Step 1: Remove .png Files
# -----------------------
def remove_png_files(folder_path: str) -> None:
    """
    Removes all .png files in the given folder.
    """
    png_files = glob.glob(os.path.join(folder_path, '*.png'))
    for png_file in png_files:
        os.remove(png_file)
        print(f"[INFO] Deleted: {png_file}")
    print("[INFO] All .png files removed. Only .raw files remain.")

remove_png_files(FOLDER_PATH)

# -----------------------
# Step 2: Build Mapping from Excel
# -----------------------
df = pd.read_excel(LABELS_XLSX)

# Invert dictionaries to go from Excel text to single-letter code
inv_instrument_map = {v: k for k, v in INSTRUMENT_MAP.items()}
inv_layer_map      = {v: k for k, v in LAYER_MAP.items()}
inv_size_map       = {v: k for k, v in SIZE_MAP.items()}

rename_map = {}

for _, row in df.iterrows():
    participant_id = row[COL_PARTICIPANT_ID]
    instrument_str = row[COL_INSTRUMENT]
    layer_str      = row[COL_LAYER]
    size_str       = row[COL_SIZE]

    # Convert Image ID to a 4-digit string if it's numeric
    try:
        numeric_id = int(row[COL_IMAGE_ID])
        image_id = f"{numeric_id:04d}"
    except (ValueError, TypeError):
        image_id = str(row[COL_IMAGE_ID])  # fallback if not numeric

    try:
        instrument_letter = inv_instrument_map[instrument_str]
        layer_letter      = inv_layer_map[layer_str]
        size_digit        = inv_size_map[size_str]
    except KeyError:
        # Skip any row that doesn't match the mapping
        continue

    key = (participant_id, instrument_letter, layer_letter, size_digit)
    rename_map[key] = image_id

# -----------------------
# Step 3: Rename .raw Files
# -----------------------
def parse_raw_filename(filename_base: str):
    """
    Parses a .raw filename (without extension), returning a tuple of:
        participant_id, instrument_letter, layer_letter, size_digit
    """
    parts = filename_base.split('_')
    participant_id = parts[0]
    remainder = parts[1] if len(parts) > 1 else ''

    # Typically the remainder has three characters, e.g. "AD3"
    instrument_letter = remainder[0] if len(remainder) > 0 else ''
    layer_letter      = remainder[1] if len(remainder) > 1 else ''
    size_digit        = remainder[2] if len(remainder) > 2 else ''

    return participant_id, instrument_letter, layer_letter, size_digit

raw_files = glob.glob(os.path.join(FOLDER_PATH, '*.raw'))
for raw_file in raw_files:
    base_name = os.path.splitext(os.path.basename(raw_file))[0]
    participant_id, instr_letter, layer_letter, size_digit = parse_raw_filename(base_name)

    key = (participant_id, instr_letter, layer_letter, size_digit)
    if key in rename_map:
        new_id = rename_map[key]
        new_name = f"{new_id}.raw"
        new_path = os.path.join(FOLDER_PATH, new_name)
        os.rename(raw_file, new_path)
        print(f"[INFO] Renamed '{base_name}.raw' -> '{new_name}'")
    else:
        print(f"[WARNING] No match in Excel for '{base_name}.raw'; skipping.")
