#!/usr/bin/env python
import os
import sys
import subprocess
import socket
from dotenv import load_dotenv

# Load environment variables from daphne.env
load_dotenv('daphne.env')

# Get configuration from environment
host = os.getenv('DAPHNE_HOST', '0.0.0.0')
port = int(os.getenv('DAPHNE_PORT', 8000))
cert_file = os.getenv('CERT_FILE')
key_file = os.getenv('KEY_FILE')
asgi_app = os.getenv('ASGI_APPLICATION')


# Check if the port is already in use
def is_port_in_use(port, host='localhost'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return False
        except socket.error:
            return True


# Find an available port if specified one is in use
if is_port_in_use(port, host):
    print(f"Port {port} is already in use. Please free it up or specify a different port in daphne.env")
    print("You can find what's using the port with: netstat -ano | findstr :8000")
    sys.exit(1)

# Build the command - use only the SSL endpoint, not both SSL and TCP
cmd = [
    "daphne",
    "-e", f"ssl:{port}:privateKey={key_file}:certKey={cert_file}",
    asgi_app
]

print(f"Starting Daphne with HTTPS on {host}:{port}")
try:
    subprocess.run(cmd)
except KeyboardInterrupt:
    print("\nDaphne server stopped.")
except Exception as e:
    print(f"Error running Daphne: {e}")
    sys.exit(1)
