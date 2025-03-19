import os
import sys
import subprocess

BIN_DIR = os.path.join(os.path.dirname(__file__), "../bin")

def get_executable(name):
    """Returns the correct executable name based on the OS."""
    if sys.platform == "win32":
        return os.path.join(BIN_DIR, f"{name}.exe")
    return os.path.join(BIN_DIR, name)

def main():
    """Runs the correct godrive or godrive_upload binary based on user input."""
    if len(sys.argv) < 2:
        print("Usage: godrive [args] or godrive_upload [args]")
        sys.exit(1)

    cmd_name = sys.argv[0]  # The command user typed
    exec_name = "godrive" if "godrive" in cmd_name else "godrive_upload"
    executable = get_executable(exec_name)

    if not os.path.exists(executable):
        print(f"Error: {executable} not found! Make sure it is installed correctly.")
        sys.exit(1)

    subprocess.run([executable] + sys.argv[1:])

if __name__ == "__main__":
    main()
