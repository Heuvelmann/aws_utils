import boto3
import logging
from aws_helpers.logger import logger
from botocore.exceptions import ClientError
import pandas as pd
from datetime import date
from typing import NamedTuple
import os
#logger = logging.getLogger(cfg.logger_app_name)

bucket_object = NamedTuple("bucket_object", [("bucket", str),
                                             ("key", str), 
                                             ("fecha", str)])

class AwsHelper:
    """[summary]
    """  
    def __init__(self, region):
        self.s3_client = boto3.client('s3', region_name=region)

    def download_from_s3(self, bucket: str, key: str, local_path: str):
        """[summary]

        Parameters
        ----------
        bucket : str
            [description]
        key : str
            [description]
        local_path : str
            [description]

        Returns
        -------
        [type]
            [description]
        """      
        logger.info(f'Se ha empezado a descargar el archivo a S3 en la ruta {bucket} {key} \n')
        try:
            self.s3_client.download_file(bucket, key, local_path)
            logger.info('Se ha descargado el archivo correctamente.')
        except (Exception, ClientError) as e:
            logger.error(f'Error descargando desde S3, {e}')
            if e.response['Error']['Code'] == '404':
                logging.info('El objeto no existe')
        return None

    def uploadfile_to_s3(self, local_path: str, bucket: str, key: str, with_kms: bool = False):
        """[summary]

        Parameters
        ----------
        local_path : str
            [description]
        bucket : str
            [description]
        key : str
            [description]
        with_kms : bool, optional
            [description], by default False

        Returns
        -------
        [type]
            [description]
        """     
        logger.info(f'Se ha empezado a cargar el archivo a S3 en la ruta {bucket} {key} \n')
        if with_kms:
            try:
                self.s3_client.upload_file(local_path, bucket, key, extra_args={'ServiceSideEncryption': 'aws:kms',
                                                                                'SS#KMSKeyId': '<<your_kms_key>>'})
                logger.info('Se ha cargado el archivo en S3 correctamente.')
            except (Exception, ClientError) as e:
                logger.error(f'Error caragando a S3, {e}')
        else:
            try:
                self.s3_client.upload_file(local_path, bucket, key)
                logger.info('Se ha cargado el archivo en S3 correctamente.')
            except (Exception, ClientError) as e:
                logging.error(f'Error cargando a S3, {e}')
        return None
    def uploadobj_to_s3(self, binary_obj: str, bucket: str, key: str, with_kms: bool = False):
        logger.info(f'Se ha empezado a cargar el archivo a S3 en la ruta {bucket} {key} \n')
        if with_kms:
            try:
                self.s3_client.put_object(Body = binary_obj, 
                                          Bucket = bucket, 
                                          Key = key, 
                                          extra_args={'ServiceSideEncryption': 'aws:kms',
                                                                                'SS#KMSKeyId': '<<your_kms_key>>'})
                logger.info('Se ha cargado el archivo en S3 correctamente.')
            except (Exception, ClientError) as e:
                logger.error(f'Error caragando a S3, {e}')
        else:
            try:
                self.s3_client.put_object(Body = binary_obj, 
                                          Bucket = bucket, 
                                          Key = key)
                logger.info('Se ha cargado el archivo en S3 correctamente.')
            except (Exception, ClientError) as e:
                logging.error(f'Error cargando a S3, {e}')
        return None
    
    def create_bucket(self, bucket_name:str,region:str , configuration:dict = None):
        
        configuration_buck = {'LocationConstraint': region}
        configuration_buck.update(configuration)

        logger.info(f"Creando bucket con el nombre {bucket_name}")
        
        try: 
            self.s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration=configuration)
        except (Exception, ClientError) as e: 
            logging.error(f'Error creando bucket, {e}')
            
        return None
    
    def get_s3_sub_paths(self,bucket, prefix):
        response = self.s3_client.list_objects_v2(
            Bucket=bucket,
            StartAfter = prefix,
            Prefix= prefix)
        return [bucket_object(bucket ,Item["Key"], Item["LastModified"])  for Item in response["Contents"]]
    
    def get_lastmod_file(self, bucket: str, prefix:str):
        items = self.get_s3_sub_paths(bucket = bucket, prefix = prefix)
        items.sort(key = lambda tup: tup.fecha, reverse = True)
        return f's3://{bucket}/{items[0].key}'
    
    def get_items_keys(self, bucket, prefix):
        items = self.get_s3_sub_paths(bucket = bucket, prefix = prefix)
        items.sort(key = lambda tup: tup.fecha, reverse = True)
        return items
    
    def download_lastmod_file(self,bucket, prefix):
        items = self.get_s3_sub_paths(bucket = bucket, prefix = prefix )
        items.sort(key=lambda tup: tup.fecha, reverse=True)
    
        if os.path.isdir(f'tmp/{prefix}'): 
             self.download_from_s3(items[0].bucket,items[0].key, f'tmp/{items[0].key}')
        else: 
            os.makedirs(f'tmp/{prefix}')
            self.download_from_s3(items[0].bucket,items[0].key, f'tmp/{items[0].key}')
        print(items[0].key)
        return f'tmp/{items[0].key}'
    
    def download_all_files(self, bucket, prefix): 
        items = self.get_s3_sub_paths(bucket = bucket, prefix = prefix)
        for item in items: 
            if os.path.isdir(f'tmp/{prefix}'): 
                self.download_from_s3(item.bucket,item.key, f'tmp/{item.key}')
            else: 
                os.makedirs(f'tmp/{prefix}')
                self.download_from_s3(item.bucket,item.key, f'tmp/{item.key}')
        return f'tmp/{prefix}'

    
    
def dataframe_to_aws(df: pd.DataFrame, bucket, key, format, **kwargs) -> None:
    date_str = date.today().strftime("%Y-%m-%d")
    name_data = key.split("/")[-2]
    try:
        (nrows, ncols) = df.shape
        logger.info(f'Cargando el dataframe {name_data} en la ruta {key}')
        logger.info(f'{name_data} Posee {ncols} columnas y {nrows} observaciones')
        logger.info(f'{name_data} head - {df.head().to_string()}')
        if format == "parquet":
            df.to_parquet(f's3://{bucket}/{key}{date_str}.parquet', 
                          index=False, **kwargs)
        else: 
            df.to_csv(f's3://{bucket}/{key}{date_str}.csv',
                      index=False,**kwargs)
    except Exception as e: 
        logger.error(f"Problema en {e}")
    return None
    
    