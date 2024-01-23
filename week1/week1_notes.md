# Docker + Postgres

## Table of contents
+ [Introduction to Docker](#movie_camera-introduction-to-docker)
+ [Ingesting NY Taxi Data to Postgres](#movie_camera-ingesting-ny-taxi-data-to-postgres)
+ [Connecting pgAdmin and Postgres](#movie_camera-connecting-pgadmin-and-postgres)

---
## :movie_camera: Introduction to Docker

Docker:
+ delivers software in packages called containers
+ containers are isolated from one another
+ (smarter notes will come later this week)

---
## :movie_camera: Ingesting NY Taxi Data to Postgres

### Setting up the server

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
+ **-it** means that the container is in interactive mode: we can interact with the container's command prompt;

+ **-e** sets enviroment variables inside the container;

+ **-v** is used to mount a volume from the host machine to the container;

+ **-p** is used to map a container's port to a port on the host machine.

+ I am on a Windows enviroment, so in this situation I have to add the **winpty** command.

![ciao](assets/week1_postgres13_docker_run_first_time.PNG)

Now we have a database running in our docker container; note that, while the container is isolated, the postgres data is mounted on the path we specified; so, if we stop the container and run the command again, docker will correctly identify that the folder already contains the data.

![ciao](assets/week1_postgres13_docker_run.PNG)

### Setting up the client

Now that we have a server, we need to set up a new container that will act as our client. We're going to open a new Git Bash window and install pgcli.

```
pip install pgcli
```

Now that we've installed pgcli, we can run the following command to try and connect to our database:

```
winpty pgcli -h localhost -p 5432 -u root -d ny_taxi
```
+ **-h** sets the hostname of our Postgres server
+ **-p** sets the port number
+ **-u** is the username of the user trying to access
+ **-d** is the name of the database
+ **winpty** is winpty again

If everything went right, a connection to the database will be created and we can execute SQL commands.

![ciao](assets/week1_pgcli_first_time.PNG)

If we now try to run a couple of queries, the database will obviously react as it's empty. Because it is. We can still SELECT 1; to ensure that the database is receiving queries from our client, and is replying as we expect.

![ciao](assets/week1_pgcli_db_is_empty.PNG)

### Setting up a pipeline

Now we have a server that can store our data, and we have a client that can read it. We now need something that can handle the transfer of the data from our dataset to our newly set up database; in this case, we're going to use Jupyter Notebook.

```
pip install jupyter
```

And now that we have Jupyter, we can run the command

```
jupyter notebook
```

to open the Jupyter Notebook editor. Let's create a new notebook and run a couple of tests to see if everything acts as we expect.

![ciao](assets/week1_jupyter_test.PNG)

Now let's take a look at the dataset we actually need to use. The links are found in the official [dezoomcamp repository](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/2_docker_sql#ny-trips-dataset).

Important: the project was created using .CSV files, and while the official link now has the data in .PARQUET format, the DataTalksClub has a copy of the original .CSV file. However, since I have practice with opening and handling .CSV files, I decided to use the .PARQUET file and get a little practice with the pyarrow library.

(As I write this, I _immediately_ encounter an error: apparently I can import pyarrow.parquet as pq and use it, but I cannot import pyarrow as pa and then use pa.parquet. The reason for this apparent inconsistency can be found [here](https://github.com/modin-project/modin/issues/951))

![ciao](assets/week1_jupyter_parquet_error.PNG)

If everything works correctly, we will successfully read our data with Pandas.

![ciao](assets/week1_jupyter_dataframe_loaded.PNG)

Now that the data has been loaded from the source into Pandas, we need to move it from Pandas into our Postgres database. Of course, to be able to insert into our database, we will need to first establish a connection with it.

I'm going to import create_engine from sqlalchemy (visible in the first cell) and then we can use our credentials to connect with our docker container.

![ciao](assets/week1_jupyter_connect_to_postgres.PNG)

We can now write an instruction that will load the column names and types to create the schema we need in our Postgres database.

![ciao](assets/week1_jupyter_create_table.PNG)

Now we have another problem: we could _try_ to do one million three hundred sixty nine thousand inserts at the same time... but it might be better if we batch it.
Since I'm using the .PARQUET file, I wrote this code to handle the difference in formats.

![ciao](assets/week1_jupyter_ingestion.PNG)

### Finishing touches

We did it! We successfully read from a .PARQUET file and wrote into a database... or did we? Let's check by going back to our client Git Bash terminal and trying to see which tables, if any, are present in our ny_taxi database, and how many rows the database has.

![ciao](assets/week1_pgcli_db_is_not_empty.PNG)

:D We have succesfully loaded the data into the Postgres database!

---

[^ Back to table of contents](#table-of-contents)

---
## :movie_camera: Connecting pgAdmin and Postgres

Now that we have loaded the data, we can explore it a little bit. For example, we can see the datetime for the first pickup contained in the database, the date for the last pickup, and the maximum amount ever paid.

![code](assets/week1_postgres13_explore_the_data.PNG)

7k dollars! Well, that must have been a trip! We don't know if those are mistakes or actual records, we might need to analyze the dataset to see if those are extreme outliers that might be best to exclude from a careful analysis.

However, the terminal is not the best interface. Shall we use docker to run a pdAdmin container as our client?

```
winpty docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    dpage/pgadmin4
```

After we run this command in yet again another Git Bash terminal, this is my current predicament:

![ciao](assets/week1_server_client_pgAdmin_pgAdminWeb.PNG)

After filling the necessary fields to make pgAdmin connect to the database, we realize that the pgAdmin container and the server container cannot actually see each other, as they are running each in their own container.

The solution? We need to run a docker container that creates a network, and then we need to run the server container and the pdAdmin container _inside_ this container.

To assist in the understanding of the concept, I made a very detailed and very instructive drawing in powerpoint.

![ciao](assets/docker_network.png)

### Setting up the network of containers

It's easier than it sounds like: we just need to stop all the containers, create a new docker container by running the command:

```
winpty docker network create pg-network
```

And then we can run our server and pgAdmin containers again, adding a name (to easily identify the container) and which network they're part of.

```
winpty docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v /c/Users/drago/Documents/GitHub/dezoomcamp24/week1/docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:13
```

```
winpty docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4
```

Finally, we can access the server container from our client container.

![ciao](assets/week1_network_pgdatabase_pgadmin.PNG)

