from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from operators import ( LoadFactOperator, GenericDataQualityOperator,
                       StageToRedshiftParquetOperator)

from helpers import SqlQueries
from operators.load_dimension import LoadDimensionOperator
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

    # stage_i94imm_to_redshift = DummyOperator(task_id='Stage_i94imm',  dag=dag)
    stage_i94imm_to_redshift = StageToRedshiftParquetOperator(
        task_id='Stage_i94imm',
        dag=dag,
        table="public.i94imm_staging",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket=S3_BUCKET,
        s3_key="capestone-project/source-data/parquet"
    )

    # stage_temperature_to_redshift = DummyOperator(task_id='stage_temperature_to_redshift',  dag=dag)
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

    # stage_us_cities_demographics_to_redshift = DummyOperator(task_id='Stage_us_cities_demographics',  dag=dag)
    stage_us_cities_demographics_to_redshift = StageToRedshiftCSVOperator(
        task_id='Stage_us_cities_demographics',
        dag=dag,
        table="public.us_cities_demographics_staging",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket=S3_BUCKET,
        s3_key="capestone-project/source-data/us-cities-demographics.csv",
        delimiter=';',
        ignoreheader=1
    )

    # stage_airport_codes_to_redshift = DummyOperator(task_id='Stage_airport_codes',  dag=dag)
    stage_airport_codes_to_redshift = StageToRedshiftCSVOperator(
        task_id='Stage_airport_codes',
        dag=dag,
        table="public.airport_codes_staging",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket=S3_BUCKET,
        s3_key="capestone-project/source-data/airport-codes_csv.csv",
        delimiter=',',
        ignoreheader=1
    )

    # copy_i94addrl_mapping_to_redshift = DummyOperator(task_id='Copy_i94addrl_mappings',  dag=dag)
    copy_i94addrl_mapping_to_redshift = StageToRedshiftCSVOperator(
        task_id='Copy_i94addrl_mappings',
        dag=dag,
        table="public.state",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket=S3_BUCKET,
        s3_key="capestone-project/source-data/i94addrl_mapping.csv",
        delimiter=',',
        ignoreheader=1
    )

    # copy_i94_cit_res_mapping_to_redshift = DummyOperator(task_id='Copy_i94_cit_res_mappings',  dag=dag)
    copy_i94_cit_res_mapping_to_redshift = StageToRedshiftCSVOperator(
        task_id='Copy_i94_cit_res_mappings',
        dag=dag,
        table="public.country_mapping",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket=S3_BUCKET,
        s3_key="capestone-project/source-data/i94cntyl_mapping.csv",
        delimiter=',',
        ignoreheader=1
    )

    # copy_i94mode_mapping_to_redshift = DummyOperator(task_id='Copy_i94mode_mappings',  dag=dag)
    copy_i94mode_mapping_to_redshift = StageToRedshiftCSVOperator(
        task_id='Copy_i94mode_mappings',
        dag=dag,
        table="public.mode_mapping",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket=S3_BUCKET,
        s3_key="capestone-project/source-data/i94model_mapping.csv",
        delimiter=',',
        ignoreheader=1
    )

    # copy_i94port_mapping_to_redshift = DummyOperator(task_id='Copy_i94port_mappings',  dag=dag)
    copy_i94port_mapping_to_redshift = StageToRedshiftCSVOperator(
        task_id='Copy_i94port_mappings',
        dag=dag,
        table="public.port_mapping",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket=S3_BUCKET,
        s3_key="capestone-project/source-data/i94prtl_mapping.csv",
        delimiter=',',
        ignoreheader=1
    )

    # copy_i94visa_mapping_to_redshift = DummyOperator(task_id='Copy_i94visa_mappings',  dag=dag)
    copy_i94visa_mapping_to_redshift = StageToRedshiftCSVOperator(
        task_id='Copy_i94visa_mappings',
        dag=dag,
        table="public.visa_mapping",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket=S3_BUCKET,
        s3_key="capestone-project/source-data/i94visa_mapping.csv",
        delimiter=',',
        ignoreheader=1
    )

    load_visit_table = LoadFactOperator(
        task_id='Load_visit_fact_table',
        dag=dag,
        postgres_conn_id="redshift",
        table="public.visit",
        append=False,
        sql=SqlQueries.visit_table_insert
    )

    load_date_table = LoadDimensionOperator(
        task_id='Load_date_dim_table',
        dag=dag,
        postgres_conn_id="redshift",
        table="public.date",
        append=False,
        sql=SqlQueries.date_table_insert
    )

    load_airport_table = LoadDimensionOperator(
        task_id='Load_airport_dim_table',
        dag=dag,
        postgres_conn_id="redshift",
        table="public.port",
        append=False,
        sql=SqlQueries.airport_table_insert
    )

    load_port_city_table = LoadDimensionOperator(
        task_id='Load_port_city_dim_table',
        dag=dag,
        postgres_conn_id="redshift",
        table="public.port_city",
        append=False,
        sql=SqlQueries.port_city_table_insert
    )

    end_laod_data_operator = DummyOperator(task_id='End_load_data',  dag=dag)

    data_quality_checks = [
        # check table contents
        {'test_sql': "SELECT COUNT(*) FROM visit", 'expected_result': 0, "comparison": '>'},
        {'test_sql': "SELECT COUNT(*) FROM port", 'expected_result': 0, "comparison": '>'},
        {'test_sql': "SELECT COUNT(*) FROM country_mapping", 'expected_result': 0, "comparison": '>'},
        {'test_sql': "SELECT COUNT(*) FROM port_city", 'expected_result': 0, "comparison": '>'},
        {'test_sql': "SELECT COUNT(*) FROM mode_mapping", 'expected_result': 0, "comparison": '>'},
        {'test_sql': "SELECT COUNT(*) FROM visa_mapping", 'expected_result': 0, "comparison": '>'},
        {'test_sql': "SELECT COUNT(*) FROM state", 'expected_result': 0, "comparison": '>'},
        {'test_sql': "SELECT COUNT(*) FROM date", 'expected_result': 0, "comparison": '>'},
        # check doubles in primary keys
        {'test_sql': GenericDataQualityOperator.DBL_VALUES_TEMPLATE.format(table='port_city',pk_cols='city, state'), 'expected_result': 0, "comparison": 'none'},
        # check nulls in primary keys
        #{'test_sql': "SELECT COUNT(*) FROM users WHERE userid is NULL or level is NULL", 'expected_result': 0, "comparison": '='},
    ]

    run_quality_checks = GenericDataQualityOperator(
        task_id='Run_data_quality_checks',
        redshift_conn_id="redshift",
        checks=data_quality_checks,
        dag=dag
    )

    end_operator = DummyOperator(task_id='End_execution',  dag=dag)

    start_operator >> create_tables_task
    
    create_tables_task >> [
        stage_i94imm_to_redshift,
        #stage_temperature_to_redshift,
        stage_us_cities_demographics_to_redshift,
        stage_airport_codes_to_redshift]

    create_tables_task >> [
        copy_i94addrl_mapping_to_redshift,
        copy_i94_cit_res_mapping_to_redshift,
        copy_i94mode_mapping_to_redshift,
        copy_i94port_mapping_to_redshift,
        copy_i94visa_mapping_to_redshift
    ]

    stage_i94imm_to_redshift >> load_visit_table

    [stage_airport_codes_to_redshift, 
     copy_i94port_mapping_to_redshift] >> load_airport_table

    stage_us_cities_demographics_to_redshift >> load_port_city_table

    load_visit_table >> load_date_table

    [
        load_date_table,
        load_port_city_table,
        load_airport_table,
        copy_i94addrl_mapping_to_redshift,
        copy_i94_cit_res_mapping_to_redshift,
        copy_i94mode_mapping_to_redshift,
        copy_i94visa_mapping_to_redshift
    ] >> end_laod_data_operator

    end_laod_data_operator >> run_quality_checks >> end_operator