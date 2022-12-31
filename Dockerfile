FROM python:3.9

LABEL image_name="xyseer/AnimeAssistant"
LABEL version=0.99
LABEL description="xy-nas-tool/AnimeAssistant is a tool for anime series auto-subscription."

WORKDIR /app
COPY ./*.py /app/
COPY ./dao /app/dao
COPY ./dto /app/dto
COPY ./web /app/web
COPY ./download_tools /app/download_tools
COPY ./requirements.txt /app/requirements.txt
COPY ./static /static

EXPOSE 12138

RUN pip3 install -r /app/requirements.txt


ENV TZ=Asia/Taipei
CMD ["python3","main.py","> /dev/null"]