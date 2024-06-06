# Twitter Account Checker

[![xcloud](https://raw.githubusercontent.com/FatBeeBHW/Twitter-Account-Checker/main/ad.jpg)](https://t.me/twittercrack)

![fatbee twitter checker](https://github.com/FatBeeBHW/Twitter-Account-Checker/assets/121733071/925583c0-24c6-4eeb-8630-9a557e521cff)

Fast, reliable Twitter Account Checker that doesn't lock accounts on check. Yet. And the best part? its free.
Far from perfect code, but feel free to correct whatever you feel it needs correction and open a PR.

The checker supports any format that ends with ct0:auth_token or just auth_token (basically, any format.)

Telegram Chat: https://t.me/twitterfunhouse

# What do i need to use it?

- Some accounts, duh.
- Rota proxy
- Or no proxy at all.

# Config Explanation

```json

{
  "proxy": "https://beeproxies.com | Telegram: @buybee_bot", # Your proxy, ideally rotating one (username:password@host:port)
  "threads": 100, # How fast we go, if you are unsure keep it under 50, ideally 20 (heavlly depends on your system and proxy.)
  "update_console": true, # Dont want messy BRRRRRRRRRR console? Set it to false.
  "save_followers_count": false, # Save followers count for stat accounts.
  "ct0_fix": false, # If your token have broken ct0 but valid auth_token, enable this and it will be fixed.
  "followers_range": {  # Set ranges for collecting stat accounts format is "Number Of followers":"File Name", must have one. Ideally 2.
    "100000": "100000plus",
    "10000": "10000plus",
    "1000": "1000plus",
    "30": "30plus"
  }
}


```

# How to build in to exe

pyinstaller.exe --onefile --name "Twitter Token Checker @fatbeebhw" --icon="icon.png" --collect-all "pyfiglet" main.py
