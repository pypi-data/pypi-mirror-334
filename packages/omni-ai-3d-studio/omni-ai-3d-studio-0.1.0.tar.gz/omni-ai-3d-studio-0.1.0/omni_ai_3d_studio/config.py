import os
from celery import Celery
import cloudinary
import cloudinary.uploader

# Configure Celery
CELERY_BROKER_URL='amqp://guest:guest@localhost:5672/'
CELERY_RESULT_BACKEND='redis://localhost:6379/0'

celery = Celery("omni_3d_studio", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery.conf.update({
    'task_serializer': 'json',
    'accept_content': ['json'],
    'result_serializer': 'json'
})

# Initialize Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_to_cloudinary(file_path, folder="default_folder"):
    """Upload an image file to Cloudinary and return the public URL."""
    try:
        result = cloudinary.uploader.upload(file_path, folder=folder)
        return result["url"]
    except Exception as e:
        return str(e)
