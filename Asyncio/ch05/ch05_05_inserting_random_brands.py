import asyncio
from random import sample
from typing import List, Tuple, Union

from util.db_handler import connect_pg


def load_common_words() -> List[str]:
    with open("res/common_words.txt") as common_words:
        return [word.strip() for word in common_words.readlines()]


def generate_brand_names(words: List[str]) -> List[Tuple[str,]]:
    return [(words[index],) for index in sample(range(100), 100)]


async def insert_brands(common_words, connection) -> int:
    brands = generate_brand_names(common_words)
    insert_brands = "INSERT INTO brand VALUES(DEFAULT, $1)"
    return await connection.executemany(insert_brands, brands)


async def main():
    common_words = load_common_words()
    connection = await connect_pg()
    await insert_brands(common_words, connection)


asyncio.run(main())

