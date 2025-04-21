import os

def load_env_file(path=".env"):
    """
    Load environment variables from a file into os.environ.

    Each line should be in KEY=VALUE format. Lines starting with # are ignored.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No .env file found at: {path}")

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ[key.strip()] = value.strip()
