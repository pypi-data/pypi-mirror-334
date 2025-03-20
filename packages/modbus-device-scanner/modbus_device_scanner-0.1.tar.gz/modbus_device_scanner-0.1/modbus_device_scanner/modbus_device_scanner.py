#!/usr/bin/env python3
"""
Modbus Device Scanner
Scans a subnet for devices with open port 502 (Modbus TCP) and attempts to verify
if they're actually Modbus devices by sending a Modbus query.
"""

import socket
import concurrent.futures
import ipaddress
import struct
import argparse
import time
import sys
from datetime import datetime

# Default Modbus port
MODBUS_PORT = 502


def create_modbus_request(unit_id=1, function_code=1, address=0, count=1):
    """
    Create a basic Modbus TCP packet

    Args:
        unit_id: Slave ID (1 byte)
        function_code: Modbus function code (1 = Read Coils) (1 byte)
        address: Starting address (2 bytes)
        count: Number of registers to read (2 bytes)

    Returns:
        Bytes containing a complete Modbus TCP request
    """
    # Transaction ID (2 bytes)
    transaction_id = 1
    # Protocol ID (2 bytes) - always 0 for Modbus TCP
    protocol_id = 0
    # Length (2 bytes) - number of bytes following this field
    length = 6  # unit_id (1) + function_code (1) + address (2) + count (2)

    # Build the header
    header = struct.pack(">HHHB", transaction_id, protocol_id, length, unit_id)

    # Build the function data
    function_data = struct.pack(">BHH", function_code, address, count)

    # Complete packet
    packet = header + function_data

    return packet


def is_modbus_device(ip, port=MODBUS_PORT, timeout=1):
    """
    Check if a host has a Modbus TCP device by sending a minimal request and
    checking for a valid response.

    Args:
        ip: IP address to check
        port: TCP port to connect to (default: 502)
        timeout: Connection timeout in seconds

    Returns:
        Dictionary with device details if it's a Modbus device, None otherwise
    """
    try:
        # Create a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        # Connect to the potential Modbus device
        result = sock.connect_ex((ip, port))

        # If connection successful (port is open)
        if result == 0:
            # Create a basic Modbus request (Read Coils)
            request = create_modbus_request(unit_id=1, function_code=1, address=0, count=1)

            # Send the request
            sock.send(request)

            # Try to receive a response
            response = sock.recv(1024)

            # Close the socket
            sock.close()

            # Process the response
            # A valid Modbus TCP response should be at least 9 bytes long and
            # should begin with the same transaction ID
            if len(response) >= 9 and response[0:2] == request[0:2]:
                # Check if function code is valid (normal response or exception response)
                function_code_response = response[7]

                # Normal response or exception response
                if function_code_response == 1 or function_code_response == 0x81:
                    return {
                        "ip": ip,
                        "port": port,
                        "is_modbus": True,
                        "function_code_response": "Normal" if function_code_response == 1 else "Exception",
                        "exception_code": response[8] if function_code_response == 0x81 else None,
                        "full_response": response.hex()
                    }

            # If the response doesn't look like Modbus but the port is open
            return {
                "ip": ip,
                "port": port,
                "is_modbus": False,
                "status": "Port open but not Modbus or device rejected query",
                "full_response": response.hex() if response else None
            }

        # If the connection failed (port closed)
        else:
            sock.close()
            return None

    except socket.timeout:
        try:
            sock.close()
        except:
            pass
        return {
            "ip": ip,
            "port": port,
            "is_modbus": False,
            "status": "Port open but connection timed out waiting for response"
        }

    except Exception as e:
        try:
            sock.close()
        except:
            pass
        return None


def scan_ip_for_modbus(ip, port=MODBUS_PORT, timeout=1):
    """
    Wrapper function for threaded scanning
    """
    result = is_modbus_device(ip, port, timeout)
    return (ip, result)


