'''
Author: Tong hetongapp@gmail.com
Date: 2025-02-14 15:53:34
LastEditors: Tong tong.he@generac.com
LastEditTime: 2025-03-15 10:23:57
FilePath: /server/src/services/services.py
Description: all integrated services
'''
import json, time, requests
from os.path import dirname, abspath
from config.config import flight_data_path, flight_dec_data_path, geo_data_path 
import sys
import re
import os
# sys.path.insert(1, '../')
import arrow
import json
from dataclasses import asdict
from dotenv import load_dotenv, find_dotenv
from services.rid_definitions import LatLngPoint, RIDOperatorDetails, UASID, OperatorLocation, UAClassificationEU
from rich.console import Console
console = Console()


class Api():
    def __init__(self, credentials, argonserver_url):        
        self.credentials = credentials
        self.argonserver_url = argonserver_url
    def status(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.credentials["access_token"],
        }
        securl = f"{self.argonserver_url}/scd/flight_planning/status"
        response = requests.get(securl, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json() 
            for key, value in data.items():
                console.print(f"{key.upper()}: {value}", style="bold yellow")
        return response 
        
class ArgonServerUploader():

    def __init__(self, credentials, argonserver_url):        
        self.credentials = credentials
        self.argonserver_url = argonserver_url
    def submit_air_traffic(self, filename: str = flight_data_path):
        with open(filename, "r") as traffic_json_file:
            traffic_json = traffic_json_file.read()
            
        traffic_json = json.loads(traffic_json)
        
        for current_reading in traffic_json: 
            icao_address = current_reading['icao_address']
            traffic_source = current_reading["traffic_source"]
            source_type = current_reading["source_type"]
            lat_dd = current_reading['lat_dd']
            lon_dd = current_reading['lon_dd']
            time_stamp = current_reading['timestamp']
            altitude_mm = current_reading['altitude_mm']                
            metadata = current_reading['metadata']
            headers = {
                "Content-Type":'application/json', 
                "Authorization": "Bearer " + self.credentials['access_token']
            }
            
            payload = {
                "observations": [{
                    "icao_address": icao_address,
                    "traffic_source": traffic_source,
                    "source_type": source_type,
                    "lat_dd": lat_dd,
                    "lon_dd": lon_dd,
                    "time_stamp": time_stamp,
                    "altitude_mm": altitude_mm,
                    'metadata': metadata
                }]
            }
            
            securl = f"{self.argonserver_url}/flight_stream/set_air_traffic"
            try:
                response = requests.post(securl, json=payload, headers=headers, timeout=10)
                response.raise_for_status() 
            except requests.exceptions.RequestException as e:
                console.print(f"Error during request: {e}", style="bold red")               
            else:
                print("Data uploaded successfully. Sleeping 10 seconds...")
                time.sleep(10)
                
    def upload_flight_declaration(self, filename: str = flight_dec_data_path):
        with open(filename, "r") as flight_declaration_file:
            f_d = flight_declaration_file.read()
            
        
        flight_declaration = json.loads(f_d)
        # now = arrow.now()
        # one_minute_from_now = now.shift(minutes =1)
        # four_minutes_from_now = now.shift(minutes =4)

        # # Update start and end time 
        # flight_declaration['start_datetime']= one_minute_from_now.isoformat()
        # flight_declaration['end_datetime'] = four_minutes_from_now.isoformat()
        headers = {"Content-Type":'application/json',"Authorization": "Bearer "+ self.credentials['access_token']}            
        securl = f"{self.argonserver_url}/flight_declaration_ops/set_flight_declaration" # set this to self (Post the json to itself)        
        response = requests.post(securl, json = flight_declaration, headers = headers, timeout=10)     
        if response.status_code == 200:
            flight_declaration_success =response.json()
            flight_declaration_id = flight_declaration_success['id']
            console.print("Flight Declaration Submitted...", style="bold green") 
            print(f"Flight Declaration ID: {flight_declaration_id}\n")
        else: 
            console.print("Error in submitting flight declaration...\n", style="bold red") 
        return response
    
    def update_operation_state(self,operation_id:str, new_state:int):        

        headers = {"Content-Type":'application/json',"Authorization": "Bearer "+ self.credentials['access_token']}            

        payload = {"state":new_state, "submitted_by":"hetongapp@gmail.com"}      
        securl = f"{self.argonserver_url}/flight_declaration_ops/flight_declaration_state/{operation_id}".format(operation_id=operation_id) # set this to self (Post the json to itself)        
        response = requests.put(securl, json = payload, headers = headers, timeout=10)
        if response.status_code == 200:
            console.print(f"Flight state has been changed to : {new_state}\n", style="bold green")  
        else: 
            flight_status_failed =response.json()
            flight_status_msg = flight_status_failed['state']
            console.print(flight_status_msg[0], style="bold red")  
        return response
    
    def submit_telemetry(self, filename, operation_id):
        with open(filename, "r") as rid_json_file:
            rid_json = rid_json_file.read()
            
        rid_json = json.loads(rid_json)
        
        states = rid_json['current_states']
        rid_operator_details  = rid_json['flight_details']
        
        uas_id = UASID(registration_id = 'CHE-5bisi9bpsiesw',  serial_number='d29dbf50-f411-4488-a6f1-cf2ae4d4237a',utm_id= '07a06bba-5092-48e4-8253-7a523f885bfe')
        eu_classification = UAClassificationEU()
        operator_location = OperatorLocation(position = LatLngPoint(lat = 46.97615311620088,lng = 7.476099729537965))
        rid_operator_details = RIDOperatorDetails(
            id= operation_id,
            uas_id = uas_id,
            operation_description="Medicine Delivery",
            operator_id='CHE-076dh0dq',
            eu_classification = eu_classification,            
            operator_location=  operator_location
        )
        for state in states: 
            headers = {"Content-Type":'application/json',"Authorization": "Bearer "+ self.credentials['access_token']}            

            payload = {"observations":[{"current_states":[state], "flight_details": {"rid_details" :asdict(rid_operator_details), "aircraft_type": "Helicopter","operator_name": "Thomas-Roberts" }}]}            
            securl = f"{self.argonserver_url}/flight_stream/set_telemetry" # set this to self (Post the json to itself)
            try:
                response = requests.put(securl, json = payload, headers = headers, timeout=10)
                
            except Exception as e:                
                print(e)
            else:
                if response.status_code == 201:
                    print("Sleeping 3 seconds..")
                    time.sleep(3)
                else: 
                    print(response.json())
      
    def get_flight_id(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.credentials["access_token"],
        }
        securl = f"{self.argonserver_url}/flight_declaration_ops/flight_declaration"
        response = requests.get(securl, headers=headers, timeout=10)
        if response.status_code == 200:
            flight_declaration_success = response.json()
            valid_ids = find_valid_ids(flight_declaration_success)
            console.print("Valid Flight Declaration IDs:", style="bold cyan")
            for flight_id in valid_ids:
                console.print(f"ID: {flight_id}", style="bold green")
        return response  
    
    def get_flight_detail(self,operation_id:str):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.credentials["access_token"],
        }
        securl = f"{self.argonserver_url}/flight_declaration_ops/flight_declaration/{operation_id}".format(operation_id=operation_id)
        response = requests.get(securl, headers=headers, timeout=10)
        if response.status_code == 200:
            print("Valid Flight Declaration IDs:")
            data = response.json()  # 解析 JSON 数据
            #docs_dir = os.path.join(os.path.expanduser("~"), "docs")
            #docs_dir = os.path.join(os.path.dirname(os.getcwd()), "docs")
            current_dir = os.path.dirname(os.path.abspath(__file__))
            docs_dir = os.path.join(current_dir, "docs")
            os.makedirs(docs_dir, exist_ok=True)  # 确保 docs 目录存在
            print(f"Flight details saved to {docs_dir}")
            file_path = os.path.join(docs_dir, f"{operation_id}.json")

            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)  # 写入 JSON 文件
        
            print(f"Flight details saved to {file_path}")
        return response    


