import os
import sys
import webbrowser
import time
import threading

def open_browser():
    """Open the default web browser to the Django server URL."""
    time.sleep(1)  # Give the server a moment to start
    webbrowser.open("http://127.0.0.1:8000/")


def main():
    """Main entry point for the CLI."""
    # Add the current directory to the Python path
    sys.path.insert(0, os.getcwd())

    # Start the Django server
    print("Starting Odoo Health Report server...")

    # Start the browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    # Run the Django server
    try:
        # Use the manage.py from this package
        from odoo_health import manage
        manage.main()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        sys.exit(0)


if __name__ == "__main__":
    main()