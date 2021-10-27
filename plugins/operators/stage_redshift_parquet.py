from airflow.hooks.postgres_hook import PostgresHook

from operators.stage_redshift_base import StageToRedshiftBaseOperator

class StageToRedshiftParquetOperator(StageToRedshiftBaseOperator):
    """
    Copies Parquet data from S3 to a Redshift Cluster
    """
    ui_color = '#358140'

    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        FORMAT AS PARQUET
    """


    def __init__(self,
                 *args,
                 **kwargs):
        """Initializes the operator

        Args:
            redshift_conn_id (str, optional): name of the connection created in Airflow. Defaults to "redshift".
            aws_credentials_id (str, optional): name of the connection created in Airflow. Defaults to "aws_credentials".
            table (str, optional): destination table. Defaults to "".
            s3_bucket (str, optional): source s3 bucket. Defaults to "".
            s3_key (str, optional): Folder inside the s3 bucket containing the data. Defaults to "".
        """
        super(StageToRedshiftParquetOperator, self).__init__(*args, **kwargs)

    def getFormatedSQL(self, table, s3_path, credentials):
        return StageToRedshiftParquetOperator.copy_sql.format(
            table,
            s3_path,
            credentials.access_key,
            credentials.secret_key
        )