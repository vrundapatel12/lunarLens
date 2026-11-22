import matplotlib.pyplot as plt
import numpy as np
def terrain_figure(array,title="Terrain raster preview"):
    fig,ax=plt.subplots(figsize=(10,5))
    im=ax.imshow(np.ma.masked_invalid(np.asarray(array,dtype=float)),cmap="terrain")
    ax.set_title(title); ax.set_xlabel("Pixel column"); ax.set_ylabel("Pixel row")
    fig.colorbar(im,ax=ax,label="Stored raster value (verify units)")
    fig.tight_layout(); return fig
def histogram_figure(array):
    values=np.asarray(array,dtype=float); values=values[np.isfinite(values)]
    fig,ax=plt.subplots(figsize=(9,3.5)); ax.hist(values,bins=40)
    ax.set_title("Terrain value distribution"); ax.set_xlabel("Stored raster value"); ax.set_ylabel("Pixel count")
    ax.grid(True,alpha=.25); fig.tight_layout(); return fig
def image_histogram(image):
    arr=np.asarray(image)
    fig,ax=plt.subplots(figsize=(9,3.2))
    if arr.ndim==2: ax.hist(arr.ravel(),bins=64)
    else:
        for idx,label in enumerate(["Red","Green","Blue"]): ax.hist(arr[:,:,idx].ravel(),bins=64,histtype="step",label=label)
        ax.legend()
    ax.set_title("Image intensity histogram"); ax.set_xlabel("Pixel intensity"); ax.set_ylabel("Frequency")
    ax.grid(True,alpha=.2); fig.tight_layout(); return fig
