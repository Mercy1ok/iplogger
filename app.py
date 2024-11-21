import os
import sys
import subprocess
import requests
import pyfiglet
from colorama import Fore, Back, Style, init
from time import sleep

# Initialize Colorama
init(autoreset=True)

# Check Dependencies
def install_dependencies():
    dependencies = ["requests", "colorama", "pyfiglet"]
    for package in dependencies:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_dependencies()

# Clear screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Fetch location details from IP
def get_location(ip):
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        response.raise_for_status()
        data = response.json()
        location_data = {
            "IP Address": ip,
            "City": data.get("city"),
            "Region": data.get("region"),
            "Country": data.get("country_name"),
            "IP Address Type": data.get("version"),
            "Region Code": data.get("region_code"),
            "Postal Code": data.get("postal"),
            "Latitude": data.get("latitude"),
            "Longitude": data.get("longitude"),
            "Timezone": data.get("timezone"),
            "Country Code": data.get("country_calling_code"),
            "Currency": data.get("currency"),
            "Currency Name": data.get("currency_name"),
            "Languages": data.get("languages"),
            "Country Area": data.get("country_area"),
            "Population": data.get("country_population"),
            "ASN": data.get("asn"),
            "Organization": data.get("org"),
        }
        return location_data
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching data: {e}")
        return None

# Display location data
def display_location(data):
    if not data:
        return
    for key, value in data.items():
        print(Fore.CYAN + f"{key}: {value}")
    if data["Latitude"] and data["Longitude"]:
        print(Fore.YELLOW + f"\nGoogle Maps: https://google.com/maps/place/{data['Latitude']},{data['Longitude']}/")

# Main Menu
def main_menu():
    clear_screen()
    title = pyfiglet.figlet_format("__ IP Tracker __")
    print(Fore.RED + title)
    print(Fore.GREEN + """
    [+] Author  : Hamooda
    [+] GitHub  : https://github.com/Mercy1ok
    """)
    print(Fore.WHITE + """
    ==============================================
    Commands:
      show      - Show all commands
      iptracker - Track an IP address
      help      - Show help menu
      exit      - Exit the program
    ==============================================
    """)

# Track IP Address
def track_ip():
    ip = input(Fore.YELLOW + "Enter IP Address: " + Style.RESET_ALL)
    print(Fore.WHITE + f"Fetching data for {ip}...")
    location_data = get_location(ip)
    if location_data:
        display_location(location_data)
        open_map = input(Fore.GREEN + "\nOpen location in Google Maps? [y/n]: ").lower()
        if open_map == "y":
            lat, lon = location_data.get("Latitude"), location_data.get("Longitude")
            if lat and lon:
                os.system(f"xdg-open https://google.com/maps/place/{lat},{lon}/@{lat},{lon},16z")
            else:
                print(Fore.RED + "Location coordinates not available.")
    else:
        print(Fore.RED + "Unable to fetch location data.")

# Command Menu
def handle_command():
    while True:
        command = input(Fore.RED + "IPTracker > " + Style.RESET_ALL).lower()
        if command == "help":
            print(Fore.CYAN + """
            Commands:
              show      - Show all commands
              iptracker - Track an IP address
              help      - Show help menu
              exit      - Exit the program
            """)
        elif command == "show":
            print(Fore.CYAN + """
            Available Commands:
              show      - Show all commands
              iptracker - Track an IP address
              help      - Show help menu
              exit      - Exit the program
            """)
        elif command == "iptracker":
            track_ip()
        elif command == "exit":
            print(Fore.GREEN + "Exiting IP Tracker. Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid Command! Type 'help' to see available commands.")

# Main Program
def main():
    main_menu()
    handle_command()

if __name__ == "__main__":
    main()
