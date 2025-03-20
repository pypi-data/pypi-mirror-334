'''
Author: Tong hetongapp@gmail.com
Date: 2025-02-14 14:07:26
LastEditors: Tong hetongapp@gmail.com
LastEditTime: 2025-02-16 09:28:22
FilePath: /server/src/server/server.py
Description: main module
'''

import time
import random
import logging
import multiprocessing
from services.services import ArgonServerUploader, Geofence, Api
from config.config import GlobalConfig
import inspect
from rich.console import Console

Config = GlobalConfig()
console = Console()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
uploader = ArgonServerUploader(credentials=Config.access_token, argonserver_url=Config.argon_server_url)
geo_sever = Geofence(credentials=Config.access_token, argonserver_url=Config.argon_server_url)
api = Api(credentials=Config.access_token, argonserver_url=Config.argon_server_url)

OPERATION_STATES = (
    (0, "Not Submitted"),
    (1, "Accepted"),
    (2, "Activated"),
    (3, "Nonconforming"),
    (4, "Contingent"),
    (5, "Ended"),
    (6, "Withdrawn"),
    (7, "Cancelled"),
    (8, "Rejected"),
)

class AirTrafficSubmit:
    def run(self):
        uploader.submit_air_traffic()

class FlightDeclSubmit:
    def run(self):
        uploader.upload_flight_declaration()

class ListDeclID:
    def run(self):
        uploader.get_flight_id()

class UpdateOprState:
    def run(self, operation_id: str, new_state: int):
        uploader.update_operation_state(operation_id, new_state)
        
class FlightDetail:
    def run(self, operation_id: str):
        uploader.get_flight_detail(operation_id)     
        
class SubmitGeoFence:
    def run(self):
        geo_sever.submit_geofence()
class GeoDetail:
    def run(self):
        geo_sever.get_geo_detail() 
        
class ApiInfo:
    def run(self):
        api.status()


class ServiceManager:
    def __init__(self):
        self.services = {}
        self.processes = {}

    def add_service(self, service_name, service):
        self.services[service_name] = service
    def start_service(self, service_name):
        if service_name in self.services:
            service = self.services[service_name]
           
            signature = inspect.signature(service.run)
            parameters = signature.parameters
            if len(parameters) > 0 and service_name=="UpdateOprState":
               
                operation_id = input("Enter operation ID: ").strip()
                new_state = int(input("Enter new state: ").strip())
                process = multiprocessing.Process(target=self._run_and_cleanup, args=(service, service_name, operation_id, new_state))
            elif len(parameters) > 0 and service_name=="FlightDetail":
                operation_id = input("Enter operation ID: ").strip()
                process = multiprocessing.Process(target=self._run_and_cleanup, args=(service, service_name, operation_id))
            else:
                
                process = multiprocessing.Process(target=self._run_and_cleanup, args=(service, service_name))
            self.processes[service_name] = process
            process.start()
            logger.info(f"Started {service_name}")
            process.join()  
            #self.stop_service(service_name)
        else:
            logger.error(f"Service {service_name} not found.")

    def _run_and_cleanup(self, service, service_name, *args):
        
        service.run(*args)
        
        
        logger.info(f"Service {service_name} finished.")
        self.processes.pop(service_name, None) 
        logger.info(f"Cleaned up process for {service_name}")

    def stop_service(self, service_name):
        if service_name in self.processes:
            process = self.processes[service_name]
            process.terminate()  
            process.join() 
            logger.info(f"Stopped {service_name}")
            self.processes.pop(service_name, None) 
        else:
            logger.error(f"Service {service_name} not running.")

    def stop_all_services(self):
        for service_name in list(self.processes.keys()):
            self.stop_service(service_name)

    def list_info(self):
        print("Operation States:")
        for state in OPERATION_STATES:
            console.print(f"{state[0]}: {state[1]}", style="bold green") 

    def list_services(self):
        if not self.services:
            logger.info("No services added.")
            return
        
        logger.info("Listing services:")
        for service_name in self.services:
            status = "running" if service_name in self.processes else "stopped"
            console.print(f"Service {service_name}: {status}", style="bold green")