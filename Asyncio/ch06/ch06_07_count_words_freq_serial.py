import os.path
import time

file_path = os.path.join("res", "googlebooks-eng-all-1gram-20120701-a")
if not os.path.exists(file_path):
    print("File not found")
    exit(0)

freqs = {}

with open(file_path, encoding="utf-8") as f:
    lines = f.readlines()
    start = time.time()

    for line in lines:
        word, _, count, _ = line.split("\t")
        freqs[word] = freqs.setdefault(word, 0) + int(count)

    end = time.time()
    print(f"{end-start:.4f}")
