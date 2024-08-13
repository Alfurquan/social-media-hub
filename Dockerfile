FROM python:3.10

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN chmod +x setup.sh

RUN ./setup.sh

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry self add poetry-dotenv-plugin
RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "python", "./social_media_hub/main.py"]
