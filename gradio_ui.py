import os
import uuid
from PIL import Image
import imageio.v2 as imageio
import gradio as gr

OUTPUT_DIR = "generated_videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_video(prompt: str):
    if not prompt.strip():
        return None, "Please enter a prompt."

    filename = f"video_{uuid.uuid4().hex[:8]}.mp4"
    output_path = os.path.join(OUTPUT_DIR, filename)
    img = Image.new("RGB", (256, 256), color=(0, 128, 255))
    temp_image_path = output_path.replace(".mp4", ".png")
    img.save(temp_image_path)
    imageio.mimsave(output_path, [imageio.imread(temp_image_path)] * 5, fps=1)

    return output_path, f"Video generated for prompt: '{prompt}'"

ui = gr.Interface(
    fn=generate_video,
    inputs=gr.Textbox(label="Enter your prompt"),
    outputs=[gr.Video(label="Generated Video"), gr.Textbox(label="Status")],
    title="AI Video Generator",
    description="Type a prompt and generate a video clip!"
)

if __name__ == "__main__":
    ui.launch()
