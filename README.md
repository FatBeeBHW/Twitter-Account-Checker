# Twitter Account Checker
Fast, reliable Twitter Account Checker that doesn't lock accounts on check. Yet. And the best part? its free.
Far from perfect code, but feel free to correct whatever you feel it needs correction and open a PR.

The checker supports and auto detect the following formats:
- user:pass:email/phone:auth
- user:pass:email/phone:ct0:auth
- token only

Telegram Chat: https://t.me/twitteropensource


# What do i need to use it?
- Some accounts, duh.
- Rota proxy

# How to build in to exe
pyinstaller.exe --onefile --name "Twitter Checker" --icon="app.ico" --collect-all "pyfiglet" main.py
