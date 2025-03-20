FROM python:3.12-slim-bookworm


RUN apt-get update \
    && apt-get install -y  \
    gcc libcairo2-dev pkg-config python3-dev ffmpeg

RUN pip install guacenc-py

CMD [ "guacenc-cli --help" ]