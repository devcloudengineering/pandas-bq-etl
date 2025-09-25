pip install "pandas==2.2.2" "SQLAlchemy==2.0.32" "psycopg[binary]==3.1.19" "numpy==1.26.4"

bq --location=southamerica-west1 mk --dataset mi-primer-proyecto-469023:stg_assert
bq --location=southamerica-west1 mk --dataset mi-primer-proyecto-469023:mart
bq --location=southamerica-west1 mk --dataset mi-primer-proyecto-469023:stg
bq --location=southamerica-west1 mk --dataset mi-primer-proyecto-469023:raw

gsutil cp ventas_hites.csv gs://data_in_hites/
gsutil cp productos_hites.csv gs://data_in_hites/
gsutil cp clientes_hites.csv gs://data_in_hites/

conda activate airflow_env

export AIRFLOW_HOME="/Users/gustavo/Desktop/DataEngineer/pandas-bq/Hites/airflow"
export AIRFLOW_CORE_DAGS_FOLDER="$AIRFLOW_HOME/dags"
mkdir -p "$AIRFLOW_HOME"/{dags,logs,plugins}
airflow info | egrep -i "airflow_home|dags_folder"
pkill -f "airflow webserver" || true
pkill -f "airflow scheduler" || true
airflow standalone
