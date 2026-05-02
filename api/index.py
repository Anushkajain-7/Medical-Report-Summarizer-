import os
import sys

# Add the project root to the path so we can import from the backend directory
# This ensures that 'from backend.app import app' works regardless of where the script is run
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Import the FastAPI app from backend/app.py
# We use the full path to avoid ambiguity and fix linting warnings
from backend.app import app
