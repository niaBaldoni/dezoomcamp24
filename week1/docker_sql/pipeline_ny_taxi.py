
import argparse
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from sqlalchemy import create_engine
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    parq_name = 'output.parquet'

    os.system(f"wget {url} -O {parq_name}")
    

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    trips = pq.read_table(parq_name)
    df = trips.to_pandas()

    print(pd.io.sql.get_schema(df, name = table_name, con = engine))

    pf = pq.ParquetFile(parq_name)

    flag = False
    for batch in pf.iter_batches(batch_size = 40000):
        table = pa.Table.from_batches([batch])
        df = table.to_pandas()
        
        if flag == False:
            df.to_sql(name = table_name, con = engine, if_exists = 'replace')
            flag = True
        else:
            df.to_sql(name = table_name, con = engine, if_exists = 'append')
        
        print("Finished another chunk.")

    print("Finished ingesting data into the postgres database.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest PARQUET data to Postgres')

    # user, password, host, port, database name, table name, url of the parquet

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table-name', help='name of the table to write our results to')
    parser.add_argument('--url', help='url of the .parquet file')

    args = parser.parse_args()
    main(args)