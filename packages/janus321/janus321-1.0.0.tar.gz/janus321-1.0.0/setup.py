from setuptools import setup, find_packages

setup(
    name='janus321',
    version='1.0.0',
    author='John codes',
    description='A package to build and manage the Janus Docker image with FastAPI integration, with InferenceManager.py as the entry point',
    packages=find_packages(where='src'),
    install_requires=[
        'fastapi',
        'uvicorn',
        'docker',
        # Add other dependencies from requirements.txt
    ],
    entry_points={
        'console_scripts': [
            'janus321=src.inference_manager:main',
        ],
    },
)
