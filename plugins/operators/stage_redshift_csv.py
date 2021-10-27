#from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.S3_hook import S3Hook

from operators.stage_redshift_base import StageToRedshiftBaseOperator

class StageToRedshiftCSVOperator(StageToRedshiftBaseOperator):
    """
    Copies JSON data from S3 to a Redshift Cluster
    """
    ui_color = '#358140'

    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        IGNOREHEADER {}
        DELIMITER '{}'
        CSV QUOTE AS '"'
    """


    def __init__(self,
                ignoreheader=1,
                delimiter=',',
                *args, **kwargs):
        """Initializes the operator

        Args:
            redshift_conn_id (str, optional): name of the connection created in Airflow. Defaults to "redshift".
            aws_credentials_id (str, optional): name of the connection created in Airflow. Defaults to "aws_credentials".
            table (str, optional): destination table. Defaults to "".
            s3_bucket (str, optional): source s3 bucket. Defaults to "".
            s3_key (str, optional): Folder inside the s3 bucket containing the data. Defaults to "".
            region (str, optional): AWS region of s3 bucket and the Redshift Cluster. Defaults to "eu-west-1".
        """
        super(StageToRedshiftCSVOperator, self).__init__(*args, **kwargs)
        self.ignoreheader = ignoreheader
        self.delimiter = delimiter

    def getFormatedSQL(self, table, s3_path, credentials):
        return StageToRedshiftCSVOperator.copy_sql.format(
            table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
            self.ignoreheader,
            self.delimiter
        )