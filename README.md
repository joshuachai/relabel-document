# OCTA Data Processing Scripts

## Overview

This project contains two Python scripts designed to process **OCTA (Optical Coherence Tomography Angiography)** data. These scripts handle file renaming, format conversion, and cleanup tasks for **Angiovue, Revo, and Spectralis** devices.

## Scripts

### 1. `main_gui.py`

**Functions**:

- Provides a simple **graphical interface (GUI)** with three buttons to run key OCTA data processing scripts.
- Each button triggers a specific script with the correct parameters:
  - **Angiovue**: Deletes `.png` files and converts `.raw` to `.bmp` using `angiovue.py`.
  - **Revo**: Renames Revo files using Excel mapping via `relabel.py revo`.
  - **Spectralis**: Renames Spectralis files using Excel mapping via `relabel.py spectralis`.
- Displays popup notifications for script success/failure.

**Run Command**:

```bash
python main_gui.py

```

### 2. `angiovue.py`

**Functions**:

- **Deletes** all `.png` files in the `AVANTI` folder, keeping only `.raw` files.
- **Converts** `.raw` files to `.tiff` format.
- **Renames** `.tiff` files based on an **Excel mapping file** (`2025_OCTA_HARMONISATION_LABELS.xlsx`).

**Run Command**:

```bash
python angiovue.py
```

**Notes**:

- `.png` files will be permanently deleted. **Backup important files before running the script**.
- `.raw` files must end with `3` or `6` to determine the correct image size.

---

### 2. `relabel.py`

**Functions**:

- **For Revo**:

  - Parses `.raw` files in the `./REVO` directory.
  - Renames them using **Image IDs from an Excel file**.

- **For Spectralis**:
  - Parses `.tiff` files in the `./Spectralis` directory.
  - Renames them based on the **Excel mapping**.

**Run Commands**:

```bash
python3 ./relabel.py revo
```

```bash
python3 ./relabel.py spectralis
```

**Notes**:

- The script requires two Excel files:
  - `2024_PartialData.xlsx`
  - `2025_OCTA_HARMONISATION_LABELS.xlsx`
- This script only supports **Revo** and **Spectralis** devices. It does **not** process **Angiovue**.
