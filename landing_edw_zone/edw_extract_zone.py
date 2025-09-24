import pandas as pd
from sqlalchemy import create_engine
from google.cloud import bigquery
from decimal import Decimal
import logging
import sys

def to_bq():

    log_format = '[%(asctime)s] %(levelname)-8s [%(filename)s] %(message)s'
    log_datefmt = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    datefmt=log_datefmt,
    handlers=[logging.StreamHandler(sys.stdout)]
    )

    logging.info("Conexion con base de datos Postgres")

    PG_USER = "admin"
    PG_PASS = "admin1234"
    PG_HOST = "localhost"
    PG_PORT = 5432
    PG_DB   = "hites_oltp_db"

    # Pool de conexion a POSTGRESQL
    engine = create_engine(f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}")

    df_ventas     = pd.read_sql_query("SELECT * FROM public.ventas",    con=engine)
    df_productos  = pd.read_sql_query("SELECT * FROM public.productos", con=engine)
    df_clientes   = pd.read_sql_query("SELECT * FROM public.clientes",  con=engine)

    df_ventas["descuento_pct"] = df_ventas["descuento_pct"].apply(
        lambda v: None if pd.isna(v) else Decimal(str(v))
    )


    PROJECT = "mi-primer-proyecto-469023"
    DATASET = "demo_hites"
    BQ_LOCATION = "southamerica-east1"

    client = bigquery.Client(project=PROJECT)

    def ingesta_df(df: pd.DataFrame, table_name, write_disposition="WRITE_APPEND"):
        """
        Carga un DataFrame a una tabla existente en BigQuery
        """
        table_id = f"{PROJECT}.{DATASET}.{table_name}"
        table = client.get_table(table_id)

        if table.num_rows > 0:
            logging.info(f"La tabla {table_id} ya contiene {table.num_rows} filas. No se cargó nada.")
            return

        job_config = bigquery.LoadJobConfig(write_disposition=write_disposition)

        job = client.load_table_from_dataframe(
            df, table_id, job_config=job_config, location=BQ_LOCATION
        )
        job.result()

        logging.info(f"{len(df)} filas cargadas en {table.full_table_id} (total actual: {table.num_rows})")

    # --- Cargas ---
    ingesta_df(df_clientes,  "clientes")
    ingesta_df(df_productos, "productos")
    ingesta_df(df_ventas,    "ventas")

to_bq()