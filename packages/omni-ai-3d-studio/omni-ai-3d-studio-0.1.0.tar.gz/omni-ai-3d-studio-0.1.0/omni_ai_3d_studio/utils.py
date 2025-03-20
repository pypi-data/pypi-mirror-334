import os
import requests
import pymeshlab

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_file_from_url(file_url, filename):
    """Download and save a file from a URL."""
    response = requests.get(file_url)
    if response.status_code == 200:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "wb") as file:
            file.write(response.content)
        return file_path
    return None

def convert_ply_to_glb(input_ply, output_glb):
    """Convert PLY file to GLB using pymeshlab."""
    try:
        ms = pymeshlab.MeshSet()
        ms.load_new_mesh(input_ply)
        ms.save_current_mesh(output_glb)
        return output_glb
    except Exception as e:
        return None
