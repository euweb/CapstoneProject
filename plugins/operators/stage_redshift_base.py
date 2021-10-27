#from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.models import BaseOperator
import abc

class StageToRedshiftBaseOperator(BaseOperator):
    """
    Copies data from S3 to a Redshift Cluster
    """
    ui_color = '#358140'

    def __init__(self,
                 redshift_conn_id="redshift",
                 aws_credentials_id="aws_credentials",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 *args, **kwargs):
        """Initializes the operator

        Args:
            redshift_conn_id (str, optional): name of the connection created in Airflow. Defaults to "redshift".
            aws_credentials_id (str, optional): name of the connection created in Airflow. Defaults to "aws_credentials".
            table (str, optional): destination table. Defaults to "".
            s3_bucket (str, optional): source s3 bucket. Defaults to "".
            s3_key (str, optional): Folder inside the s3 bucket containing the data. Defaults to "".
        """
        super(StageToRedshiftBaseOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.aws_credentials_id = aws_credentials_id

    @abc.abstractmethod
    def getFormatedSQL(self, table, s3_path, credentials):
        return

    def execute(self, context):
        aws_hook = S3Hook(aws_conn_id=self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Clearing data from destination Redshift table {self.table}")
        redshift.run("DELETE FROM {}".format(self.table))

        self.log.info("Copying data from S3 to Redshift")
        rendered_key = self.s3_key.format(**context)
        s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)

        formatted_sql = self.getFormatedSQL(self.table, s3_path, credentials)

        redshift.run(formatted_sql)