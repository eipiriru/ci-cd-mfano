import subprocess
import json
from datetime import datetime
import os

METADATA_FILE = "metadata_sql.json"
FOLDER_SQL = "sql/"

# Fungsi untuk membaca metadata yang sudah ada
def load_metadata():
    try:
        with open(METADATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Fungsi untuk menyimpan metadata ke file
def save_metadata(metadata):
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=4)

# Fungsi untuk mendapatkan file baru dari git diff
def get_new_files():
    result = subprocess.check_output(["git", "diff", "--cached", "--name-status", FOLDER_SQL]).decode("utf-8")
    new_files = [
        line.split("\t")[1]
        for line in result.strip().split("\n")
        if line.startswith("A")  # "A" berarti file baru ditambahkan
    ]
    return new_files

# Fungsi untuk mendapatkan create date file
def get_create_date(file_path):
    # create_time = os.stat(file_path).st_ctime
    # return datetime.fromtimestamp(create_time).strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Menjalankan perintah stat untuk mendapatkan waktu pembuatan file
        stat_output = subprocess.check_output(['stat', '--format=%W', file_path]).decode().strip()
        
        # Jika stat_output adalah '0', berarti tidak ada informasi 'create date'
        if stat_output == '0':
            # return None  # Tidak ada create date
            create_time = os.stat(file_path).st_ctime
            return datetime.fromtimestamp(create_time).strftime("%Y-%m-%d %H:%M:%S")
        
        # Mengonversi epoch timestamp menjadi datetime
        create_time = datetime.fromtimestamp(int(stat_output))
        return create_time.strftime("%Y-%m-%d %H:%M:%S")
    
    except subprocess.CalledProcessError:
        print(f"Error: unable to get file information for {file_path}")
        return None

# Fungsi utama untuk mencatat metadata
def update_metadata():
    metadata = load_metadata()
    new_files = get_new_files()

    for file in new_files:
        if file not in metadata:
            try:
                metadata[file] = get_create_date(file)
            except FileNotFoundError:
                print(f"File not found: {file}")

    save_metadata(metadata)
    print(f"Metadata diperbarui untuk {len(new_files)} file baru.")

if __name__ == "__main__":
    update_metadata()
