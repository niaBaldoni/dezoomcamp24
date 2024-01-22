# Docker + Postgres

## Introduction to Docker

Docker:
+ delivers software in packages called containers
+ containers are isolated from one another
+ (smarter notes will come later this week)

## Ingesting NY Taxi Data to Postgres

We want to create a docker container that will run a postgres:13 image

```
winpty docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v C://Users//[...]//dezoomcamp24//week1//docker_sql//ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --name pg-database \
    postgres:13
```
**-it** means that the container is in interactive mode: we can interact with the container's command prompt;

**-e** sets enviroment variables inside the container;

**-v** is used to mount a volume from the host machine to the container;

**-p** is used to map a container's port to a port on the host machine.

This section will probably be updated with smarter notes in the morning
