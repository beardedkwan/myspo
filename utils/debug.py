import os
import json
import inspect
from datetime import datetime

DEBUG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "debug.txt")

def log(data) -> None:
    """Log data to debug.txt with timestamp and calling function context."""
    # Get the caller's frame info
    frame = inspect.stack()[1]
    caller = f"{frame.function}() in {os.path.basename(frame.filename)}:{frame.lineno}"

    with open(DEBUG_FILE_PATH, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {caller}\n")

        if isinstance(data, (dict, list)):
            f.write(json.dumps(data, indent=2))
        else:
            f.write(str(data))

        f.write("\n\n")
