import os
import time
import datetime
import requests
from string import Template
import json
try:
    from onesaitplatform.common.log import log
    import onesaitplatform.common.config as config
except Exception as e:
    print("Error - Not possible to import necesary libraries: {}".format(e))


class FileManager:
    """ 
    Class FileManager to make operations with binary repository
    """
    protocol = "https"
    binary_files_path = "/controlpanel/binary-repository"
    
    upload_template = Template("$protocol://$host$path")
    
    def __init__(self, 
                 host = config.HOST,
                 user_token = config.USER_TOKEN):
        """ 
        Class FileManager to make operations with binary repository

        @param host               Onesaitplatform host
        @param user_token         Onesaitplatform user-token
        """
        self.host = host
        self.user_token = user_token

    def __str__(self):
        """
        String to print object info
        """
        hide_attributes = []
        info = "{}".format(self.__class__.__name__)
        info += "("
        for k, v in self.__dict__.items():
            if k not in hide_attributes:
                info += "{}={}, ".format(k, v)
        info = info[:-2] + ")"
        
        return info
            

    def upload_file(self, filename, filepath):
        """
        Upload a file to binary-repository

        @param filename           file name
        @param filepath           file path
        """
        _ok = False
        _res = None
        try:
            
            if not os.path.exists(filepath):
                raise IOError("Source file not found: {}".format(filepath))

            url = self.upload_template.substitute(protocol=self.protocol, host = self.host, path = self.binary_files_path)
            headers = {'Authorization': self.user_token}
            files_to_up = {'file':(filename, open(filepath, 'rb'), "multipart/form-data")}

            response = requests.request("POST", url, headers=headers, files=files_to_up)

            if response.status_code == 201:
                _ok = True
                _res = {"id": response.text,
                       "msg": "Succesfully uploaded file"}

            else:
                raise Exception("Response: {} - {}".format(response.status_code, response.text))

        except Exception as e:
            log.error("Not possible to upload file: {}".format(e))
            _res = e

                
        return _ok, _res

    # TODO: download file from binary repository
    def download_file(self):
        print("TODO: Download file")
        print("We are working on it yet... It will be ready soon :D")
    