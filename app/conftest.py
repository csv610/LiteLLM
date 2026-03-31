import sys
import os

# Add the app directory to sys.path to allow absolute imports
app_dir = os.path.dirname(os.path.abspath(__file__))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)
