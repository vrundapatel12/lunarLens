from pathlib import Path
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance, ImageOps
from modules.data_loader import list_images, list_metadata, list_terrain, load_image
from modules.metadata_reader import read_xml_metadata
from modules.image_processor import image_summary
from modules.terrain_analyzer import load_geotiff, terrain_statistics
from modules.visualization import terrain_figure, histogram_figure, image_histogram
from modules.report_generator import build_report

st.set_page_config(page_title="LunarLens | Lunar Data Studio", page_icon="🌙", layout="wide")
st.markdown("""
<style>
.stApp {background:linear-gradient(180deg,#081426 0%,#0b1729 55%,#101d31 100%);}
[data-testid="stSidebar"] {background:#0d1b30;}
h1,h2,h3 {letter-spacing:-.4px;}
.hero {padding:1.35rem 1.5rem;border:1px solid #29415f;border-radius:16px;background:linear-gradient(120deg,#142b48,#102039);margin-bottom:1rem;}
.hero small {color:#a9bfd9;letter-spacing:2px;text-transform:uppercase;}
.hero h1 {margin:.25rem 0;color:#f4f7fb;font-size:2.25rem;}
.hero p {color:#b8c9dc;margin:0;}
.kpi {padding:14px;border:1px solid #29415f;border-radius:12px;background:#10223a;}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="hero"><small>ASTRA 2026 · SPACE DATA LAB</small><h1>🌙 LunarLens</h1><p>Explore lunar imagery, inspect mission metadata and analyse terrain products.</p></div>', unsafe_allow_html=True)
with st.sidebar:
    st.markdown("## Mission workspace")
    mission=st.selectbox("Mission",["Chandrayaan-2"])
    instrument=st.selectbox("Instrument",["OHRC","TMC-2","Other / not specified"])
    st.divider()
    st.caption("LOCAL DATA LIBRARY")
    st.write("Images · XML labels · GeoTIFF terrain")
    st.caption("Demo assets are simulated and are not official mission observations.")

images, xmls, rasters = list_images(), list_metadata(), list_terrain()
overview, image_tab, terrain_tab, metadata_tab = st.tabs(["◈  Overview","▧  Image studio","⌁  Terrain lab","⌗  Metadata & reports"])

with overview:
    st.subheader("Workspace overview")
    c1,c2,c3,c4=st.columns(4)
    for col,label,value in [(c1,"Images",len(images)),(c2,"XML labels",len(xmls)),(c3,"Terrain rasters",len(rasters)),(c4,"Mission",mission)]:
        with col: st.markdown(f'<div class="kpi"><span style="color:#9fb4cd">{label}</span><h2 style="margin:.2rem 0">{value}</h2></div>',unsafe_allow_html=True)
    st.markdown("### Explore your lunar data")
    left,right=st.columns([1.2,1])
    with left:
        st.markdown("**Data workflow**")
        st.write("1. Add an image to `data/images/`.")
        st.write("2. Add its XML label to `data/metadata/`.")
        st.write("3. Add a single-band elevation GeoTIFF to `data/terrain/`.")
        st.info("Use the tabs above to enhance images, inspect metadata and explore terrain.")
    with right:
        st.markdown("**Data integrity**")
        st.warning("Included sample imagery and metadata are synthetic demonstration assets. Do not interpret them as Chandrayaan measurements.")

with image_tab:
    st.subheader("Image studio")
    if not images: st.info("Add PNG, JPG or TIFF images to data/images/.")
    else:
        selected=st.selectbox("Select an image",images,format_func=lambda p:p.name,key="image_select")
        original=load_image(selected).convert("RGB")
        a,b=st.columns([1.5,1])
        with b:
            st.markdown("**Enhancement controls**")
            brightness=st.slider("Brightness",0.25,2.5,1.0,0.05)
            contrast=st.slider("Contrast",0.25,2.5,1.0,0.05)
            sharpness=st.slider("Sharpness",0.0,3.0,1.0,0.1)
            mode=st.selectbox("Display mode",["Colour","Grayscale","Inverted"])
            show_original=st.checkbox("Compare with original",False)
        processed=ImageEnhance.Brightness(original).enhance(brightness)
        processed=ImageEnhance.Contrast(processed).enhance(contrast)
        processed=ImageEnhance.Sharpness(processed).enhance(sharpness)
        if mode=="Grayscale": processed=ImageOps.grayscale(processed)
        elif mode=="Inverted": processed=ImageOps.invert(processed)
        with a:
            if show_original:
                x,y=st.columns(2)
                x.image(original,caption="Original",use_container_width=True)
                y.image(processed,caption="Enhanced",use_container_width=True)
            else: st.image(processed,caption=selected.name,use_container_width=True)
        summary=image_summary(selected)
        m1,m2,m3,m4=st.columns(4)
        m1.metric("Width",f'{summary["width_px"]:,} px');m2.metric("Height",f'{summary["height_px"]:,} px')
        m3.metric("Format",summary["format"]);m4.metric("Colour mode",summary["mode"])
        st.markdown("**Pixel intensity distribution**")
        st.pyplot(image_histogram(processed),use_container_width=True,clear_figure=True)
        import io
        buffer=io.BytesIO();processed.save(buffer,format="PNG")
        st.download_button("Download enhanced image",buffer.getvalue(),f"{selected.stem}_enhanced.png","image/png")

with terrain_tab:
    st.subheader("Terrain lab")
    if not rasters: st.info("No GeoTIFF found. Add a supported single-band GeoTIFF to data/terrain/ to enable terrain analysis.")
    else:
        selected_raster=st.selectbox("Select terrain raster",rasters,format_func=lambda p:p.name)
        try:
            arr,info=load_geotiff(selected_raster); stats=terrain_statistics(arr)
            cols=st.columns(4)
            for col,key in zip(cols,["minimum","maximum","mean","median"]): col.metric(key.replace("_"," ").title(),f'{stats[key]:,.3f}')
            st.pyplot(terrain_figure(arr,selected_raster.name),use_container_width=True,clear_figure=True)
            st.pyplot(histogram_figure(arr),use_container_width=True,clear_figure=True)
            try:
                import plotly.graph_objects as go
                step=max(1,int(max(arr.shape)/180))
                sample=arr[::step,::step]
                fig=go.Figure(data=[go.Surface(z=np.ma.masked_invalid(sample),colorscale="Earth")])
                fig.update_layout(title="3D terrain surface (stored raster values)",height=520,margin=dict(l=0,r=0,t=45,b=0))
                st.plotly_chart(fig,use_container_width=True)
            except ImportError: st.info("Install Plotly to enable the interactive 3D terrain view.")
            with st.expander("Raster technical details"): st.json(info)
            st.caption("Values and units must be interpreted using the official product label. This prototype does not apply unknown scale factors.")
        except Exception as e: st.error(f"Could not process this raster: {e}")

with metadata_tab:
    st.subheader("Metadata explorer")
    metadata={}
    if xmls:
        selected_xml=st.selectbox("Select XML label",xmls,format_func=lambda p:p.name,key="xml_select")
        try:
            metadata=read_xml_metadata(selected_xml)
            st.success(f"Read {len(metadata)} populated metadata fields.")
            query=st.text_input("Search metadata fields",placeholder="Try mission, product, instrument...")
            filtered={k:v for k,v in metadata.items() if query.lower() in k.lower() or query.lower() in v.lower()}
            st.dataframe(pd.DataFrame([{"Field":k,"Value":v} for k,v in filtered.items()]),use_container_width=True,hide_index=True)
            with st.expander("View raw parsed metadata"): st.json(metadata)
        except Exception as e: st.error(f"Could not read XML: {e}")
    else: st.info("Add XML labels to data/metadata/.")
    st.divider()
    dataset=st.text_input("Dataset / product name",value=selected_xml.name if xmls else "Not selected")
    report=build_report(mission,instrument,dataset,metadata=metadata)
    st.download_button("↓  Download observation report",report,"lunarlens_report.txt","text/plain",use_container_width=True)

st.divider()
st.caption("LunarLens · Educational exploration prototype · Verify scientific interpretation against official mission documentation.")
