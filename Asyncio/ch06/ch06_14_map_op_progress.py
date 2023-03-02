from concurrent.futures import ProcessPoolExecutor
import functools
import asyncio
from multiprocessing import Value
from typing import List, Dict
from ch06_08_count_words_freq_parallel import (
    partition, merge_dictionaries
)
