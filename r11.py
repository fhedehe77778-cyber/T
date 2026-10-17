#!/usr/bin/env python3
"""
Discord 4-char Username Guesser
Commands:
  1 <N>  - generate N usernames (default 200) and save to usernames.txt
  2      - show the last generated batch
  help   - show commands
  exit   - quit
"""

import random
import string
import os
import sys

CHARSET = string.ascii_lowercase + string.digits + "._"
LENGTH = 4
BATCH_FILE = "usernames.txt"
LAST_BATCH = []

def generate_batch(n):
    seen = set()
    result = []
    max_possible = len(CHARSET) ** LENGTH
    if n > max_possible:
        n = max_possible
    while len(result) < n:
        u = ''.join(random.choice(CHARSET) for _ in range(LENGTH))
        if u not in seen:
            seen.add(u)
            result.append(u)
    return result

def save_batch(batch):
    with open(BATCH_FILE, "w") as f:
        f.write("\n".join(batch))

def load_batch():
    if not os.path.exists(BATCH_FILE):
        return []
    with open(BATCH_FILE) as f:
        return [line.strip() for line in f if line.strip()]

def main():
    global LAST_BATCH
    print("Discord 4-char Username Guesser")
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
            print("  1 <N>  - generate N usernames (default 200)")
            print("  2      - show last generated batch")
            print("  help   - this menu")
            print("  exit   - quit")

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

            batch = generate_batch(n)
            LAST_BATCH = batch
            save_batch(batch)

            print(f"\nGenerated {len(batch)} usernames -> {BATCH_FILE}\n")
            for i, u in enumerate(batch, 1):
                print(f"  {i:3d}. {u}")
            print()

        elif cmd == "2":
            batch = LAST_BATCH if LAST_BATCH else load_batch()
            if not batch:
                print("no batch yet. use '1 <N>' first.")
                continue
            print(f"\nLast batch ({len(batch)} usernames):\n")
            for i, u in enumerate(batch, 1):
                print(f"  {i:3d}. {u}")
            print()

        else:
            print("unknown command. type 'help'.")

if __name__ == "__main__":
    main()
