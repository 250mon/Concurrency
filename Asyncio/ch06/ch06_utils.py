from typing import Dict, List


def partition(data: List, chunk_size: int) -> List:
    for i in range(0, len(data), chunk_size):
        yield data[i: i + chunk_size]

def merge_dictionaries(first: Dict[str, int],
                       second: Dict[str, int]) -> Dict[str, int]:
    merged = first
    for key in second:
        merged[key] = merged.get(key, 0) + second[key]
    return merged

def map_frequencies(chunk: List[str]) -> Dict[str, int]:
    counter = {}
    for line in chunk:
        word, _, count, _ = line.split('\t')
        counter[word] = counter.setdefault(word, 0) + int(count)
    return counter
