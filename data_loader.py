from pathlib import Path
from PIL import Image
PROJECT_ROOT=Path(__file__).resolve().parents[1]
DATA_DIR=PROJECT_ROOT/"data"
IMAGE_EXTS={".png",".jpg",".jpeg",".tif",".tiff"}
def list_files(folder,extensions=None):
    folder=Path(folder)
    if not folder.exists(): return []
    return sorted(p for p in folder.iterdir() if p.is_file() and (extensions is None or p.suffix.lower() in extensions))
def list_images(): return list_files(DATA_DIR/"images",IMAGE_EXTS)
def list_metadata(): return list_files(DATA_DIR/"metadata",{".xml"})
def list_terrain(): return list_files(DATA_DIR/"terrain",{".tif",".tiff"})
def load_image(path):
    with Image.open(path) as img: return img.copy()
