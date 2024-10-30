import asyncio
import curl_cffi
from curl_cffi.requests import AsyncSession
from rich import print
from time import perf_counter
import random
import aiofiles
import psutil
from util.const import *
from util.helpers import load_tokens, banner, check_completed, cleanup_files
from rich.progress import Progress
import os
import warnings
import orjson

warnings.filterwarnings("ignore")
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


total_valid = 0
total_dead = 0
total_locked = 0
total_consent = 0
total_suspended = 0
write_lock = asyncio.Lock()
count_semaphore = asyncio.Semaphore(1)


async def validity(auth_token, ct0=None, extra=None):
    global total_valid, total_dead, total_locked, total_consent, total_suspended
    cookies = {'auth_token': auth_token}

    if ct0 and not CT0_FIX:
        cookies['ct0'] = ct0
        PROFILE_HEADERS['x-csrf-token'] = ct0

    async with AsyncSession(proxy=PROXY, impersonate=random.choice(["chrome124", "chrome123"]), timeout=10, max_clients=1) as client:
        while True:
            try:
                if not ct0 or CT0_FIX:
                    response = await client.head('https://business.x.com/', headers=PROFILE_HEADERS, cookies=cookies)

                    ct0_value = response.cookies.get('ct0')

                    if ct0_value:
                        cookies['ct0'] = ct0_value
                        PROFILE_HEADERS['x-csrf-token'] = ct0_value
                        if CT0_FIX:
                            ct0 = ct0_value
                    else:
                        continue

                response = await client.post('https://api.x.com/1.1/account/update_profile.json', headers=PROFILE_HEADERS, cookies=cookies)

                response_json = orjson.loads(response.content)

                error_info = response_json.get('errors', [{}])[0]
                error_code = error_info.get('code', response.status_code)
                bounce_location = error_info.get('bounce_location', '')

                status_map = {
                    326: ("bold steel_blue1", "LOCKED") if bounce_location != '/i/flow/consent_flow' else ("bold yellow", "CONSENT"),
                    200: ("bold chartreuse1", "VALID"),
                    32: ("red", "DEAD"),
                    64: ("bold red3", "SUSPENDED"),
                }

                status_color, status_text = status_map.get(
                    error_code, ("bold red", "UNKNOWN"))

                # Check if the status is valid
                if status_text == "VALID":
                    followers_count = response_json.get('followers_count', 0)
                elif status_text in ("DEAD", "SUSPENDED", "LOCKED", "CONSENT"):
                    followers_count = 0
                else:
                    continue

                composed_token = ':'.join(
                    str(item)
                    for sublist in [extra, ct0, auth_token]
                    for item in (sublist if isinstance(sublist, list) else [sublist])
                    if item is not None
                )

                if followers_count >= MIN_THRESHOLD:
                    output_file = next(
                        (f'output/{name}.txt' for threshold, name in THRESHOLDS.items() if followers_count >= threshold))
                    if SAVE_FOLLOWER_COUNT:
                        composed_token += f":{followers_count}\n"
                    else:
                        composed_token += "\n"
                else:
                    composed_token += "\n"
                    output_file = f'output/{status_text.lower()}.txt'

                async with write_lock:
                    async with aiofiles.open(output_file, mode='a', encoding="latin-1") as f:
                        try:
                            await f.write(composed_token)
                            await f.flush()
                        except Exception as e:
                            print(f"Error writing to {output_file}: {e}")
                if UPDATE_CONSOLE:
                    print(f"[{status_color}][[bold white]*[{status_color}]] [{status_color}]{
                          auth_token} [bold white][[{status_color}]{status_text}[bold white]] | Followers: {followers_count:,}")

                return status_text
            except (curl_cffi.CurlError, curl_cffi.CurlECode, Exception) as e:
                print(e)
                return None


async def get_network_usage():
    network_stats = psutil.net_io_counters()
    return network_stats.bytes_sent, network_stats.bytes_recv


async def worker(token_queue, progress, task, total_tokens):
    global total_valid, total_dead, total_locked, total_consent, total_suspended

    while True:
        line = await token_queue.get()
        if line is None:
            token_queue.task_done()
            break

        max_retries = 10
        retries = 0
        for retries in range(max_retries):
            try:
                components = line.strip().split(":")
                auth_token = components[-1]
                ct0_value = components[-2] if len(components) > 1 else None
                remaining_components = components[:-2]

                status_text = await validity(auth_token, ct0=ct0_value, extra=remaining_components)
                async with count_semaphore:
                    status_counters = {
                        "VALID": total_valid,
                        "DEAD": total_dead,
                        "LOCKED": total_locked,
                        "CONSENT": total_consent,
                        "SUSPENDED": total_suspended
                    }

                    status_counters[status_text] += 1
                    total_valid, total_dead, total_locked, total_consent, total_suspended = status_counters.values()
                    progress.update(task, advance=1)
                    completed = progress.tasks[task].completed
                    progress.update(
                        task,
                        description=f"[bold cyan][*] [white]Checked [green]{completed:,} [white]of [green]{total_tokens:,} [white]tokens · Valid: {total_valid:,} · Suspended: {total_suspended:,} · Dead: {total_dead:,} · Locked: {total_locked:,}" + (
                            " · [bold red]!!! DO NOT CLOSE, LAST TOKENS ARE SOMETIMES VERY SLOW !!! · " if total_tokens - completed <= 100 else "")
                    )
                    os.system(
                        f"title Status: {completed:,} of {total_tokens:,} checked · Valid: {total_valid:,} · Suspended: {total_suspended:,} · Dead: {total_dead:,} · Locked: {total_locked:,} · Telegram: @fatbeebhw")
                token_queue.task_done()
                break

            except Exception as e:
                print(
                    f"[yellow][!] Error: {auth_token} | ({retries + 1}/{max_retries})...")
                retries += 1
                continue

        else:
            print(
                f"[red]Max retries reached for token {line}. Saving as error.")
            token_queue.task_done()
            break


async def main():
    global total_valid, total_dead, total_locked, total_consent, total_suspended

    await cleanup_files(["consent", "dead", "locked", "valid", "suspended"])
    total_tokens = banner(NUM_THREADS)

    await asyncio.sleep(3)

    token_queue = asyncio.Queue()
    await load_tokens('tokens.txt', token_queue)
    t1_start = perf_counter()

    for _ in range(NUM_THREADS):
        await token_queue.put(None)

    start_sent, start_recv = await get_network_usage()
    with Progress() as progress:
        task = progress.add_task(
            "[cyan]Checking tokens...", total=total_tokens)
        workers = [worker(token_queue, progress, task, total_tokens)
                   for _ in range(NUM_THREADS)]

        await asyncio.gather(*workers)
        await token_queue.join()
    end_sent, end_recv = await get_network_usage()
    sent_megabytes = (end_sent - start_sent) / (1024 ** 2)
    recv_megabytes = (end_recv - start_recv) / (1024 ** 2)
    data_usage = sent_megabytes + recv_megabytes

    check_completed(t1_start, total_tokens, total_valid,
                    total_dead, total_locked, total_consent, total_suspended, data_usage)

if __name__ == "__main__":
    asyncio.run(main())
