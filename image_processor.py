from pathlib import Path
from PIL import Image
import numpy as np
def image_summary(path):
    with Image.open(path) as im:
        arr=np.asarray(im)
        return {"filename":Path(path).name,"format":im.format or "Unknown","mode":im.mode,
                "width_px":im.width,"height_px":im.height,"array_shape":str(arr.shape)}
