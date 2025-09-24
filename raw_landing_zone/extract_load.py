import pandas as pd
import logging
import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError

def extract_file_data_int_main():
    log_format = '[%(asctime)s] %(levelname)-8s [%(filename)s] %(message)s'
    log_datefmt = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=log_datefmt,
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    logging.info("Procesamiento de datos con pandas\n")
    logging.info("Leyendo informacion desde DATA IN \n")
    logging.info("Leyendo informacion de df_clientes \n")

    df_clientes = pd.read_csv('/Users/gustavo/Desktop/Hites/data_in/clientes_hites.csv', sep=',', decimal=',', header=0)

    logging.info("###############################################")
    logging.info("Columnas referenciales al dataframe df_clientes")
    logging.info("###############################################")

    print('\n')

    for columna in df_clientes.columns:
        logging.info(columna)

    print('\n')
    print(df_clientes.head(5))

    print('\n')
    logging.info("Leyendo informacion de df_productos \n")

    df_productos = pd.read_csv('/Users/gustavo/Desktop/Hites/data_in/productos_hites.csv', sep=',', decimal=',', header=0)

    logging.info("###############################################")
    logging.info("Columnas referenciales al dataframe df_productos")
    logging.info("###############################################")
    print('\n')

    for columna in df_productos.columns:
        logging.info(columna)

    print('\n')
    print(df_productos.shape)
    print(df_productos.head(5))
    print(df_productos.describe())

    print('\n')
    logging.info("Leyendo informacion de df_ventas \n")

    df_ventas = pd.read_csv('/Users/gustavo/Desktop/Hites/data_in/ventas_hites.csv', sep=',', decimal=',', header=0)

    logging.info("###############################################")
    logging.info("Columnas referenciales al dataframe df_ventas")
    logging.info("###############################################")
    print('\n')

    for columna in df_ventas.columns:
        logging.info(columna)

    print('\n')
    print(df_ventas.shape)
    print(df_ventas.head(5))


    logging.info("#############################################")
    logging.info("Procesando informacion Conversion a Datetime")
    logging.info("#############################################")
    print('\n')

    logging.info("Convirtiendo fechas de tipo object a datetime")
    FMT_EXTEND='%Y-%m-%d %H:%M:%S'
    FMT='%Y-%m-%d'

    logging.info("Convirtiendo fechas de df_clientes")
    df_clientes["fecha_registro"] = pd.to_datetime(df_clientes["fecha_registro"], format=FMT, errors='coerce').dt.date
    df_clientes["fecha_nacimiento"] = pd.to_datetime(df_clientes["fecha_nacimiento"], format=FMT, errors='coerce').dt.date

    logging.info("Convirtiendo fechas de df_productos")
    df_productos["fecha_creacion"] = pd.to_datetime(df_productos["fecha_creacion"], format=FMT, errors='coerce').dt.date

    logging.info("Convirtiendo fechas de df_ventas")
    df_ventas["fecha_venta"] = pd.to_datetime(df_ventas["fecha_venta"], format=FMT_EXTEND, errors='coerce')

    logging.info("Convirtiendo datos numericos de df_ventas")
    df_ventas["descuento_pct"] = pd.to_numeric(df_ventas["descuento_pct"], errors='coerce')

    print('\n')
    logging.info("#################################################")
    logging.info("Procesando informacion Eliminando datos faltantes")
    logging.info("#################################################")
    print('\n')

    logging.info("Eliminando datos faltantes de df_clientes")
    df_clientes.dropna()
    logging.info("Eliminando datos faltantes de df_productos")
    df_productos.dropna()
    logging.info("Eliminando datos faltantes de df_ventas")
    df_ventas.dropna()

    print('\n')
    logging.info("##################################################")
    logging.info("Ingestando informacion en HITES_OLTP_DB POSTGRESQL")
    logging.info("##################################################")
    print('\n')

    logging.info("Estableciendo conexion a postgresql con el driver psycopg y ORM sqlalchemy")
    db_connection_str = 'postgresql+psycopg://admin:admin1234@localhost:5432/hites_oltp_db'
    db_engine = create_engine(db_connection_str)
    try:

        logging.info("Ingesta de datos desde df_clientes hacia tabla CLIENTES en POSTGRES")
        table_clientes='clientes'
        df_clientes.to_sql(table_clientes, con=db_engine, if_exists='append', schema='public', index=False)
        logging.info("Carga Exitosa de df_clientes")

        logging.info("Ingesta de datos desde df_productos hacia tabla PRODUCTOS en POSTGRES")
        table_productos='productos'
        df_productos.to_sql(table_productos, con=db_engine, if_exists='append', schema='public', index=False)
        logging.info("Carga Exitosa de df_productos")


        logging.info("Ingesta de datos desde df_ventas hacia tabla VENTAS en POSTGRES")
        table_ventas='ventas'
        df_ventas.to_sql(table_ventas, con=db_engine, if_exists='append', schema='public',  index=False)
        logging.info("Carga Exitosa de df_ventas")

    except IntegrityError as e:
        logging.error(f"Error de integridad (PK/FK/Unique): {e}")
        raise
    except OperationalError as e:
        logging.error(f"Error operacional (Conexiones): {e}")
        raise
    except ProgrammingError as e:
        logging.error(f"Error de SQL o esquema: {e}")
        raise
    except Exception as e:
        logging.exception("Error inesperado en to_sql")
        raise

extract_file_data_int_main()