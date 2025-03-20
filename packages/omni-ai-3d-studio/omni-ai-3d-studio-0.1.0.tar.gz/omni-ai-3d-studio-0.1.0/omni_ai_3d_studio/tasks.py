import replicate
from .config import celery

@celery.task(name="tasks.upscale_image")
def upscale_image_task(data):
    """Runs the image upscaling process asynchronously using Celery."""
    try:
        output = replicate.run(
            "philz1337x/clarity-upscaler:dfad41707589d68ecdccd1dfa600d55a208f9310748e44bfe35b4a6291453d5e",
            input=data
        )
        return output
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
        return output
    except Exception as e:
        return {"error": str(e)}
