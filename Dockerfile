FROM python:3.13-slim

LABEL image_name="xyseer/AnimeAssistant"
LABEL version=0.9c
LABEL description="xy-nas-tool/AnimeAssistant is a tool for anime series auto-subscription."

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY ./*.py /app/
COPY ./dao /app/dao
COPY ./dto /app/dto
COPY ./web /app/web
COPY ./download_tools /app/download_tools
COPY ./static /static

EXPOSE 12138

# remove vulnerablilities
RUN pip3 uninstall -y setuptools pip


ENV TZ=Asia/Taipei
CMD ["python3","main.py","> /dev/null"]
