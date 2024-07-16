FROM chetan1111/botasaurus:latest

WORKDIR /app
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN apt update -y && apt install gcc -y


COPY pyproject.toml .
RUN apt-get install xvfb
RUN Xvfb :99 -ac & export DISPLAY=:99

RUN rm -rf build
RUN poetry install

RUN npm install -g npm@10.4.0

ENTRYPOINT ["poetry", "run", "dev"]