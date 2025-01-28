from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prettymapp.geo import get_aoi, GeoCodingError
from prettymapp.osm import get_osm_geometries
from prettymapp.plotting import Plot
from prettymapp.settings import STYLES
import matplotlib.pyplot as plt
import io
import base64

app = FastAPI()

class MapRequest(BaseModel):
    location: str
    radius: int
    style: str

@app.post("/")
async def generate_map(request: MapRequest):
    try:
        aoi = get_aoi(address=request.location, radius=request.radius)
    except GeoCodingError as e:
        raise HTTPException(status_code=400, detail=str(e))

    df = get_osm_geometries(aoi=aoi)
    draw_settings = STYLES.get(request.style, STYLES["Peach"])

    fig = Plot(
        df=df,
        aoi_bounds=aoi.bounds,
        draw_settings=draw_settings,
    ).plot_all()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", pad_inches=0, bbox_inches="tight", transparent=True)
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode()

    return {"image_url": f"data:image/png;base64,{img_str}"}
