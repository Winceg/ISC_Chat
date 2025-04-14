import sys  # Import system-specific parameters and functions
import os  # Import OS module for interacting with the operating system
import subprocess  # Import subprocess module for spawning new processes
import threading  # Import threading module for concurrent execution
import time  # Import time module for time-related functions
from PySide6.QtWidgets import QApplication  # Import QApplication class from PySide6
from chat import ChatClient  # Import ChatClient class from src.chat module


def start_logic():
    """Start the chat server in a separate process"""
    print("Starting logic...")  # Print message indicating server start
    server_path = os.path.join(os.path.dirname(__file__), 'src/server.py')  # Get the path to the server script
    subprocess.Popen([sys.executable, server_path])  # Start the server script in a new process
    time.sleep(1)  # Wait for 1 second to ensure the server starts


def start_client(host, port):
    """Start the chat client GUI"""
    print("Starting client...")  # Print message indicating client start
    app = QApplication(sys.argv)  # Create a new QApplication instance
    client = ChatClient(host, port)  # Create an instance of ChatClient
    client.show()  # Show the client window
    sys.exit(app.exec())  # Start the application event loop