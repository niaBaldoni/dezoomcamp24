# $ docker build -t test:pandas .
# ^ command to build this image in the selected folder

# COPY [sourceDirectory] [toDockerImage]

FROM python:3.9

RUN pip install pandas argparse pyarrow sqlalchemy psycopg2-binary

WORKDIR /app
COPY pipeline_ny_taxi.py pipeline_ny_taxi.py

ENTRYPOINT [ "python", "pipeline_ny_taxi.py" ]