class Geofence():
    def __init__(self, credentials, argonserver_url):        
        self.credentials = credentials
        self.argonserver_url = argonserver_url   

    def submit_geofence(self,filename: str = geo_data_path):
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found.")
            return

        with open(filename, "r") as geo_data_path:
            geo_json = json.load(geo_data_path)
        if geo_json.get("type") != "FeatureCollection" or "features" not in geo_json:
            print("Error: Invalid GeoJSON format.")
            return
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.credentials["access_token"]
        }
        securl = f"{self.argonserver_url}/geo_fence_ops/set_geo_fence"
        try:
            response = requests.put(securl, json=geo_json, headers=headers, timeout=10)
            response.raise_for_status()  
            response_data = response.json() 
            geofence_id = response_data.get("id")
            message = response_data.get("message", "No message returned")

            console.print(f"{message}",style="bold green")
            console.print(f"Geofence ID: {geofence_id}",style="bold green")
        except requests.exceptions.RequestException as e:
            console.print(f"Error during request: {e}",style="bold red")
        else:
            console.print("Geofence data uploaded successfully.",style="bold green")
          
    def get_geo_detail(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.credentials["access_token"],
        }
        securl = f"{self.argonserver_url}/geo_fence_ops/geo_fence"
        response = requests.get(securl, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json() 
            # docs_dir = os.path.join(os.path.expanduser("~"), "docs")
            #docs_dir = os.path.join(os.path.dirname(os.getcwd()), "docs")
            current_dir = os.path.dirname(os.path.abspath(__file__))
            docs_dir = os.path.join(current_dir, "docs")
            os.makedirs(docs_dir, exist_ok=True) 

            file_path = os.path.join(docs_dir, "geo_data.json")

            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)  
        
            print(f"Geo details saved to {file_path}")
        return response    






def is_valid_id(id_value):
    uuid_pattern = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
    return bool(uuid_pattern.match(id_value))

def find_valid_ids(data):
    valid_ids = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "id" and is_valid_id(str(value)): 
                valid_ids.append(value)
            
            elif isinstance(value, (dict, list)):
                valid_ids.extend(find_valid_ids(value))
    
    elif isinstance(data, list):
        for item in data:
            valid_ids.extend(find_valid_ids(item))
    
    return valid_ids