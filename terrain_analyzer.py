import numpy as np
def load_geotiff(path):
    try: import rasterio
    except ImportError as exc: raise RuntimeError("Install rasterio: python -m pip install rasterio") from exc
    with rasterio.open(path) as src:
        band=src.read(1,masked=True).astype("float64")
        arr=np.asarray(band.filled(np.nan),dtype=float)
        info={"width":src.width,"height":src.height,"crs":str(src.crs) if src.crs else "Not specified",
              "bounds":str(src.bounds),"nodata":src.nodata,"units":src.units[0] if src.units else "Not specified"}
    return arr,info
def terrain_statistics(array):
    values=np.asarray(array,dtype=float); values=values[np.isfinite(values)]
    if not values.size: raise ValueError("No valid numeric raster cells.")
    return {"valid_cells":int(values.size),"minimum":float(values.min()),"maximum":float(values.max()),
            "mean":float(values.mean()),"median":float(np.median(values)),"std_dev":float(values.std())}
