from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from operators import ( LoadFactOperator, GenericDataQualityOperator,
                       StageToRedshiftParquetOperator)

from helpers import SqlQueries
from operators.stage_redshift_csv import StageToRedshiftCSVOperator



DAG_ID = 'capstone_project_dag2'
S3_BUCKET = Variable.get("s3_bucket")
START_DATE = datetime(2021, 10, 12)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': START_DATE,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'schedule_interval': None,
    'max_active_runs': 1
}

with DAG(
    DAG_ID,
    default_args=default_args,
) as dag:

    start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)
    
    # added as described here: https://knowledge.udacity.com/questions/163614
    create_tables_task = PostgresOperator(
        task_id="create_tables",
        dag=dag,
        sql='create_tables.sql',
        postgres_conn_id="redshift"
    )

    stage_i94imm_to_redshift = DummyOperator(task_id='Stage_i94imm',  dag=dag)
    # stage_i94imm_to_redshift = StageToRedshiftParquetOperator(
    #     task_id='Stage_i94imm',
    #     dag=dag,
    #     table="public.i94imm_staging",
    #     redshift_conn_id="redshift",
    #     aws_credentials_id="aws_credentials",
    #     s3_bucket=S3_BUCKET,
    #     s3_key="capestone-project/source-data/parquet"
    # )

    stage_temperature_to_redshift = DummyOperator(task_id='stage_temperature_to_redshift',  dag=dag)
    # stage_temperature_to_redshift = StageToRedshiftCSVOperator(
    #     task_id='Stage_temperature',
    #     dag=dag,
    #     table="public.temperature_staging",
    #     redshift_conn_id="redshift",
    #     aws_credentials_id="aws_credentials",
    #     s3_bucket=S3_BUCKET,
    #     s3_key="capestone-project/source-data/GlobalLandTemperaturesByCity.csv",
    #     delimiter=',',
    #     ignoreheader=1
    # )

    stage_us_cities_demographics_to_redshift = DummyOperator(task_id='Stage_us_cities_demographics',  dag=dag)
    # stage_us_cities_demographics_to_redshift = StageToRedshiftCSVOperator(
    #     task_id='Stage_us_cities_demographics',
    #     dag=dag,
    #     table="public.us_cities_demographics_staging",
    #     redshift_conn_id="redshift",
    #     aws_credentials_id="aws_credentials",
    #     s3_bucket=S3_BUCKET,
    #     s3_key="capestone-project/source-data/us-cities-demographics.csv",
    #     delimiter=';',
    #     ignoreheader=1
    # )

    stage_airport_codes_to_redshift = DummyOperator(task_id='Stage_airport_codes',  dag=dag)
    # stage_airport_codes_to_redshift = StageToRedshiftCSVOperator(
    #     task_id='Stage_airport_codes',
    #     dag=dag,
    #     table="public.airport_codes_staging",
    #     redshift_conn_id="redshift",
    #     aws_credentials_id="aws_credentials",
    #     s3_bucket=S3_BUCKET,
    #     s3_key="capestone-project/source-data/airport-codes_csv.csv",
    #     delimiter=',',
    #     ignoreheader=1
    # )



    end_operator = DummyOperator(task_id='End_execution',  dag=dag)

    start_operator >> create_tables_task >> [
        stage_i94imm_to_redshift,
        stage_temperature_to_redshift,
        stage_us_cities_demographics_to_redshift,
        stage_airport_codes_to_redshift] >> end_operator