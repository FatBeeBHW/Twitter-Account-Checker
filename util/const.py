import json

VERSION = "8.0.0"

PROFILE_HEADERS = {
    'x-twitter-client-language': 'en',
    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'content-type': 'application/x-www-form-urlencoded',
    'Referer': 'https://x.com/',
    'x-twitter-auth-type': 'OAuth2Session',
    'x-twitter-active-user': 'yes',
}

with open("config.json", "r") as f:
    config = json.load(f)

PROXY_URL = config.get("proxy")
NUM_THREADS = config.get("threads")
CT0_FIX = config.get("ct0_fix")
MAX_RETRIES = 10
UPDATE_CONSOLE = config.get("update_console")
SAVE_FOLLOWER_COUNT = config.get("save_followers_count")
THRESHOLDS = {int(k): v for k, v in config['followers_range'].items()}
MIN_THRESHOLD = min(THRESHOLDS.keys())

if PROXY_URL:
    PROXY = f"http://{PROXY_URL}"
else:
    PROXY = None
