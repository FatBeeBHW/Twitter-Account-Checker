import aiofiles
import os
from rich import print
from rich.prompt import Prompt
from time import perf_counter
import pyfiglet
from util.const import *
import sys
import requests
import time


def fetch_motd(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {
            "date": "Today",
            "message": "Have a nice day!",
            "version": VERSION
        }


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


async def load_tokens(file_path, token_queue):
    line_count = 0
    async with aiofiles.open(file_path, mode='r', encoding="latin-1") as f:
        async for line in f:
            line = line.strip()
            await token_queue.put(line)
            line_count += 1
    return line_count


def calculate_est_time(total_tokens, threads):
    constant_factor = 0.044
    real_time_minutes = (constant_factor * total_tokens) / threads
    minutes = int(real_time_minutes)
    seconds = int((real_time_minutes - minutes) * 60)
    return minutes, seconds


def banner(threads):
    global total_tokens

    os.system("title FatBee's Account Checker")
    cls()

    print(f"""[yellow] _____     _   ____            _        ____ _               _
|  ___|_ _| |_| __ )  ___  ___( )___   / ___| |__   ___  ___| | _____ _ __ 
| |_ / _` | __|  _ \ / _ \/ _ \// __| | |   | '_ \ / _ \/ __| |/ / _ \ '__|
|  _| (_| | |_| |_) |  __/  __/ \__ \ | |___| | | |  __/ (__|   <  __/ |   
|_|  \__,_|\__|____/ \___|\___| |___/  \____|_| |_|\___|\___|_|\_\___|_|""")
    print(
        f"[bold white]🐝 Made by [bold yellow]FatBee[/bold yellow]  |  💬 Telegram: [bold cyan]@fatbeebhw[/bold cyan]  |  💬 Telegram Group: [bold cyan]@twitterfunhouse[/bold cyan]  | ✅ Version: [bold light_green]{VERSION}[/bold light_green ]                                                                                 "  # nopep8
    )
    timestamp = int(time.time())
    motd_url = f"https://raw.githubusercontent.com/FatBeeBHW/Twitter-Account-Checker/main/motd.json?token={timestamp}"
    motd_data = fetch_motd(motd_url)

    try:
        with open("tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        total_tokens = len(tokens)

        if not tokens:
            print("[yellow]\n[!] Tokens File is Empty.\n")
            input("Press any button to exit...")
            sys.exit(0)
        else:
            print(
                f"[yellow]\n[!] Loaded [cyan]{total_tokens:,} [yellow]Accounts")

        # Data Usage
        initial_data_usage = total_tokens * 11.1
        expected_data_usage = round(initial_data_usage / 1000, 3)
        print(
            f"[yellow][!] Expected Data Usage is less than [cyan]{expected_data_usage} MB")

        # Expected Time to Complete
        minutes, seconds = calculate_est_time(total_tokens, threads)
        print(
            f"[yellow][!] Expected Run Time: [cyan]{minutes} Minute(s) {seconds} Second(s)")

        if PROXY_URL:
            print("[bold green][*] You are checking with proxy.")
        else:
            print("[bold red][!] You are checking proxyless!")

        print(
            f"[yellow]━━━━━━━━━━━━━━━━ [bold cyan]Updates & Infos ({motd_data['date']}) [yellow]━━━━━━━━━━━━━━━━ \n")
        print(f"[bold green]📝 Notes:")
        print(f"{motd_data['message']}\n")
        print(
            f"Current Version: {motd_data['version']} | Your version: {VERSION} \n")
        print(
            "[yellow]━━━━━━━━━━━━━━━━ [bold cyan]🚀 Are you ready?[yellow] ━━━━━━━━━━━━━━━━ \n")

        are_you_ready = Prompt.ask(
            "[bold green_yellow]🚀 Are you ready?[/bold green_yellow]", choices=["Yes", "No"], default="Yes")

        if are_you_ready != "Yes":
            print("[bold red]🛑 Stopping...[/bold red]")
            exit()
    except FileNotFoundError:
        print("[red]\n[!] Tokens.txt file not found.")
        input("Press any button to exit...")
        sys.exit(0)

    return total_tokens


def check_completed(t1_start, total_tokens, total_valid, total_dead, total_locked, total_consent, total_suspended, data_usage):
    cls()
    counts = {
        "VALID": total_valid,
        "DEAD": total_dead,
        "LOCKED": total_locked,
        "CONSENT": total_consent,
        "SUSPENDED": total_suspended
    }

    total_bad = total_dead + total_locked + total_suspended + total_consent
    if total_tokens == 0:
        percent = 0  # Avoid dividing by zero
    else:
        percent = (total_bad / total_tokens) * 100
    percent = round(percent, 3)
    final_time = round(perf_counter() - t1_start)
    mm, ss = divmod(final_time, 60)
    timestamp = int(time.time())
    motd_url = f"https://raw.githubusercontent.com/FatBeeBHW/Twitter-Account-Checker/main/motd.json?token={timestamp}"
    motd_data = fetch_motd(motd_url)

    os.system("title FatBee's Account Checker")
    print(f"""[yellow] _____     _   ____            _        ____ _               _
|  ___|_ _| |_| __ )  ___  ___( )___   / ___| |__   ___  ___| | _____ _ __ 
| |_ / _` | __|  _ \ / _ \/ _ \// __| | |   | '_ \ / _ \/ __| |/ / _ \ '__|
|  _| (_| | |_| |_) |  __/  __/ \__ \ | |___| | | |  __/ (__|   <  __/ |   
|_|  \__,_|\__|____/ \___|\___| |___/  \____|_| |_|\___|\___|_|\_\___|_|""")
    print(
        f"[bold white]🐝 Made by [bold yellow]FatBee[/bold yellow]  | 💬 Telegram: [bold cyan]@fatbeebhw[/bold cyan]  | 💬 Telegram Group: [bold cyan]@twitterfunhouse[/bold cyan]  | ✅ Version: [bold light_green]{VERSION}[/bold light_green]")
    print(f"[bold white]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold white]")
    print(
        f"[bold green]⏳ Total Running Time: {mm} Minute(s) {ss} Second(s)[/bold green]")
    print(
        f"[bold green]🌐 Total Data Used: {data_usage:.2f} MB[/bold green]\n")

    print(
        f"[bold yellow][*] [bold white]Accounts Checked: [bold yellow]{total_tokens:,}[/bold yellow]")
    print(
        f"[bold yellow][*] [bold white]Lock Rate: [bold red]{percent}%[/bold red]")
    print(
        f"[bold yellow][*] [bold white]Valid Accounts: [bold green]{counts['VALID']:,}[/bold green]")
    print(
        f"[bold yellow][*] [bold white]Invalid Accounts: [bold red]{counts['DEAD']:,}[/bold red]")
    print(
        f"[bold yellow][*] [bold white]Suspended Accounts: [bold red]{counts['SUSPENDED']:,}[/bold red][bold white] - Im in need of Suspended tokens, you can donate them to me [bold green]@fatbeebhw")
    print(
        f"[bold yellow][*] [bold white]Unlockable: [bold yellow]{counts['LOCKED']:,}[/bold yellow]")
    print(
        f"[yellow][*] [bold white]Consent Locked: [bold yellow]{counts['CONSENT']:,}[/bold yellow]")
    print()
    print(
        f"[yellow]━━━━━━━━━━━━━━━━ [bold cyan]Updates & Infos ({motd_data['date']}) [yellow]━━━━━━━━━━━━━━━━ \n")
    print(f"[bold green]📝 Notes:")
    print(f"{motd_data['message']}\n")
    print(
        f"Current Version: {motd_data['version']} | Your version: {VERSION} \n")

    print(f"[bold white]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold white]")
    print("[bold red] ** RESTARTING THE CHECKER WILL DELETE ALL THE FILES IN OUTPUT FOLDER ** (NOT THE STAT IF ANY)[/bold red]")
    input("Press any key to exit..")


async def cleanup_files(file_names):
    for file_name in file_names:
        async with aiofiles.open(f"output/{file_name}.txt", 'w') as f:
            await f.write('')
