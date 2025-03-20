import replicate
from .config import celery
import os
import replicate
from .config import celery
from .utils import save_file_from_url

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@celery.task(name="tasks.upscale_image")
def upscale_image_task(data):
    """Runs the image upscaling process asynchronously using Celery."""
    try:
        output = replicate.run(
            "philz1337x/clarity-upscaler:dfad41707589d68ecdccd1dfa600d55a208f9310748e44bfe35b4a6291453d5e",
            input=data
        )

        if not output or not isinstance(output, list):
            return {"error": "Invalid response from Replicate"}

        saved_files = []
        for index, file_obj in enumerate(output):
            if isinstance(file_obj, replicate.helpers.FileOutput):
                local_filename = f"upscaled_{index}.png"
                local_path = os.path.join(UPLOAD_FOLDER, local_filename)

                with open(local_path, "wb") as file:
                    file.write(file_obj.read())  # ✅ Save file locally

                saved_files.append(f"http://127.0.0.1:5000/static/uploads/{local_filename}")

        if not saved_files:
            return {"error": "No valid output files received"}

        return {"upscaled_image_urls": saved_files}  # ✅ JSON-serializable output

    except Exception as e:
        return {"error": str(e)}


@celery.task(name="tasks.generate_mesh")
def generate_mesh_task(data):
    """Runs the 3D model mesh generation process asynchronously using Celery."""
    try:
        output = replicate.run(
            "firtoz/trellis:4876f2a8da1c544772dffa32e8889da4a1bab3a1f5c1937bfcfccb99ae347251",
            input=data
        )

        if not output or not isinstance(output, dict):
            return {"error": "Invalid response from Replicate"}

        saved_files = {}

        for key, file_obj in output.items():
            if isinstance(file_obj, str) and file_obj.startswith("http"):
                # ✅ Download the file from the Replicate URL
                local_filename = f"{key}.ply" if "ply" in key else f"{key}.mp4"
                local_path = os.path.join(UPLOAD_FOLDER, local_filename)

                response = requests.get(file_obj)
                if response.status_code == 200:
                    with open(local_path, "wb") as file:
                        file.write(response.content)  # ✅ Save file locally

                    # ✅ Store the local file URL in JSON response
                    saved_files[key] = f"http://127.0.0.1:5000/static/uploads/{local_filename}"

        if not saved_files:
            return {"error": "No valid output files received"}

        return {"generated_files": saved_files}  # ✅ Proper JSON Response

    except Exception as e:
        return {"error": str(e)}