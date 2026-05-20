import socket
target_ip = input("Enter Target IP: ")
open_ports = []
def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            # Basic service guess
            try:
                service_name = socket.getservbyport(port, "tcp")
            except:
                service_name = "Unknown"
            # Banner grabbing
            banner = ""
            try:
                s.settimeout(2)
                raw_banner = s.recv(1024)
                if raw_banner:
                    banner = raw_banner.decode('utf-8').strip()
            except:
                banner = "No Banner / Requires GET Request"
            print(f"[+] Port {port} is OPEN (Guess: {service_name})")
            if banner:
                print(f"    └─ Actual Banner: {banner}")
            open_ports.append(
                f"Port {port} ({service_name}) - Banner: {banner}"
            )
        s.close()
    except Exception:
        pass
# Scan common ports
for port in range(20, 100):
    scan_port(port)
print("\nOpen Ports Found:")
for p in open_ports:
    print(p)
