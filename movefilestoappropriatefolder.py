from pathlib import Path
import shutil
import glob
import os


def movefiletofolder(destination_folder_path, source_file_path):
    # 2. Ensure the destination folder exists, creating it if necessary
    # parents=True allows creation of intermediate directories if they don't exist
    # exist_ok=True prevents an error if the directory is already there
    destination_folder_path.mkdir(parents=True, exist_ok=True)

    # 3. Construct the full destination path for the file
    # This joins the destination folder path object with the file name from the source path object
    destination_file_path = destination_folder_path / source_file_path.name

    # 4. Move the file
    try:
        # shutil.move can accept Path objects directly in modern Python/shutil versions
        shutil.move(str(source_file_path), str(destination_file_path))
        print(f"Successfully moved '{source_file_path.name}' to '{destination_folder_path}'")

    except FileNotFoundError:
        print(f"Error: The source file '{source_file_path}' or the destination directory '{destination_folder_path}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied. Check file permissions.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Define the directory path you want to search
directory_path = 'C:/Users/lkhum\OneDrive/Documents/Spotify Analysis Repos/top200globalchart/updated-spotify-top200globalchart-analysis/'
destination_folder_path = 'C:/Users/lkhum/OneDrive/Documents/Spotify Analysis Repos/top200globalchart/updated-spotify-top200globalchart-analysis/spotify-top200globalchart-analysis/spotify '
splitpathstr = 'C:/Users/lkhum\\OneDrive/Documents/Spotify Analysis Repos/top200globalchart/updated-spotify-top200globalchart-analysis\\'

therelfilestrs = ["kr", "za", "global", "gb", "ng", "au", "in", "us"]

# Create a search pattern for all files ending with .csv in that specific directory
# The asterisk (*) acts as a wildcard for the filename itself
search_pattern = os.path.join(directory_path, '*.csv')

# Use glob.glob() to get the list of matching files
csv_files_paths = glob.glob(search_pattern)

print(f"Found {len(csv_files_paths)} CSV files:")
allfiles = []
for file_path in csv_files_paths:
    allfiles.append(file_path)

for filename in allfiles:
    for innerfiles in filename.split(splitpathstr):
        if(innerfiles != ""):
            destpath = destination_folder_path + innerfiles.split('regional-')[1].split("-")[0] + " " + 'v2/'
            movefiletofolder(Path(destpath), Path(filename))

