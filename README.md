# Twitter Account Checker

[![xcloud](https://raw.githubusercontent.com/FatBeeBHW/Twitter-Account-Checker/main/ad.jpg)](https://t.me/twittercrack)

![image](https://user-images.githubusercontent.com/121733071/213888978-192462cb-68ba-46fa-8919-6d428583842e.png)

Fast, reliable Twitter Account Checker that doesn't lock accounts on check. Yet. And the best part? its free.
Far from perfect code, but feel free to correct whatever you feel it needs correction and open a PR.

The checker supports any format that ends with ct0:auth_token or just auth_token

Telegram Chat: https://t.me/twitteropensource

# What do i need to use it?

- Some accounts, duh.
- Rota proxy
- Or no proxy at all.
- 
# Config Explanation
```json

{
    "proxy": "", # Your proxy, without protocol (no http//: in front.)
    "threads": 20, # Number of threads, more threads more speed.
    "ct0_fix": false # Set it to true if you have issues with your ct0 token, this will fix it and save it in the output.
}

```

# How to build in to exe
pyinstaller.exe --onefile --name "Twitter Checker" --icon="app.ico" --collect-all "pyfiglet" main.py
