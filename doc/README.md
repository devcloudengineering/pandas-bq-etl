pip install "pandas==2.2.2" "SQLAlchemy==2.0.32" "psycopg[binary]==3.1.19" "numpy==1.26.4"

bq --location=southamerica-west1 mk --dataset mi-primer-proyecto-469023:stg_assert
bq --location=southamerica-west1 mk --dataset mi-primer-proyecto-469023:mart
bq --location=southamerica-west1 mk --dataset mi-primer-proyecto-469023:stg
bq --location=southamerica-west1 mk --dataset mi-primer-proyecto-469023:raw

gsutil cp ventas_hites.csv gs://data_in_hites/
gsutil cp productos_hites.csv gs://data_in_hites/
gsutil cp clientes_hites.csv gs://data_in_hites/

conda activate airflow_env

# Fija versión estable y tu Python

export AIRFLOW_VERSION=2.10.5
export PYTHON_VERSION=3.11
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

# Sube Airflow y sus dependencias con constraints

pip install --upgrade "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# re-instala el provider FAB según constraints

pip install --upgrade "apache-airflow-providers-fab" --constraint "${CONSTRAINT_URL}"

# Asegura tu HOME y hostname

export AIRFLOW_HOME="/Users/gustavo/Desktop/Hites/airflow"

# Migra BD y levanta

airflow db upgrade
airflow standalone
