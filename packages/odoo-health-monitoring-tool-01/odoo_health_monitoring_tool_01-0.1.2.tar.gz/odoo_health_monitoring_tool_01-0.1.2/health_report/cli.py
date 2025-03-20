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
    # Find the directory where THIS script (cli.py) is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Assuming cli.py is inside odoo_report/, move up to the project root
    root_dir = os.path.abspath(script_dir)  # Adjust if cli.py is outside

    # Add project root to sys.path so Python can find manage.py
    sys.path.insert(0, root_dir)

    # Start the Django server
    print("Starting Odoo Health Report server...")

    # Start the browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    # Run the Django server
    try:
        import manage  # Import manage.py
        manage.main()  # Call Django's main function
    except KeyboardInterrupt:
        print("\nShutting down server...")
        sys.exit(0)
    except ModuleNotFoundError as e:
        print(f"Error: {e}")
        print("Ensure you are running this script from the correct directory.")
        print("Try running: python cli.py from the root directory.")
        sys.exit(1)

if __name__ == "__main__":
    main()