def scan_subnet_for_modbus(subnet, port=MODBUS_PORT, timeout=1, max_workers=100):
    """
    Scan a subnet for Modbus devices

    Args:
        subnet: Subnet in CIDR notation (e.g., '192.168.1.0/24')
        port: TCP port to check for Modbus (default: 502)
        timeout: Connection timeout in seconds
        max_workers: Maximum number of concurrent threads

    Returns:
        List of dictionaries with detected Modbus devices
    """
    try:
        # Parse the subnet
        network = ipaddress.ip_network(subnet)

        # Get all IP addresses in the subnet
        ip_list = [str(ip) for ip in network.hosts()]

        print(
            f"[*] Starting Modbus scan of {subnet} ({len(ip_list)} hosts) at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Results container
        modbus_devices = []
        open_ports = []

        # For large subnets, use progress indicators
        total_ips = len(ip_list)
        progress_step = max(1, total_ips // 20)  # Show progress at 5% intervals

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_ip = {executor.submit(scan_ip_for_modbus, ip, port, timeout): ip for ip in ip_list}

            # Process results as they complete
            completed = 0
            for future in concurrent.futures.as_completed(future_to_ip):
                ip = future_to_ip[future]
                completed += 1

                # Show progress for large scans
                if total_ips > 20 and completed % progress_step == 0:
                    progress = (completed / total_ips) * 100
                    print(f"[*] Scan progress: {progress:.1f}% ({completed}/{total_ips})")

                try:
                    ip, result = future.result()
                    if result:
                        if result.get("is_modbus", False):
                            print(f"[+] Modbus device found: {ip}:{port}")
                            modbus_devices.append(result)
                        else:
                            print(f"[*] Open port but not Modbus: {ip}:{port}")
                            open_ports.append(result)
                except Exception as e:
                    print(f"[!] Error processing result for {ip}: {e}")

        return modbus_devices, open_ports

    except Exception as e:
        print(f"[!] Error scanning subnet: {e}")
        return [], []


def main():
    parser = argparse.ArgumentParser(description='Scan for Modbus TCP devices on a network')
    parser.add_argument('--subnet', '-s', default='192.168.1.0/24',
                        help='Network subnet in CIDR notation (e.g., 192.168.1.0/24)')
    parser.add_argument('--port', '-p', type=int, default=MODBUS_PORT,
                        help=f'TCP port to scan (default: {MODBUS_PORT})')
    parser.add_argument('--timeout', '-t', type=float, default=1.0,
                        help='Connection timeout in seconds (default: 1.0)')
    parser.add_argument('--workers', '-w', type=int, default=100,
                        help='Maximum number of concurrent workers (default: 100)')
    parser.add_argument('--verify', '-v', action='store_true',
                        help='Perform more thorough verification (slower)')

    args = parser.parse_args()

    try:
        # Validate subnet format
        try:
            ipaddress.ip_network(args.subnet)
        except ValueError:
            print(f"[!] Invalid subnet format: {args.subnet}")
            print("[!] Please use CIDR notation (e.g., 192.168.1.0/24)")
            sys.exit(1)

        start_time = time.time()
        modbus_devices, open_ports = scan_subnet_for_modbus(
            args.subnet, args.port, args.timeout, args.workers
        )
        end_time = time.time()

        # Display results
        print("\n" + "=" * 70)
        print(f"MODBUS SCAN RESULTS - Subnet: {args.subnet}")
        print("=" * 70)

        if modbus_devices:
            print(f"\nFound {len(modbus_devices)} Modbus devices:")
            for device in modbus_devices:
                print(f"\n[+] Modbus Device: {device['ip']}:{device['port']}")
                print(f"    Response Type: {device.get('function_code_response', 'Unknown')}")
                if device.get('exception_code') is not None:
                    print(f"    Exception Code: {device['exception_code']}")
        else:
            print("\nNo Modbus devices found.")

        if open_ports:
            print(f"\nFound {len(open_ports)} hosts with port {args.port} open but not confirmed as Modbus:")
            for entry in open_ports:
                print(f"    {entry['ip']}:{entry['port']} - {entry.get('status', 'Unknown status')}")

        print("\n" + "=" * 70)
        print(f"Scan completed in {end_time - start_time:.2f} seconds")
        print("=" * 70 + "\n")

    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()