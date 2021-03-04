## Instalación: 

Instalar mediante  **pip install git+https://github.com/Pactia/aws_utils**


## Ejemplo de uso simple: 

```python
from aws_helpers import aws_s3_helpers
s3_client_utils = aws_s3_helpers.AwsHelper(region = "us-east-1")
list_objectos_en_la_ruta = s3_client_utils.get_s3_sub_paths("pactia-datalake-in", "variables_externas/")
```

## TODO: 
1. Mejorar convencion de nombres 
2. Documentar funciones adicionales 
3. Ejemplo uso combinado sharepoint + s3

## Clases y funciones disponibles
| Script             | Class            | function                             |
|--------------------|------------------|--------------------------------------|
| athena_helpers     | -                | clean_up                             |
| athena_helpers     | Athena           | _init__                              |
| athena_helpers     | Athena           | execute_query_in_athena              |
| athena_helpers     | Athena           | wait_for_query_to_complete           |
| athena_helpers     | Athena           | wait_for_query_to_complete           |
| aws_s3_helpers     | AwsHelper        | _init__                              |
| aws_s3_helpers     | AwsHelper        | download_from_s3                     |
| aws_s3_helpers     | AwsHelper        | uploadfile_to_s3                     |
| aws_s3_helpers     | AwsHelper        | uploadobj_to_s3                      |
| aws_s3_helpers     | AwsHelper        | create_bucket                        |
| aws_s3_helpers     | AwsHelper        | get_s3_sub_paths                     |
| aws_s3_helpers     | AwsHelper        | get_lastmod_file                     |
| aws_s3_helpers     | AwsHelper        | get_items_keys                       |
| aws_s3_helpers     | AwsHelper        | download_lastmod_file                |
| aws_s3_helpers     | AwsHelper        | download_all_files                   |
| aws_s3_helpers     | AwsHelper        | dataframe_to_aws                     |
| sharepoint_helpers | SharePointHelper | _init__                              |
| sharepoint_helpers | SharePointHelper | _share_auth                          |
| sharepoint_helpers | SharePointHelper | _get_auth_cookies                    |
| sharepoint_helpers | SharePointHelper | get_site                             |
| sharepoint_helpers | SharePointHelper | _to_timestamp                        |
| sharepoint_helpers | SharePointHelper | list_files_share                     |
| sharepoint_helpers | SharePointHelper | download_file                        |
| sharepoint_helpers | SharePointHelper | _make_key_for_recursive_upload_to_s3 |
| sharepoint_helpers | SharePointHelper | recursive_upload_files_to_s3         |
| sharepoint_helpers | SharePointHelper | download_last_mod_file               |
| sharepoint_helpers | SharePointHelper | recursive_dowload_lastfile           |
| sharepoint_helpers | SharePointHelper | upload_fileobj                       |
