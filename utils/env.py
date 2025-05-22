import os
from pathlib import Path

def load_env_file(filename=".env"):
    """
    Load environment variables from a file into os.environ.

    The .env file is expected to be one directory up from this script.
    Each line should be in KEY=VALUE format. Lines starting with # are ignored.
    """
    script_dir = Path(__file__).resolve().parent
    env_path = script_dir.parent / filename

    if not env_path.exists():
        raise FileNotFoundError(f"No .env file found at: {env_path}")

    with env_path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ[key.strip()] = value.strip()

def get_env_path():
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == "myspo":
            return parent / ".env"
    raise FileNotFoundError("Could not locate 'myspo' project root.")
