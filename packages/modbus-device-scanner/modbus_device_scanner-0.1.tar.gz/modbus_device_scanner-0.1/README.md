# Modbus Scanner

A package to scan for Modbus TCP devices on a network.

## Installation

```bash
pip install .
```

# Usage

```bash
modbus_device_scanner --subnet 192.168.1.0/24
modbus_device_scanner --port 503
modbus_device_scanner --timeout 2.0
modbus_device_scanner --workers 50