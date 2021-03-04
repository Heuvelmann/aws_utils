## Instalación: 

Instalar mediante  **pip install git+https://github.com/Pactia/aws_utils**


## Ejemplo de uso simple: 

```python
from aws_helpers import aws_s3_helpers
s3_client_utils = aws_s3_helpers.AwsHelper(region = "us-east-1")
s3_client_utils = get_s3_sub_paths("pactia-datalake-in", "variables_externas/")
```

## TODO: 
1. Mejorar convencion de nombres 
2. Documentar funciones adicionales 
3. Ejemplo uso combinado sharepoint + s3
