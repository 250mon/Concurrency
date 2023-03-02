import functools
from typing import Dict


def map_frequency(text: str) -> Dict[str, int]:
    words = text.split(' ')
    frequencies = {}
    for word in words:
        frequencies.setdefault(word, 0)
        frequencies[word] += 1
    return frequencies

def merge_dictionaries(first: Dict[str, int],
                       second: Dict[str, int]) -> Dict[str, int]:
    merged = first
    for key in second:
        merged[key] = merged.get(key, 0) + second[key]
    return merged

lines = ["I know what I know",
         "I know what I know",
         "I don't know much",
         "They don't know much"]

mapped_results = list(map(map_frequency, lines))

for result in mapped_results:
    print(result)

print(functools.reduce(merge_dictionaries, mapped_results))