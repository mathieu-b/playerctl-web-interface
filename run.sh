#!/usr/bin/env bash
set -e


echo "Checking that uv is installed..."
if ! command -v uv &> /dev/null
then
    echo "
ERROR: uv could not be found
Please install uv following the instructions at: https://docs.astral.sh/uv/getting-started/installation/
and try again.
" >&2
    exit 1
else
    echo "uv is installed ✔"
fi


echo "Checking that playerctl is installed..."
if ! command -v playerctl &> /dev/null
then
    echo "
ERROR: playerctl could not be found
Please install playerctl and try again
On Debian / Ubuntu:
  sudo apt install guix
  guix install playerctl

" >&2
    exit 1
else
    echo "playerctl is installed ✔"
fi


echo "Running the app with uv ..."
uv run src/app.py
