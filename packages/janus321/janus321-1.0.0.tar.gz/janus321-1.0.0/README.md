# Janus321

A package to build and manage the Janus Docker image with FastAPI integration, with `InferenceManager.py` as the entry point.

## Installation

To install the package, run:

```bash
pip install janus321
```

## Usage

To use the package, run:

```bash
janus321
```

This will start the `InferenceManager.py` script, which is the entry point of the package.

## Building and Managing the Docker Image

The `janus_docker.py` script handles building and managing the Docker image using the Dockerfile at the root level. For more information on how to use this functionality, refer to the `janus_docker.py` script.

## Testing

The package includes unit tests in `test.py` and `pytest.ini`. To run the tests, use:

```bash
pytest
```

## Dependencies

The package depends on the following libraries:

- FastAPI
- Uvicorn
- Docker

For a complete list of dependencies, refer to the `requirements.txt` file.
