### Command to build the server container
```
winpty docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v D://20_Projects//dezoomcamp24//week1//docker_sql//ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --name pg-database \
    postgres:13

```

### Command to build the client container
```
winpty pgcli -h localhost -p 5432 -u root -d ny_taxi
```

### Command to build the pgAdmin container
```
winpty docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    dpage/pgadmin4
```

---
# A Network of Containers

### Build the network container
```
winpty docker network create pg-network
```

### Build the server container in the network
```
winpty docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v D://20_Projects//dezoomcamp24//week1//docker_sql//ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:13
```

### Build the pgAdmin container in the network
```
winpty docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4
```

## Dockerizing the ingestion script

```
URL="https://github.com/niaBaldoni/dezoomcamp24/raw/main/week1/docker_sql/data/yellow_tripdata_2021-01.parquet"

python pipeline_ny_taxi.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table-name=yellow_taxi_trips \
    --url=${URL}
```

```
docker build -t taxi_ingest:v005 .
```

```
winpty docker run -it \
    --network=pg-network \
    taxi_ingest:v005 \
        --user=root \
        --password=root \
        --host=pg-database \
        --port=5432 \
        --db=ny_taxi \
        --table-name=yellow_taxi_trips \
        --url=${URL}
```

## Docker-Compose

```

```