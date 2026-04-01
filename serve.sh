#!/usr/bin/env bash
PORT="${1:-8080}"
echo "Serving Random of Exile at http://localhost:$PORT"
python3 -m http.server "$PORT"
