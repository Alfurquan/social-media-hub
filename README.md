SOCIAL Media Hub
=================

This project is developed using [poetry](https://python-poetry.org/docs/) package management tool for python and [FastAPI](https://fastapi.tiangolo.com/)

## Getting started
In order to get started with this project, make sure you have these pre requisites installed and setup on your machine

### Prerequisities

1. Install [python](https://www.python.org/) version 3.10+
2. Install [poetry](https://python-poetry.org/docs/#installation)
3. Add [poetry dotnev plugin](https://pypi.org/project/poetry-dotenv-plugin/) using command - ```poetry self add poetry-dotenv-plugin```

### Steps
1. Git clone the repo
2. Create a .env file with the content having the secret used to generate JWT tokens. You can for e.g generate an openssl random secret using command - `openssl rand -hex 32` 
    ```
    SECRET_KEY="<Put in secret here>"
    ```
3. Go to repo root and run `poetry install` to install all dependencies
4. Run `poetry shell` to launch a poetry shell terminal
5. Run `social-media-hub` to launch the web server which will be listening on `http://127.0.0.1:8000`
6. You can view all API endpoints at this address `http://127.0.0.1:8000/docs`  
