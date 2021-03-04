import boto3
import pandas
import csv
import time
import os
from time import sleep
    
def clean_up(bucket:str) -> None:
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    for obj in bucket.objects.filter(Prefix='Query-Results/'):
        s3.Object(bucket.name,obj.key).delete()

    for obj in bucket.objects.filter(Prefix='temp/'):
        s3.Object(bucket.name, obj.key).delete()
        

class AthenaQueryFailed(Exception):
    pass


class Athena(object):
    S3_TEMP_BUCKET = "pactia-out-athena"

    def __init__(self, bucket=S3_TEMP_BUCKET):
        self.bucket = bucket
        self.client = boto3.Session().client("athena")


    def execute_query_in_athena(self, query, 
                                output_s3_directory = "temp/athena/output/",
                                database="datalake_pactia"):
        """ 
        """
        
        response = self.client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={"Database": database},
            ResultConfiguration={
                "OutputLocation": 's3://' + self.bucket + '/' + output_s3_directory}
        )
        query_execution_id = response["QueryExecutionId"]
        filename = "{filename}.csv".format(filename=response["QueryExecutionId"])
        s3_result_path = os.path.join('s3://' + self.bucket + '/' + output_s3_directory, filename)
        logger.info(
            "Query query_execution_id <<{query_execution_id}>>, result_s3path <<{s3path}>>".format(
                query_execution_id=query_execution_id, s3path=s3_result_path
            )
        )
        self.wait_for_query_to_complete(query_execution_id)
        return s3_result_path

    def wait_for_query_to_complete(self, query_execution_id):
        is_query_running = True
        backoff_time = 5
        while is_query_running:
            response = self.__get_query_status_response(query_execution_id)
            status = response["QueryExecution"]["Status"][
                "State"
            ]  # possible responses: QUEUED | RUNNING | SUCCEEDED | FAILED | CANCELLED
            if status == "SUCCEEDED":
                is_query_running = False
            elif status in ["CANCELED", "FAILED"]:
                logger.error(f"{response['QueryExecution']['Status']['StateChangeReason']}")
                raise AthenaQueryFailed(status)
            elif status in ["QUEUED", "RUNNING"]:
                logger.info("Esperando por {} segundos.".format(backoff_time))
                sleep(backoff_time)
            else:
                raise AthenaQueryFailed(status)

    def __get_query_status_response(self, query_execution_id):
        response = self.client.get_query_execution(QueryExecutionId=query_execution_id)
        return response