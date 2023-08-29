import aiofiles
import os
import pyfiglet
from rich import print
from time import perf_counter
import pyfiglet
from util.const import *


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


async def load_tokens(file_path, token_queue):
    line_count = 0  # Initialize a counter for the lines
    async with aiofiles.open(file_path, mode='r') as f:
        async for line in f:
            line = line.strip()
            await token_queue.put(line)
            line_count += 1  # Increment the counter for each line
    return line_count  # Return the total number of lines read


def banner():
    global total_tokens

    os.system("title FatBee's Account Checker")
    cls()
    ascii_banner = pyfiglet.figlet_format("FatBee's Checker")
    print(f"[yellow]{ascii_banner}")
    print(
        f"[bold white]🐝 Made by [bold yellow]FatBee[/bold yellow]  |  💬 Telegram: [bold cyan]@fatbeebhw[/bold cyan]  |  💬 Telegram Group: [bold cyan]@twitteropensource[/bold cyan]  | ✅ Version: [bold light_green]{VERSION}[/bold light_green]"
    )

    try:
        with open("tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        total_tokens = len(tokens)

        if not tokens:
            print("[yellow]\n[!] Tokens File is Empty.\n")
            exit()
        else:
            print(
                f"[yellow]\n[!] Loaded [cyan]{total_tokens} [yellow]Accounts")

        # Data Usage
        initial_data_usage = total_tokens * 1.1
        expected_data_usage = round(initial_data_usage / 1000, 3)
        print(
            f"[yellow][!] Expected Data Usage is less than [cyan]{expected_data_usage} MB")

        # Expected Time to Complete
        initial_time = total_tokens * 0.035
        minutes, seconds = divmod(initial_time, 60)
        rounded_minutes = round(minutes)
        rounded_seconds = round(seconds)
        print(
            f"[yellow][!] Expected Run Time: [cyan]{rounded_minutes} Minute(s) {rounded_seconds} Second(s)")

        if PROXY_URL:
            print("[bold green][*] You are checking with proxy.")
        else:
            print("[bold red][!] You are checking proxyless!.")

        print(
            "[yellow]━━━━━━━━━━━━━━━━ [bold cyan]Initializing Threads [yellow]━━━━━━━━━━━━━━━━ \n")

    except FileNotFoundError:
        print("[red]\n[!] Tokens.txt file not found.")
        exit()

    return total_tokens  # Return the total number of tokens


def check_completed(t1_start, total_tokens, total_valid, total_dead, total_locked, total_consent):
    cls()
    counts = {
        "VALID": total_valid,
        "DEAD": total_dead,
        "LOCKED": total_locked,
        "CONSENT": total_consent
    }

    total_bad = total_dead + total_locked
    if total_tokens == 0:
        percent = 0  # Avoid dividing by zero
    else:
        percent = (total_bad / total_tokens) * 100
    percent = round(percent, 3)
    final_time = round(perf_counter() - t1_start)
    mm, ss = divmod(final_time, 60)

    ascii_banner = pyfiglet.figlet_format("FatBee's Checker")
    print(f"[bold yellow]{ascii_banner}")
    print(
        f"[bold white]🐝 Made by [bold yellow]FatBee[/bold yellow]  |  💬 Telegram: [bold cyan]@fatbeebhw[/bold cyan]  |  💬 Telegram Group: [bold cyan]@twitteropensource[/bold cyan]  | ✅ Version: [bold light_green]{VERSION}[/bold light_green]")
    print(f"[bold white]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold white]")
    print(
        f"[bold green]⏳ Total Running Time: {mm} Minute(s) {ss} Second(s)[/bold green]")
    print(
        f"[bold yellow][*] [bold white]Accounts Checked: [bold yellow]{total_tokens}[/bold yellow]")
    print(
        f"[bold yellow][*] [bold white]Lock Rate: [bold red]{percent}%[/bold red]")
    print(
        f"[bold yellow][*] [bold white]Valid Accounts: [bold green]{counts['VALID']}[/bold green]")
    print(
        f"[bold yellow][*] [bold white]Invalid Accounts: [bold red]{counts['DEAD']}[/bold red]")
    print(
        f"[bold yellow][*] [bold white]Unlockable: [bold yellow]{counts['LOCKED']}[/bold yellow]")
    print(
        f"[yellow][*] [bold white]Consent Locked: [bold yellow]{counts['CONSENT']}[/bold yellow]")
    print(f"[bold white]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold white]")
    print("[bold red] ** RESTARTING THE CHECKER WILL DELETE ALL THE FILES IN OUTPUT FOLDER **[/bold red]")
    input("Press any key to exit..")


async def cleanup_files(file_names):
    for file_name in file_names:
        async with aiofiles.open(f"output/{file_name}.txt", 'w') as f:
            await f.write('')
