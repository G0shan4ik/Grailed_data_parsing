FROM chetan1111/botasaurus:latest

WORKDIR /app
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN apt update -y && apt install gcc -y


COPY pyproject.toml .
RUN apt-get install xvfb
RUN Xvfb :99 -screen 0 1024x768x16 & export DISPLAY=:99

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i --force-depends google-chrome-stable_current_amd64.deb
RUN apt-get install -f

RUN rm -rf build
RUN poetry install

RUN npm install -g npm@10.4.0

#ENTRYPOINT ["poetry", "run", "dev"]
CMD ["python", "main.py"]