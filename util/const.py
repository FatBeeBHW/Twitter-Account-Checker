import json
VERSION = "5.0"
PROFILE_HEADERS = {
    'authority': 'twitter.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'origin': 'https://twitter.com',
    'referer': 'https://twitter.com/settings/profile',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'x-twitter-active-user': 'yes',
    'x-twitter-auth-type': 'OAuth2Session',
    'x-twitter-client-language': 'en'
}

with open("config.json", "r") as f:
    config = json.load(f)

PROXY_URL = config.get("proxy")
NUM_THREADS = config.get("threads")
CT0_FIX = config.get("ct0_fix")
MAX_RETRIES = 10

if PROXY_URL:
    PROXY = f"http://{PROXY_URL}"
else:
    PROXY = None
