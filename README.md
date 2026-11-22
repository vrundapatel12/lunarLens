# LunarLens — ASTRA Final Prototype

A modular Streamlit application for exploring lunar imagery, XML metadata, and single-band terrain GeoTIFFs.

> **Data notice:** The included image, XML metadata, and CSV examples are synthetic demonstration assets. They are not genuine Chandrayaan observations. Do not present their values as official mission measurements.

## Features

- Dark space-themed dashboard with mission and data-library overview
- Image Studio: brightness, contrast, sharpness, grayscale, invert, original/enhanced comparison, image information, histogram, and PNG export
- Metadata Explorer: XML parsing, searchable field table, raw parsed metadata, and downloadable observation summary
- Terrain Lab: GeoTIFF statistics, 2D terrain map, value histogram, raster details, and interactive 3D surface when Plotly is installed
- Modular code in `modules/`

## Requirements

- Python 3.10 or newer recommended
- Windows PowerShell instructions below

## Run on Windows

Open this folder in VS Code, then run these commands in its terminal:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501` if the browser does not open automatically.

If PowerShell blocks virtual-environment activation, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Project structure

```text
LunarLens_ASTRA_Final/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── modules/
│   ├── data_loader.py
│   ├── image_processor.py
│   ├── metadata_reader.py
│   ├── report_generator.py
│   ├── terrain_analyzer.py
│   └── visualization.py
└── data/
    ├── images/
    ├── metadata/
    └── terrain/
```

## Add data

- Put PNG, JPG, or TIFF images in `data/images/`.
- Put XML labels in `data/metadata/`.
- Put single-band GeoTIFF rasters in `data/terrain/`.

The current XML reader is a simple generic XML text extractor. Official PDS4 labels may need a more specialized parser and product-specific interpretation. The terrain module displays stored raster values; it does not guess scale factors, offsets, or scientific units. Confirm those from the official product label and documentation.

## Troubleshooting

- Run `python -m py_compile app.py` to check the main app's Python syntax.
- If a module import fails, make sure the terminal is in this project folder and that dependencies were installed from this folder's `requirements.txt`.
- Stop Streamlit with `Ctrl+C`, then restart using `streamlit run app.py`.

## Educational-use note

LunarLens is an educational exploration prototype, not a scientific validation tool. Preserve source attribution and follow the data provider's usage conditions when adding real mission data.


## Included demo data (synthetic)

The `data/images/` folder includes OHRC-style and TMC-2-style illustrative images. `data/metadata/` includes matching synthetic XML examples. `data/terrain/demo_lunar_terrain_SIMULATED.tif` is a generated single-band GeoTIFF for testing the Terrain Lab. None of these files are official Chandrayaan observations; terrain values are arbitrary units, not metres.
