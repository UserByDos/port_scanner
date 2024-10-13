import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from colorama import init, Fore, Style
import time

init(autoreset=True)

def get_ip_info(ip):
    try:
        response = requests.get(f"http://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None

def print_ip_info(info):
    if info:
        print(f"\n{Fore.MAGENTA}=== IP Information ===")
        print(f"{Fore.YELLOW}IP Address: {Fore.CYAN}{info.get('ip', 'N/A')}")
        print(f"{Fore.YELLOW}City: {Fore.CYAN}{info.get('city', 'N/A')}")
        print(f"{Fore.YELLOW}Region: {Fore.CYAN}{info.get('region', 'N/A')}")
        print(f"{Fore.YELLOW}Country: {Fore.CYAN}{info.get('country', 'N/A')}")
        print(f"{Fore.YELLOW}ISP: {Fore.CYAN}{info.get('org', 'N/A')}")
        print(f"{Fore.YELLOW}Location: {Fore.CYAN}{info.get('loc', 'N/A')}")
        print(f"{Fore.MAGENTA}=======================\n")

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.05)
        result = sock.connect_ex((target, port))
        sock.close()
        if result == 0:
            return port
    except Exception:
        return None

def scan_ports(target, port_range):
    open_ports = []
    print(f"{Fore.CYAN}Scanning {target} from port {port_range[0]} to {port_range[1]}...\n")

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=500) as executor:
        futures = [executor.submit(scan_port, target, port) for port in range(port_range[0], port_range[1] + 1)]
        for future in as_completed(futures):
            port = future.result()
            if port:
                print(f"{Fore.GREEN}Port {port} is open.")
                open_ports.append(port)

    end_time = time.time()
    total_time = end_time - start_time

    if open_ports:
        print(f"\n{Fore.YELLOW}Total Open Ports: {len(open_ports)}")
        print(f"{Fore.GREEN}Ports: {open_ports}")
    else:
        print(f"{Fore.RED}No open ports found.")

    print(f"\n{Fore.CYAN}Scan completed in {total_time:.2f} seconds.\n")

def display_title():
    print(f"{Fore.BLUE}{Style.BRIGHT}==============================================")
    print(f"{Fore.YELLOW}{Style.BRIGHT}           Advanced Python Port Scanner")
    print(f"{Fore.BLUE}{Style.BRIGHT}==============================================\n")

if __name__ == "__main__":
    display_title()
    target = input(f"{Fore.CYAN}Enter the IP address to scan (default: 127.0.0.1): ") or "127.0.0.1"
    port_range = (1, 1025)
    ip_info = get_ip_info(target)
    print_ip_info(ip_info)
    scan_ports(target, port_range)
