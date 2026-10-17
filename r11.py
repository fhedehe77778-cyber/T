#!/usr/bin/env python3
"""
Discord 4-char Username Checker
Commands:
  1 <N>  - generate and check N usernames (default 200)
  2      - show available usernames found
  delay <s> - set delay between checks (default 22)
  help   - show commands
  exit   - quit
"""

import random
import string
import time
import json
import urllib.request
import urllib.error
import os

CHARSET = string.ascii_lowercase + string.digits + "._"
LENGTH = 4
API_URL = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"
AVAILABLE_FILE = "available.txt"
BATCH_FILE = "usernames.txt"

DELAY = 22
DELAY_JITTER = 4  # +/- seconds so pattern isn't fixed

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36"
}

def generate_username():
    return ''.join(random.choice(CHARSET) for _ in range(LENGTH))

def check_username(username):
    payload = json.dumps({"username": username}).encode("utf-8")
    req = urllib.request.Request(API_URL, data=payload, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return not data.get("taken", True), resp.status
    except urllib.error.HTTPError as e:
        return None, e.code
    except Exception as e:
        return None, str(e)

def load_available():
    if not os.path.exists(AVAILABLE_FILE):
        return []
    with open(AVAILABLE_FILE) as f:
        return [line.strip() for line in f if line.strip()]

def main():
    global DELAY
    print("Discord 4-char Username Checker")
    print("Type 'help' for commands.\n")

    while True:
        try:
            cmd = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye")
            break

        if not cmd:
            continue

        if cmd.lower() == "exit":
            break

        elif cmd.lower() == "help":
            print("  1 <N>     - generate and check N usernames (default 200)")
            print("  2         - show available usernames found")
            print("  delay <s> - set delay between checks (default 22)")
            print("  help      - this menu")
            print("  exit      - quit")

        elif cmd.lower().startswith("delay"):
            parts = cmd.split()
            if len(parts) != 2:
                print("usage: delay <seconds>")
                continue
            try:
                DELAY = float(parts[1])
                print(f"delay set to {DELAY}s")
            except ValueError:
                print("invalid number")

        elif cmd.startswith("1"):
            parts = cmd.split()
            n = 200
            if len(parts) > 1:
                try:
                    n = int(parts[1])
                    if n <= 0:
                        print("number must be positive")
                        continue
                except ValueError:
                    print("usage: 1 <number>   (or just '1' for 200)")
                    continue

            print(f"\nChecking {n} usernames (delay ~{DELAY}s)...\n")
            generated = []
            available = []
            checked = 0
            attempts = 0

            while checked < n:
                u = generate_username()
                attempts += 1
                if attempts > n * 10:
                    print("too many collisions, stopping early.")
                    break

                if u in generated:
                    continue

                generated.append(u)
                ok, status = check_username(u)
                checked += 1

                if status == 429:
                    print(f"  [{checked}/{n}] {u} -> 429 rate limited, waiting 90s...")
                    time.sleep(90)
                    continue

                if ok is True:
                    available.append(u)
                    print(f"  [{checked}/{n}] {u} -> [+] AVAILABLE")
                elif ok is False:
                    print(f"  [{checked}/{n}] {u} -> [-] taken")
                else:
                    print(f"  [{checked}/{n}] {u} -> [?] error: {status}")

                if checked < n:
                    jitter = random.uniform(-DELAY_JITTER, DELAY_JITTER)
                    time.sleep(max(5, DELAY + jitter))

            with open(BATCH_FILE, "w") as f:
                f.write("\n".join(generated))

            if available:
                with open(AVAILABLE_FILE, "a") as f:
                    f.write("\n".join(available) + "\n")

            print(f"\nDone. Checked {checked} usernames.")
            print(f"Available: {len(available)}")
            if available:
                print("Saved to " + AVAILABLE_FILE)
            print(f"Full batch saved to {BATCH_FILE}\n")

        elif cmd == "2":
            available = load_available()
            if not available:
                print("no available usernames yet.")
                continue
            print(f"\nAvailable usernames ({len(available)}):\n")
            for i, u in enumerate(available, 1):
                print(f"  {i:3d}. {u}")
            print()

        else:
            print("unknown command. type 'help'.")

if __name__ == "__main__":
    main()
