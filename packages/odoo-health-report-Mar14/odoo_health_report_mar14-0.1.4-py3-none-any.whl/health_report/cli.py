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
    # Ensure the root directory (where manage.py is) is in the Python path
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
    root_dir = os.path.abspath(os.path.join(script_dir, ".."))  # Move up to odoo_report

    sys.path.insert(0, root_dir)  # Add odoo_report/ to sys.path

    # Start the Django server
    print("Starting Odoo Health Report server...")

    # Start the browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    # Run the Django server
    try:
        # Import manage.py from the correct location
        import manage
        manage.main()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        sys.exit(0)
    except ModuleNotFoundError as e:
        print(f"Error: {e}")
        print("Ensure you are running this script from the correct environment.")
        sys.exit(1)

if __name__ == "__main__":
    main()
