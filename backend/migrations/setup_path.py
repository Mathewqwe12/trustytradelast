import sys
from pathlib import Path

# Добавляем директорию backend в PYTHONPATH
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
