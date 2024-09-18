#!python3
import dropbox
from dotenv import load_dotenv
import os
import io

def list_files_in_directory(dbx, folder_path=''):
    """List files in a Dropbox directory."""
    try:
        result = dbx.files_list_folder(folder_path)
        if result.entries:
            print(f"Files in directory '{folder_path}':")
            for entry in result.entries:
                print(entry.name)
        else:
            print(f"No files found in directory '{folder_path}'.")
    except dropbox.exceptions.ApiError as e:
        print(f"API Error: {e}")

def main():
    # Load environment variables from .env file
    load_dotenv()
    DROPBOX_ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')
    
    # Verify the Dropbox client instantiation
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        print("Dropbox client created successfully")
    except AttributeError as e:
        print(f"Error: {e}")

    list_files_in_directory(dbx, 'my-test/')


if __name__ == "__main__":
    main()