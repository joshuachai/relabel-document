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
        Study participant ID, Instrument, Retinal Layer, Image size [mm], Image ID.

Usage:
    - Update FOLDER_PATH and LABELS_XLSX with your paths.
    - Run the script. All .png files in the folder will be removed, 
      and .raw files will be renamed according to the Excel data.

Note:
    - Files without a matching record in Excel will be skipped with a warning.
    - If you need to retain any .png files, back them up before running the script.
"""

import os
import glob
import pandas as pd
import tifffile
import numpy as np

# -----------------------
# Configuration
# -----------------------

FOLDER_PATH = './AVANTI'
LABELS_XLSX = './2025_OCTA_HARMONISATION_LABELS.xlsx'

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
    Removes all .png files in the specified folder.

    Parameters:
    ----------
    folder_path : str
        Path to the folder where .png files will be removed.
    """
    png_files = glob.glob(os.path.join(folder_path, '*.png'))
    
    for png_file in png_files:
        os.remove(png_file)
        print(f"{png_file} has been deleted")
    
    print("[INFO] All .png files removed. Only .raw files remain.")

remove_png_files(FOLDER_PATH)

# -----------------------
# Step 2: Convert .raw Files to .tiff
# -----------------------

def read_raw_image(raw_path: str, width: int, height: int, offset: int = 0) -> np.ndarray:
    """
    Reads a .raw file and returns a NumPy array (32-bit float), shaped as (height, width).

    Parameters:
    ----------
    raw_path : str
        Path to the .raw file.
    width : int
        Image width.
    height : int
        Image height.
    offset : int
        Byte offset (default: 0).

    Returns:
    ----------
    np.ndarray
        The image data as a 32-bit float NumPy array.
    """
    with open(raw_path, 'rb') as f:
        f.seek(offset)
        raw_data = f.read()

    # Interpret as 32-bit float (little-endian)
    array = np.frombuffer(raw_data, dtype=np.float32)

    # Reshape to (height, width)
    array = array.reshape((height, width))

    return array

def save_as_tiff(array: np.ndarray, tiff_path: str) -> None:
    """
    Saves a NumPy array as a 32-bit float TIFF file (compatible with ImageJ).

    Parameters:
    ----------
    array : np.ndarray
        The image data as a NumPy array.
    tiff_path : str
        The file path where the TIFF file will be saved.
    """
    tifffile.imwrite(tiff_path, array, dtype=np.float32, imagej=True)

def batch_convert(input_folder: str) -> None:
    """
    Batch processes .raw files:
    - Identifies whether they are 3×3 or 6×6 images.
    - Converts them to .tiff format.
    - Deletes the original .raw files.

    Parameters:
    ----------
    input_folder : str
        The folder containing .raw files to be processed.
    """
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.raw'):
            raw_path = os.path.join(input_folder, filename)
            base_name = os.path.splitext(filename)[0]
            last_char = base_name[-1]  # Extract the last character before .raw

            # Determine image dimensions based on last character
            if last_char == '3':
                width, height = 304, 304
                print(f"Identified {filename} as 3×3 (304x304)")
            elif last_char == '6':
                width, height = 400, 400
                print(f"Identified {filename} as 6×6 (400x400)")
            else:
                print(f"[WARNING] Unable to identify {filename}, last character is not 3 or 6. Skipping.")
                continue

            # Read the .raw file
            try:
                array = read_raw_image(raw_path, width, height)
            except ValueError as ve:
                print(f"[ERROR] Failed to read: {filename}, Error: {ve}")
                continue

            # Save as .tiff
            tiff_name = base_name + ".tiff"
            tiff_path = os.path.join(input_folder, tiff_name)
            save_as_tiff(array, tiff_path)

            # Delete the original .raw file
            os.remove(raw_path)
            print(f"{filename} has been converted to {tiff_name}")

batch_convert(FOLDER_PATH)

# -----------------------
# Step 3: Build Mapping from Excel
# -----------------------

df = pd.read_excel(LABELS_XLSX)

# Invert dictionaries to convert Excel text values back to single-letter codes
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
        image_id = str(row[COL_IMAGE_ID])  # Fallback if not numeric

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
# Step 4: Rename .tiff Files
# -----------------------

def parse_tiff_filename(filename_base: str):
    """
    Parses a .tiff filename (without extension), returning:
        (participant_id, instrument_letter, layer_letter, size_digit)
    """
    parts = filename_base.split('_')
    participant_id = parts[0]
    remainder = parts[1] if len(parts) > 1 else ''

    instrument_letter = remainder[0] if len(remainder) > 0 else ''
    layer_letter      = remainder[1] if len(remainder) > 1 else ''
    size_digit        = remainder[2] if len(remainder) > 2 else ''

    return participant_id, instrument_letter, layer_letter, size_digit

tiff_files = glob.glob(os.path.join(FOLDER_PATH, '*.tiff'))

for tiff_file in tiff_files:
    base_name = os.path.splitext(os.path.basename(tiff_file))[0]
    participant_id, instr_letter, layer_letter, size_digit = parse_tiff_filename(base_name)

    key = (participant_id, instr_letter, layer_letter, size_digit)

    if key in rename_map:
        new_id = rename_map[key]
        new_name = f"{new_id}.tiff"
        new_path = os.path.join(FOLDER_PATH, new_name)
        os.rename(tiff_file, new_path)
        print(f"'{base_name}.raw' has been changed to '{new_name}'")  # Print confirmation of the renaming
    else:
        print(f"[WARNING] No match in Excel for '{base_name}.raw'; skipping.")  # Warn if no match was found
