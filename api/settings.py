import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# todo: specify this as an environment variable, rather than relative to the code?
DOWNLOADED_FILE_CACHE_DIR = os.path.join(BASE_DIR, "download_cache")
