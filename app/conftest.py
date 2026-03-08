import sys
import os

app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)

for root, dirs, files in os.walk(app_dir):
    # Exclude hidden directories and __pycache__
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
    sys.path.insert(0, root)
