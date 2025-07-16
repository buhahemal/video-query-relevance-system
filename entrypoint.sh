#!/bin/bash
set -e

if [ "$1" = "process" ]; then
    exec python app/process_videos.py
else
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
fi 