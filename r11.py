import random
import string

# بدون حروف/أرقام متشابهة (i, l, o, 0, 1) — تطلع أنظف وأميز
letters = "abcdefghjkmnpqrstuvwxyz"
digits  = "23456789"

seen = set()

def gen(length: int) -> str:
    u = random.choice(letters)  # أول حرف دايماً حرف
    for _ in range(length - 1):
        u += random.choice(letters if random.random() < 0.5 else digits)
    return u

def main():
    while True:
        try:
            cmd = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if cmd != "2":            # أمر واحد فقط
            break

        made = 0
        while made < 20:
            length = 4 if made % 2 == 0 else 5   # رباعي / خماسي بالتناوب
            u = gen(length)
            if u not in seen:                     # منع التكرار
                seen.add(u)
                print(u)
                made += 1

if __name__ == "__main__":
    main()
