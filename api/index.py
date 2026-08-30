import sys
import os

# Include backend directory in sys.path
backend_dir = os.path.join(os.path.dirname(__file__), '..', 'library-backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app import create_app

app = create_app()
