import subprocess
import json
from datetime import datetime

METADATA_FILE = "metadata_sql.json"

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
    result = subprocess.check_output(["git", "diff", "--cached", "--name-status"]).decode("utf-8")
    new_files = [
        line.split("\t")[1]
        for line in result.strip().split("\n")
        if line.startswith("A")  # "A" berarti file baru ditambahkan
    ]
    return new_files

# Fungsi utama untuk mencatat metadata
def update_metadata():
    metadata = load_metadata()
    new_files = get_new_files()

    for file in new_files:
        if file not in metadata:
            metadata[file] = {
                "create_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

    save_metadata(metadata)
    print(f"Metadata diperbarui untuk {len(new_files)} file baru.")

if __name__ == "__main__":
    update_metadata()
