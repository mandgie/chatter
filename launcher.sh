#!/usr/bin/env bash

# Get the directory of the script or follow symlinks if it is a symlink
FILE_SOURCE="${BASH_SOURCE[0]}"
while [ -h "$FILE_SOURCE" ]; do
  SCRIPT_DIR="$(cd -P "$(dirname "$FILE_SOURCE")" && pwd)"
  FILE_SOURCE="$(readlink "$FILE_SOURCE")"
  [[ $FILE_SOURCE != /* ]] && FILE_SOURCE="$SCRIPT_DIR/$FILE_SOURCE"
done
SCRIPT_DIR="$(cd -P "$(dirname "$FILE_SOURCE")" && pwd)"

# Read the Python interpreter path from config.ini
PYTHON_PATH=$(awk -F' = ' '/executable/ {print $2}' "$SCRIPT_DIR/config.ini")

# Execute the Python script with the specified interpreter
$PYTHON_PATH "$SCRIPT_DIR/chatter.py" "${@}"