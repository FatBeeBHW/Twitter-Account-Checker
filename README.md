
# Twitter Account Checker 🐦

[![xcloud](https://raw.githubusercontent.com/FatBeeBHW/Twitter-Account-Checker/main/ad.jpg)](https://t.me/twittercrack)

![fatbee twitter checker](https://github.com/FatBeeBHW/Twitter-Account-Checker/assets/121733071/925583c0-24c6-4eeb-8630-9a557e521cff)

Fast and reliable Twitter Account Checker that’s safe to use without risking account locks (for now). Best part? It's completely free! 🎉

Feel free to improve the code and open a PR if you see room for enhancements. This checker supports any account format that ends with `ct0:auth_token` or simply `auth_token`.

📢 **Join our Telegram Chat**: [Twitter Funhouse](https://t.me/twitterfunhouse)

---

## 🚀 Features

- **Flexible Format:** Works with any format ending in `ct0:auth_token` or just `auth_token`.
- **Customizable Settings:** Adjust threads, follower count, and other options.
- **Proxies Optional:** Use with a rotating proxy for optimal results, but works without one too.
  
---

## 🔧 Requirements

- Some Twitter accounts to check, obviously. 😉
- Ideally, a rotating proxy, though a proxy isn’t strictly necessary in case you need to check few accounts. 

---

## ⚙️ Configuration Guide

Customize your settings using the following configuration format:

```json
{
  "proxy": "https://beeproxies.com | Telegram: @buybee_bot", // Your proxy, ideally rotating (format: username:password@host:port)
  "threads": 500, // Speed of checks. For most setups, keep under 200; ideally 100 (depends on your system and proxy).
  "update_console": true, // Set to false to reduce console clutter.
  "save_followers_count": false, // Enable to save follower count for stat accounts.
  "ct0_fix": false, // Set to true if ct0 token is broken but auth_token is valid.
  "followers_range": {  // Ranges for saving stat accounts by followers, format is "Follower Count":"File Name"
    "100000": "100000plus",
    "10000": "10000plus",
    "1000": "1000plus",
    "30": "30plus"
  }
}
```

---

## 🛠️ Building the Checker into an Executable

To create an executable from the script, use **PyInstaller** with the following command:

```bash
pyinstaller.exe --onefile --name "Twitter Token Checker @fatbeebhw" --icon="icon.png" --collect-all "pyfiglet" main.py
```

This will bundle everything into a single executable file named **"Twitter Token Checker @fatbeebhw"** with an icon of your choice.

