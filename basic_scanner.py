import socket
import sys
from datetime import datetime
# Target IP / Hostname
target = input("Enter Target IP or Hostname: ")
# Hostname ko IP mein convert karna
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("[!] Hostname resolve nahi hua.")
    sys.exit()
print("-" * 50)
print(f"Scanning Target : {target}")
print(f"Resolved IP     : {target_ip}")
print(f"Scan Started    : {datetime.now()}")
print("-" * 50)
try:
    # 1 se 1024 ports scan karna
    for port in range(1, 1025):
        # Socket create
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Timeout
        s.settimeout(0.5)
        # Connection test
        result = s.connect_ex((target_ip, port))
        # Open port
        if result == 0:
            try:
                service = socket.getservbyport(port, "tcp")
            except:
                service = "Unknown"
            print(f"[+] Port {port:<5} OPEN | Service: {service}")
        # Socket close
        s.close()
except KeyboardInterrupt:
    print("\n[!] Scanner stopped by user.")
    sys.exit()
except Exception as e:
    print(f"[!] Error: {e}")
print("-" * 50)
print(f"Scan Finished : {datetime.now()}")
print("-" * 50)
