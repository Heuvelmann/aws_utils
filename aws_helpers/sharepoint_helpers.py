from shareplum import Site
from shareplum.site import Version
from shareplum import Office365
from aws_s3_helpers import AwsHelper
import os 
import json
import re
import boto3
from datetime import datetime
from typing import List, NamedTuple
#from config import username, password
import requests
import logging
import sys


## Dataobjects


sharepoint_file = NamedTuple("sharepoint_file", [("folder", str),
                                                 ("name", str), 
                                                 ("created_at", datetime)])
class SharePointHelper:
  
    def __init__(self, username:str, password:str):
        self.username = username
        self.password = password
        self.office_auth = self._share_auth()
    
    def _share_auth(self) -> Office365: 
        auth_base = Office365('https://pactia.sharepoint.com',
                           username=self.username, password=self.password)
        return auth_base
    
    def _get_auth_cookies(self):
        office_auth = self.office_auth
        sec_token = office_auth.get_security_token(office_auth.username, 
                                               office_auth.password)
        url = "https://pactia.sharepoint.com/_forms/default.aspx?wa=wsignin1.0"
        response = requests.post(url, data = sec_token)
        return response.cookies
        
    def get_site(self) -> Site:
        site = Site("https://pactia.sharepoint.com/sites/AnalticaAI", 
            version = Version.v365, authcookie = self._get_auth_cookies())
        return site
    
    
    def _to_timestamp(self, share_time:str) -> datetime: 
        return datetime.fromisoformat(share_time[:-1]).date()
    
    
    def list_files_share(self,folder_name:str) -> List[NamedTuple]: 
        folder = self.get_site().Folder(folder_name)
        return [sharepoint_file(folder_name, 
                            file["Name"],
                            self._to_timestamp(file["TimeCreated"])) for file in folder.files]

    def download_file(self, folder_name:str, file_name:str) -> None:
        response = self.get_site().Folder(folder_name).get_file(file_name)
        #last = folder_name.split("/")[-1]
        if os.path.isdir(f'tmp/{folder_name}'): 
            with open(f'tmp/{folder_name}/{file_name}', mode="wb") as f: 
                f.write(response)
        else: 
            os.makedirs(f'tmp/{folder_name}')
            with open(f'tmp/{folder_name}/{file_name}', mode="wb") as f: 
                f.write(response)
        return f'tmp/{folder_name}/{file_name}'
    
    def _make_key_for_recursive_upload_to_s3(self, ruta, cache_base_folder_name):
        return f"{cache_base_folder_name}{ruta.split(cache_base_folder_name)[1]}"
    
    def recursive_upload_files_to_s3(self,folder_name, folder_name_cache,
                                     bucket=None, base_prefix=None):
        s3_client = AwsHelper()
        folder_cache = folder_name_cache
        folder = self.get_site().Folder(folder_name)
        print(folder_name)
        print(folder_cache)
        files = [sharepoint_file(folder_name, 
                            file["Name"],
                            self._to_timestamp(file["TimeCreated"])) for file in folder.files]
        rutas = [self.download_file(folder_name, file.name) for file in files]
       # [s3_client.uploadfile_to_s3(ruta, bucket, key = base_prefix + \
       #     self._make_key_for_recursive_upload_to_s3(ruta,folder_cache)) for ruta in rutas]
        for fol in folder.folders:
            print(f'{folder_name}/{fol}')
            self.recursive_upload_files_to_s3(f'{folder_name}/{fol}', folder_cache, bucket, base_prefix)
        
        
    def download_last_mod_file(self, folder_name:str) -> None:
        items = self.list_files_share(self.get_site(), folder_name) 
        items.sort(key=lambda namedt: namedt[2], reverse=True)
        self.download_file(self.get_site(), folder_name, items[0].name)
        
    
    def recursive_dowload_lastfile(self, folder_name:str) -> None:
        site = self.get_site()
        folder = site.Folder(folder_name) 
        for fol in folder.folders:
            fol_dow = f'{folder_name}/{fol}' 
            download_last_mod_file(site, fol_dow)
            
    def upload_fileobj(self, folder_name, upload_fileobj):
        folder = self.get_site().Folder(folder_name)
        with open(upload_fileobj, "r") as file:
            folder.upload_file(file.read(), upload_fileobj)      
            
            



     

    
        


        

        


def to_timestamp(share_time:str) -> datetime: 
    return datetime.fromisoformat(share_time[:-1]).date()

    
    
    
# ==============================================================================================================

