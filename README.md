# Twitter Account Checker

![image](https://user-images.githubusercontent.com/121733071/213888978-192462cb-68ba-46fa-8919-6d428583842e.png)
![image](https://user-images.githubusercontent.com/121733071/213888978-192462cb-68ba-46fa-8919-6d428583842e.png)

Fast, reliable Twitter Account Checker that doesn't lock accounts on check. Yet. And the best part? its free.
Far from perfect code, but feel free to correct whatever you feel it needs correction and open a PR.

The checker supports any format that ends with ct0:auth_token or just auth_token

Telegram Chat: https://t.me/twitteropensource

# What do i need to use it?

- Some accounts, duh.
- Rota proxy
- or no proxy at all.

# How to build in to exe

pyinstaller.exe --onefile --name "Twitter Checker" --icon="app.ico" --collect-all "pyfiglet" main.py
