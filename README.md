# Relabeling Script for OCTA Images

## Overview
This script renames and organizes Optical Coherence Tomography Angiography (OCTA) images based on metadata extracted from filenames and an accompanying Excel file. It processes image files from different instruments, including Revo, Spectralis, and Angiovue, standardizing their names according to a predefined format.

## Prerequisites
Ensure you have the following installed before running the script:
- Python 3
- Required Python libraries: `pandas`, `glob`, `os`, `sys`, `pathlib`
- Excel files containing metadata: 
  - `2024_PartialData.xlsx`
  - `2025_OCTA_HARMONISATION_LABELS.xlsx`

## Installation
1. Clone or download the repository containing `relable.py`.
2. Install required Python packages by running:
   ```sh
   pip install pandas openpyxl
   ```

## Usage
To execute the script, run:
```sh
./relable.py {instrument name}
```
Where `{instrument name}` can be:
- `revo`: Processes files in the `./REVO` directory.
- `spectralis`: Processes files in the `./Spectralis` directory.
- `angiovue`: Processes files in the `./AVANTI` directory.

### Example Usage:
```sh
./relable.py revo
./relable.py spectralis
./relable.py angiovue
```

## Script Functions
### `decomposeFileName()`
- Extracts study ID, instrument type, retinal layer, image size, and scan resolution from filenames.

### `ExtractFileInfo()`
- Generates a short identifier for file names based on instrument type, image size, and retinal layer.

### `revo(imageID_list)`
- Processes and renames Revo-generated files.

### `spectralis(name_list, imageID_list)`
- Processes and renames Spectralis-generated files.

### `angiovue()`
- Processes Angiovue-generated files.
- Deletes unnecessary `.png` files.
- Renames `.raw` files based on metadata from the Excel file.

### `extractFileName()`
- Parses command-line arguments and calls the corresponding function based on the selected instrument.

## Notes
- The script relies on consistent filename formatting.
- Ensure that the Excel files contain the correct mapping data before execution.
- Running the script may overwrite existing filenames; use with caution.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

