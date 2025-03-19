import sys
import os
import io
import zipfile
import shutil
import signal
from tqdm import tqdm
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

VERSION = "1.0.3"

TOOL_INFO = """
Godrive CLI Tool
----------------
A command-line tool to easily upload files and directories to Google Drive.

Features:
- First-time user setup for Google authentication
- Supports file and directory uploads
- Resumes authentication if previously authenticated

Developed by Rohan Yadav
LinkedIn -> https://www.linkedin.com/in/rohanbhatotiya
GitHub -> https://github.com/rohanbhatotiya
Email -> rohanbhatotiya@gmail.com
"""

godrive_dir = os.path.expanduser("~/.godrive")
os.makedirs(godrive_dir, exist_ok=True)

client_secrets_path = os.path.join(godrive_dir, "client_secrets.json")
auth_file_path = os.path.join(godrive_dir, "auth.txt")


def prompt_user(prompt):
    return input(prompt)


def verify_client_secrets(content):
    return len(content) > 0 and len(content) < 5000 and content[0] == "{" and content[-1] == "}"

def get_client_secrets():
    attempts = 0
    while attempts < 3:
        client_secrets = prompt_user("\nPaste your client_secrets.json content:\n")
        print("Verifying...")
        if verify_client_secrets(client_secrets):
            try:
                with open(client_secrets_path, "w") as f:
                    f.write(client_secrets)
                print("✅ Successfully verified and saved.")
                return
            except Exception as e:
                print(f" Error saving client_secrets.json: {e}")
                return
        else:
            print(" Invalid client_secrets.json format. Please try again.")
            attempts += 1

    print("Too many failed attempts. Exiting...")
    sys.exit(1)


def verify_file_path(file_path):
    try:
        abs_path = os.path.abspath(file_path)
        if not os.path.exists(abs_path):
            print(" File/Directory does not exist.")
            return False
        return True
    except Exception as e:
        print(f" Error resolving absolute path: {e}")
        return False


def print_version():
    print("Godrive CLI Version:", VERSION)


def print_info():
    print(TOOL_INFO)


def signal_handler(sig, frame):
    print("\n Exiting gracefully... Goodbye!")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def authenticate():
    """Handles Google authentication, prompting the user if needed."""
    if not os.path.exists(client_secrets_path):
        print("\n⚠️  Missing or invalid client_secrets.json. You need to provide a new one.")
        get_client_secrets()

    gauth = GoogleAuth()
    gauth.LoadClientConfigFile(client_secrets_path)

    if os.path.exists(auth_file_path):
        gauth.LoadCredentialsFile(auth_file_path)
        if gauth.credentials and not gauth.access_token_expired:
            print("✅ Using existing authentication.")
            return GoogleDrive(gauth)

    print(" Re-authenticating...")
    gauth.CommandLineAuth()
    gauth.SaveCredentialsFile(auth_file_path)
    print(" Authentication successful.")
    return GoogleDrive(gauth)


def zip_directory(directory_path):
    """Creates a zip file for a directory before uploading."""
    parent_dir = os.path.dirname(directory_path)
    dir_name = os.path.basename(directory_path)
    zip_name = os.path.join(parent_dir, f"{dir_name}(by_godrive).zip")

    if os.path.exists(zip_name):
        print(f" Using existing zip: {zip_name}")
        return zip_name

    print(" Creating a zip file...")
    try:
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, directory_path))
        print(f" Zip created: {zip_name}")
    except Exception as e:
        if "No space left" in str(e):
            print(" No space left to create a zip. Try uploading files individually.")
            sys.exit(1)
        else:
            print(f"Error while zipping: {e}")
            sys.exit(1)

    return zip_name


def upload_file(drive, file_path, custom_name):
    """Uploads a file or directory (as zip) to Google Drive."""
    if not os.path.exists(file_path):
        print(" Error: File does not exist!")
        return False

    is_zipped = False

    if os.path.isdir(file_path):
        file_path = zip_directory(file_path)
        is_zipped = True

    original_name, original_extension = os.path.splitext(os.path.basename(file_path))

    if custom_name:
        upload_name = f"{custom_name}{original_extension}"
    else:
        upload_name = f"{original_name}{original_extension}"

    file_drive = drive.CreateFile({"title": upload_name})

    print("\n Uploading file...")
    try:
        with open(file_path, "rb") as f:
            file_drive.content = io.BytesIO(f.read())
            file_drive.Upload()

        print("\nUpload Complete!")
        print(f" File uploaded with name: {upload_name}")

        if is_zipped:
            os.remove(file_path)

    except Exception as e:
        print(f" Upload failed: {e}")
        return False

    return True


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "version":
            print_version()
            return
        elif sys.argv[1] == "info":
            print_info()
            return

    print("Welcome to Godrive CLI!")

    if not os.path.exists(client_secrets_path) or not verify_client_secrets(open(client_secrets_path).read()):
        print("\n⚠️  Missing or invalid client_secrets.json. You need to provide a new one.")
        get_client_secrets()
    else:
        choice = prompt_user("\n✅ Valid client_secrets.json found. Do you want to change it? (y/n): ")
        if choice.lower() == "y":
            get_client_secrets()
        else:
            print("✅ Using existing client_secrets.json.")

    files_input = prompt_user("\n Enter the path(s) of the file(s)/directory to upload (separate multiple with '$'):\n").strip()
    file_paths = files_input.split("$")

    base_dir = os.path.dirname(file_paths[0]) if len(file_paths) > 1 else None
    same_directory = all(os.path.dirname(f) == base_dir or os.path.basename(f) == f for f in file_paths)

    resolved_paths = []
    for f in file_paths:
        full_path = os.path.join(base_dir, f) if same_directory and not os.path.isabs(f) else f
        if not os.path.exists(full_path):
            print(f"❌ Error: File not found -> {full_path}")
            sys.exit(1)
        resolved_paths.append(full_path)

    if os.path.exists(auth_file_path):
        prev_user = prompt_user("\n Previous upload was done on a saved account. Do you want to use the same account? (y/n): ").strip().lower()
        if prev_user == "n":
            os.remove(auth_file_path)
            print(" Old authentication removed. You will need to authenticate again.")

    drive = authenticate()

    for path in resolved_paths:
        upload_file(drive, path, None)

    print("\n✅ All files uploaded successfully!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Operation cancelled by user. Exiting safely...")
        sys.exit(1)
