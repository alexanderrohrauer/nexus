#!/bin/sh
sleep 10 && uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level debug
