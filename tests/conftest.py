import sys
import os
from pathlib import Path

# Add app subdirectories to sys.path to support their internal absolute imports
project_root = Path(__file__).parent.parent
app_dirs = [
    project_root / "app" / "ArticleReviewer",
    project_root / "app" / "FAQGenerator",
    project_root / "app" / "ObjectGuesser",
    project_root / "app" / "MedKit" / "drug" / "medicine" / "drugbank",
]

for d in app_dirs:
    if str(d) not in sys.path:
        sys.path.insert(0, str(d))
