# $ docker build -t test:pandas .
# ^ command to build this image in the selected folder

# COPY [sourceDirectory] [toDockerImage]


FROM python:3.9

RUN pip install pandas

WORKDIR /app
COPY pipeline.py pipeline.py

ENTRYPOINT [ "bash" ]