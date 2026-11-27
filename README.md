# Phosphoric Acid Mass Balance Calculator

A Python 3 desktop app that calculates the mass balance for the wet process of producing phosphoric acid from phosphate ore using sulfuric acid. I made it for my thesis to make work on phosphoric acid production easier.

## Features

- Supports both phosphate forms:
  - Fluorapatite (with fluoride, produces HF)
  - Tricalcium phosphate (without fluoride)
- Interface languages: English, French, German
- Ore mass can be entered in kg, g, or t; results can be displayed in kg, g, or t
- Accepts both `.` and `,` as the decimal separator
- Exports results to an OpenDocument Text (`.odt`) file

## Notes

Recovery rate only scales the actual H3PO4 yield. All other streams (H2SO4 feed, gypsum, HF) are reported as theoretical values at 100% conversion.

## Requirements

- Python 3
- tkinter (GUI; bundled with Python on Windows and macOS)
- odfpy (for `.odt` export)

## Installation and Usage

### Windows
1. Install Python from [python.org](https://www.python.org/downloads/). Check **"Add Python to PATH"** during installation.
2. Open Command Prompt in the project folder.
3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
4. Run the app:
   ```cmd
   python phosphoric_acid.py
   ```

### macOS
1. Open Terminal in the project folder.
2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python3 phosphoric_acid.py
   ```

### Linux (Debian/Ubuntu)
1. Open a terminal in the project folder.
2. Install tkinter:
   ```bash
   sudo apt install python3-tk
   ```
3. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python3 phosphoric_acid.py
   ```
