'''
Author: Tong hetongapp@gmail.com
Date: 2025-02-14 15:11:52
LastEditors: Tong hetongapp@gmail.com
LastEditTime: 2025-02-15 18:16:42
FilePath: /server/src/config/config.py
Description: global configurations
'''
# singleton_config.py
from auth.auth import Auth
import uuid
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, "config.json")
flight_data_path = os.path.join(current_dir, "flight_data.json")
flight_dec_data_path = os.path.join(current_dir, "flight_dec_data.json")
geo_data_path = os.path.join(current_dir, "geo_data.json")
class GlobalConfig:
    _instance = None
    access_token = None
    uuid = None
    argon_server_url = None 
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(GlobalConfig, cls).__new__(cls)
            cls._instance.load_config()
            cls._instance.get_access_token()  
            cls._instance.generate_uuid()
        return cls._instance
    
    def load_config(self):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                self.argon_server_url = config.get("ARGON_SERVER_URL", "")
        except Exception as e:
            print(f"Error loading config: {e}")

    def set_access_token(self, token):
        self.access_token = token

    def get_access_token(self, scopes: str = "argonserver.write", audience: str = "utm.test"):
        adapter = Auth()
        token = adapter.issue_token(audience, scopes.split(' '))
        t_data = {'access_token': token}
        self.set_access_token(t_data)
        return t_data
    
    def generate_uuid(self):
        self.uuid = str(uuid.uuid4()) 
        return self.uuid
