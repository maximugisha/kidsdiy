#!/usr/bin/env python
import os
import sys
import time
import subprocess
import socket
import threading
from pathlib import Path
from dotenv import load_dotenv

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Watchdog not found, installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "watchdog"])
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

# Load environment variables from daphne.env
load_dotenv('daphne.env')

# Get configuration from environment
host = os.getenv('DAPHNE_HOST', '0.0.0.0')
port = int(os.getenv('DAPHNE_PORT', 8000))
cert_file = os.getenv('CERT_FILE')
key_file = os.getenv('KEY_FILE')
asgi_app = os.getenv('ASGI_APPLICATION')
project_path = os.getenv('PROJECT_PATH', os.path.abspath(os.path.dirname(__file__)))

# Check if the port is already in use
def is_port_in_use(port, host='localhost'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return False
        except socket.error:
            return True

# Daphne process reference
daphne_process = None

# Function to start Daphne
def start_daphne():
    global daphne_process

    # Build the command - use only the SSL endpoint
    cmd = [
        "daphne",
        "-e", f"ssl:{port}:privateKey={key_file}:certKey={cert_file}",
        asgi_app
    ]

    print(f"\n[{time.strftime('%H:%M:%S')}] Starting Daphne with HTTPS on {host}:{port}")

    # Kill any existing process
    if daphne_process and daphne_process.poll() is None:
        print(f"[{time.strftime('%H:%M:%S')}] Stopping previous Daphne instance...")
        daphne_process.terminate()
        try:
            daphne_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            daphne_process.kill()

    # Start a new process
    daphne_process = subprocess.Popen(cmd)

# File change handler
class ChangeHandler(FileSystemEventHandler):
    def __init__(self, restart_delay=2):
        self.restart_delay = restart_delay
        self.last_modified = time.time()
        self.is_restarting = False

    def on_any_event(self, event):
        # Ignore directory events and .git changes
        if event.is_directory or '.git' in event.src_path:
            return

        # Ignore certain file types
        ignored_extensions = ['.pyc', '.pyo', '.pyd', '.git', '.swp', '.swo']
        if any(event.src_path.endswith(ext) for ext in ignored_extensions):
            return

        # Debounce rapid changes
        current_time = time.time()
        if current_time - self.last_modified < self.restart_delay:
            return
        self.last_modified = current_time

        if not self.is_restarting:
            self.is_restarting = True
            print(f"\n[{time.strftime('%H:%M:%S')}] Changes detected in {event.src_path}")
            print(f"[{time.strftime('%H:%M:%S')}] Restarting Daphne in {self.restart_delay}s...")

            # Use a timer to avoid restarting too frequently
            timer = threading.Timer(self.restart_delay, self.restart_server)
            timer.daemon = True
            timer.start()

    def restart_server(self):
        try:
            start_daphne()
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Error restarting Daphne: {e}")
        finally:
            self.is_restarting = False

def main():
    # Check if port is available
    if is_port_in_use(port, host):
        print(f"Port {port} is already in use. Please free it up or specify a different port in daphne.env")
        print("You can find what's using the port with: netstat -ano | findstr :{port}")
        sys.exit(1)

    # Start Daphne initially
    start_daphne()

    # Set up file watching
    path = Path(project_path)
    print(f"[{time.strftime('%H:%M:%S')}] Watching for changes in {path}...")

    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n[{time.strftime('%H:%M:%S')}] Shutting down...")
        if daphne_process:
            daphne_process.terminate()
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()