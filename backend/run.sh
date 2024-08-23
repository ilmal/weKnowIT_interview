export CACHE_SAVE_DIR="./cache"
export GENERATED_STORIES_SAVE_DIR="./chatgpt-stories"
export FLASK_APP=main.py

PYTHONWARNINGS="ignore" flask  run --host 0.0.0.0
