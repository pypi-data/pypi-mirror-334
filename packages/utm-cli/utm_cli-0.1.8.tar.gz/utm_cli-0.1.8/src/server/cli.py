'''
Author: Tong hetongapp@gmail.com
Date: 2025-02-15 09:12:56
LastEditors: Tong hetongapp@gmail.com
LastEditTime: 2025-02-16 09:51:49
FilePath: /server/src/server/cli.py
Description:UTM CLI 
'''
import sys
import os
import typer
import pyfiglet
from rich.console import Console
from server import ServiceManager, AirTrafficSubmit, FlightDeclSubmit, ListDeclID, UpdateOprState, FlightDetail, SubmitGeoFence, GeoDetail, ApiInfo
import readline

def completer(text, state):
    options = ['start', 'run', 'stop', 'restart', 'status', 'exit', 'ServiceManager', 'ApiInfo', 'SubmitAirTraffic', 'AirTrafficSubmit', 'FlightDeclSubmit', 'ListDeclID', 'UpdateOprState', 'FlightDetail', 'SubmitGeoFence', 'GeoDetail', 'ApiInfo']  # 这里是补全选项
    matches = [option for option in options if option.startswith(text)]
    return matches[state] if state < len(matches) else None


def print_banner():
    banner = pyfiglet.figlet_format("UTM")
    console.print(banner,style="bold green")
    
readline.set_completer(completer)

readline.parse_and_bind('tab: complete')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "..")
sys.path.append(SRC_DIR)
history_file = os.path.expanduser("~/.python_history")

if os.path.exists(history_file):
    readline.read_history_file(history_file)
def save_history():
    readline.write_history_file(history_file)
import atexit
atexit.register(save_history)

app = typer.Typer()
console = Console()

service_manager = ServiceManager()

service_manager.add_service('SubmitAirTraffic', AirTrafficSubmit())
service_manager.add_service('FlightDeclSubmit', FlightDeclSubmit())
service_manager.add_service('ListDeclID', ListDeclID())
service_manager.add_service('UpdateOprState', UpdateOprState())
service_manager.add_service('FlightDetail', FlightDetail())
service_manager.add_service('SubmitGeoFence', SubmitGeoFence())
service_manager.add_service('GeoDetail', GeoDetail())
service_manager.add_service('ApiInfo', ApiInfo())


@app.command()
def main():
    """Console script for server."""
    print_banner()
    
    console.print("⚡ Welcome to the UTM services CLI ⚡", style="bold green")
    console.print("⚡ ---------Vesion 0.1.7---------- ⚡", style="bold green")
    while True:
        try:
            command = console.input("[bold yellow]⭐ UTM ==> ").strip()
            #command = input("⭐ service-manager ==> ").strip()
            if not command: 
                continue
            if command.startswith('run'):
                service_name = command.split(' ')[1]
                service_manager.start_service(service_name)
            elif command.startswith('stop'):
                service_name = command.split(' ')[1]
                service_manager.stop_service(service_name)
            elif command == 'stop_all':
                service_manager.stop_all_services()
            elif command == 'info':
                service_manager.list_info()
            elif command == 'list':
                service_manager.list_services() 
            elif command == 'exit':
                console.print("Exiting...")
                break
            else:
                console.print(f"Unknown command: {command}", style="bold red")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
        except IndexError:
            console.print("Please specify a service name after the command.", style="bold red")
        except Exception as e:
            console.print(f"Error: {e}", style="bold red")


if __name__ == "__main__":
    app()
