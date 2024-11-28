#!/bin/bash

METADATA_FILE="metadata_sql.json"
FOLDER_SQL="sql/"

# Fungsi untuk memastikan file metadata.json ada
initialize_metadata_file() {
  if [ ! -f "$METADATA_FILE" ]; then
    echo "{}" > "$METADATA_FILE"  # Inisialisasi metadata kosong
  fi
}

# Fungsi untuk mendapatkan file baru dari git diff
get_new_files() {
  git diff --cached --name-status $FOLDER_SQL | awk '$1 == "A" {print $2}'
}

# Fungsi untuk mendapatkan create date (Unix timestamp) file
get_create_date() {
  local file="$1"
  stat --format='%W' "$file"
}

# Fungsi utama untuk memperbarui metadata
update_metadata() {
  initialize_metadata_file

  # Membaca metadata yang ada
  local temp_metadata=$(mktemp)
  cp "$METADATA_FILE" "$temp_metadata"

  # Loop file baru dari git diff
  for file in $(get_new_files); do
    if ! jq -e --arg file "$file" '.[$file]' "$temp_metadata" &>/dev/null; then
      # Mendapatkan tanggal pembuatan
      create_date=$(get_create_date "$file")
      if [ "$create_date" -eq 0 ]; then
        # Jika create_date tidak valid, gunakan tanggal sekarang
        create_date=$(date +%s)
      fi

      # Tambahkan metadata file ke file sementara
      jq --arg file "$file" --arg date "$(date -d "@$create_date" +'%Y-%m-%d %H:%M:%S')" \
         '.[$file] = $date' "$temp_metadata" > "$temp_metadata.new" && mv "$temp_metadata.new" "$temp_metadata"
    fi
  done

  # Menyimpan kembali metadata yang diperbarui
  mv "$temp_metadata" "$METADATA_FILE"
  echo "Metadata updated in $METADATA_FILE"
}

# Eksekusi fungsi
update_metadata
