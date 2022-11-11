import sys
from pathlib import Path

# Fixes absolute path import resolution in dev server.
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR.parent))
sys.path.append(str(BASE_DIR.parent.parent))