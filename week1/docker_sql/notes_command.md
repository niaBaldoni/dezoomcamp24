```

services:
    postgres:
        image: postgres:12
        enviroment:
            POSTGRES_USER: airflow
            POSTGRES_PASSWORD: airflow
            POSTGRES_DB: airflow
        volumes:
            - postgres-db-volume:/var/lib/postgresql/data
        healthcheck:
            test: ["CMD", "pg_isready", "-U", "airflow"]
            interval: 5s
            retries: 5
        restart: always
```

```
winpty docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v C://Users//drago//Documents//GitHub//dezoomcamp24//week1//docker_sql//ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --name pg-database \
    postgres:13

```

```
$ winpty pgcli -h localhost -p 5432 -u root -d ny_taxi
```

```
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    dpage/pgadmin4
```

## network
```
docker network create pg-network
```

```
winpty docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v C://Users//drago//Documents//GitHub//dezoomcamp24//week1//docker_sql//ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:13
```

```
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4
```