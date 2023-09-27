from rich import print
from time import perf_counter
import aiohttp
import json
from aiohttp import ClientSession, ClientTimeout, TCPConnector
import asyncio
import aiofiles
from util.const import *
from util.helpers import load_tokens, banner, check_completed, cleanup_files
from rich.progress import Progress

total_valid = 0
total_dead = 0
total_locked = 0
total_consent = 0
total_suspended = 0
write_lock = asyncio.Lock()
count_semaphore = asyncio.Semaphore(1)


async def validity(auth_token, ct0=None, extra=None):
    global total_valid, total_dead, total_locked, total_consent,total_suspended
    cookies = {'auth_token': auth_token}

    if ct0 and not CT0_FIX:
        cookies['ct0'] = ct0
        PROFILE_HEADERS['x-csrf-token'] = ct0

    retries = 0  # Initialize retries
    async with ClientSession(connector=TCPConnector(ssl=False), timeout=ClientTimeout(total=7)) as client:
        for retries in range(MAX_RETRIES):
            try:
                if not ct0 or CT0_FIX:
                    async with client.get('https://twitter.com/i/api/1.1/account/update_profile.json', headers=PROFILE_HEADERS, cookies=cookies, proxy=PROXY) as response:
                        set_cookie_header = response.headers.getall(
                            'Set-Cookie')
                        new_ct0 = next((s.split(';')[0].split(
                            '=')[1] for s in set_cookie_header if 'ct0' in s), None)
                        if new_ct0:
                            cookies['ct0'] = new_ct0
                            PROFILE_HEADERS['x-csrf-token'] = new_ct0
                            if CT0_FIX:
                                ct0 = new_ct0

                async with client.post('https://twitter.com/i/api/1.1/account/update_profile.json', headers=PROFILE_HEADERS, cookies=cookies, proxy=PROXY) as response:
                    source = await response.text()

                    status_map = {
                        200: ("bold green", "VALID"),
                        "https://twitter.com/account/access": ("bold cyan", "LOCKED"),
                        "/i/flow/consent_flow": ("bold yellow", "CONSENT"),
                        "is suspended and": ("bold red", "SUSPENDED")
                    }

                    status_color, status_text = "bold red", "DEAD"
                    for key, value in status_map.items():
                        if key == response.status or str(key) in source:
                            status_color, status_text = value
                            break

                    followers_count = 0
                    response_json = json.loads(source)
                    followers_count = response_json.get('followers_count', 0)

                    # Update global counters
                    async with count_semaphore:
                        if status_text == "VALID":
                            total_valid += 1
                        elif status_text == "DEAD":
                            total_dead += 1
                        elif status_text == "LOCKED":
                            total_locked += 1
                        elif status_text == "CONSENT":
                            total_consent += 1
                        elif status_text == "SUSPENDED":
                            total_suspended += 1

                    line_components = []
                    if extra:
                        line_components.extend(extra)
                    if ct0:
                        line_components.append(ct0)
                    if auth_token:
                        line_components.append(auth_token)

                    composed_token = ':'.join(line_components) + '\n'
                    output_files = []

                    if followers_count >= 100_000:
                        output_files.append('output/100Kplus.txt')
                    if followers_count >= 10_000:
                        output_files.append('output/10Kplus.txt')
                    if followers_count >= 1000:
                        output_files.append('output/1Kplus.txt')
                    if followers_count >= 30:
                        output_files.append('output/30plus.txt')
                    if not output_files:
                        output_files.append(f'output/{status_text.lower()}.txt')

                    for output_file in output_files:
                        async with write_lock:  # Ensure only one task writes to a file at any time
                            async with aiofiles.open(output_file, mode='a') as f:
                                try:
                                    await f.write(composed_token)
                                    await f.flush()  
                                except Exception as e:
                                    print(f"Error writing to {output_file}: {e}")

                    print(
                        f"[{status_color}][[bold white]*[{status_color}]] [{status_color}]{auth_token} [bold white][[{status_color}]{status_text}[bold white]] | Followers: {followers_count}")

                    break
            except (aiohttp.ClientError, asyncio.TimeoutError, Exception) as e:
                print(f"[red]Error: {e}")
                if retries < MAX_RETRIES - 1:
                    print(f"[yellow]Retrying ({retries + 1}/{MAX_RETRIES})...")
                retries += 1
                continue


async def worker(token_queue, progress, task):
    while True:
        line = await token_queue.get()
        if line is None:
            token_queue.task_done()
            break
        max_retries = 10
        retries = 0

        while retries < max_retries:
            try:
                components = line.strip().split(":")
                auth_token = components[-1]
                ct0_value = components[-2] if len(components) > 1 else None
                remaining_components = components[:-2]
                await validity(auth_token, ct0=ct0_value, extra=remaining_components)
                async with count_semaphore:
                    progress.update(task, advance=1)
                token_queue.task_done()
                break

            except Exception as e:
                print(
                    f"[yellow]An error occurred while processing token: {e}. Retrying {retries + 1}/{max_retries}")
                retries += 1
                continue

        if retries == max_retries:
            print(
                f"[red]Max retries reached for token {line}. Saving as error.")
            token_queue.task_done()
            break
            

async def main():
    global total_valid, total_dead, total_locked, total_consent,total_suspended

    await cleanup_files(["consent", "dead", "locked", "valid", "30plus", "suspended", "10Kplus", "1Kplus", "100Kplus"])
    total_tokens = banner()

    await asyncio.sleep(3)
    

    token_queue = asyncio.Queue()
    await load_tokens('tokens.txt', token_queue)
    t1_start = perf_counter()
    # Signal for each worker to terminate
    for _ in range(NUM_THREADS):
        await token_queue.put(None)

    with Progress() as progress:
        task = progress.add_task(
            "[cyan]Checking tokens...", total=total_tokens)
        workers = [worker(token_queue, progress, task)
                   for _ in range(NUM_THREADS)]

        await asyncio.gather(*workers)
        await token_queue.join()

    check_completed(t1_start, total_tokens, total_valid,
                    total_dead, total_locked, total_consent,total_suspended)

if __name__ == "__main__":
    asyncio.run(main())
