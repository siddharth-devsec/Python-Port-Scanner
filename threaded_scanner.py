import socket
import sys
import argparse
from datetime import datetime
import concurrent.futures
from threading import Lock
# Thread-safe printing
print_lock = Lock()
# Store open ports
open_ports = []
# Argument parser
parser = argparse.ArgumentParser(
    description="Professional Python Port Scanner"
)
parser.add_argument(
    "-t",
    "--target",
    help="Target IP address or hostname",
    required=True
)
parser.add_argument(
    "-w",
    "--workers",
    help="Number of threads (default: 100)",
    type=int,
    default=100
)
parser.add_argument(
    "-o",
    "--output",
    help="Output file name",
    default="open_ports.txt"
)
args = parser.parse_args()
target = args.target
threads = args.workers
output_file = args.output
# Resolve hostname
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("[!] Unable to resolve hostname.")
    sys.exit()
print("-" * 60)
print(f"Target        : {target}")
print(f"Resolved IP   : {target_ip}")
print(f"Threads       : {threads}")
print(f"Scan Started  : {datetime.now()}")
print("-" * 60)
def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Socket timeout
        s.settimeout(1)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            # Service detection
            try:
                service = socket.getservbyport(port, "tcp")
            except:
                service = "Unknown"
            # Banner grabbing
            banner = ""
            try:
                s.send(b"HELLO\r\n")
                banner = s.recv(1024).decode().strip()
                if not banner:
                    banner = "No Banner"
            except:
                banner = "No Banner"
            # Thread-safe output
            with print_lock:
                print(f"[+] Port {port:<5} OPEN  | Service: {service}")
                if banner != "No Banner":
                    print(f"    Banner: {banner}")
            # Save results
            open_ports.append({
                "port": port,
                "service": service,
                "banner": banner
            })
        s.close()
    except:
        pass
try:
    # Multithreaded scanning
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=threads
    ) as executor:
        executor.map(scan_port, range(1, 1025))
except KeyboardInterrupt:
    print("\n[!] Scan interrupted by user.")
    sys.exit()
# Sort ports
open_ports.sort(key=lambda x: x["port"])
print("-" * 60)
print(f"Scan Finished : {datetime.now()}")
print("-" * 60)
# Save results
if open_ports:
    print(f"\n[+] Saving results to {output_file}")
    with open(output_file, "w") as file:
        file.write(f"Port Scan Results for {target}\n")
        file.write(f"Resolved IP: {target_ip}\n")
        file.write("-" * 60 + "\n")
        for item in open_ports:
            file.write(
                f"Port {item['port']} | "
                f"Service: {item['service']} | "
                f"Banner: {item['banner']}\n"
            )
    print("[✓] Results saved successfully!")
else:
    print("[!] No open ports found.")
