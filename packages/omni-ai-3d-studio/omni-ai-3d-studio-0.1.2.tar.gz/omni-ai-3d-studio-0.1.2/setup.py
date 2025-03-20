from setuptools import setup, find_packages

setup(
    name="omni-ai-3d-studio",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "Flask",
        "celery",
        "redis",
        "pika",
        "cloudinary",
        "requests",
        "pymeshlab",
        "replicate"
    ],
    author="Adhithyan J",
    author_email="adhijag54@gmail.com",
    description="A package for AI-powered 3D model generation and image upscaling",
    license="MIT"
)
