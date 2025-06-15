import os
import uuid
from PIL import Image
import imageio.v2 as imageio
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Create FastAPI app
app = FastAPI()

# Serve static files (your website UI)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# Make sure video output folder exists
OUTPUT_DIR = "generated_videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/generate")
async def generate_video(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return {"detail": "Prompt cannot be empty."}

    filename = f"video_{uuid.uuid4().hex[:8]}.mp4"
    output_path = os.path.join(OUTPUT_DIR, filename)

    # Simulate a video by generating 5 identical image frames
    img = Image.new("RGB", (256, 256), color=(0, 128, 255))
    temp_image_path = output_path.replace(".mp4", ".png")
    img.save(temp_image_path)
    imageio.mimsave(output_path, [imageio.imread(temp_image_path)] * 5, fps=1)

    return {"video_url": f"/videos/{filename}"}

@app.get("/videos/{video_name}")
def serve_video(video_name: str):
    video_path = os.path.join(OUTPUT_DIR, video_name)
    if os.path.exists(video_path):
        return FileResponse(video_path, media_type="video/mp4")
    return {"detail": "Video not found"}
