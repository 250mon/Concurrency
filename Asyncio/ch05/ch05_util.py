import asyncpg
from operator import methodcaller

def get_options(file_path="config"):
    with open(file_path, "r") as fd:
        lines = fd.readlines()
    lines = map(methodcaller("strip"), lines)
    lines_filtered = filter(lambda l: not l.startswith("#"), lines)
    lines_dict_iter = map(methodcaller("split", "="), lines_filtered)
    # converting map obj to dict
    # options = {opt1: value1, opt2: value2, ...}
    # options = dict(lines_dict_iter)
    options = {k.strip(): v.strip() for k, v in lines_dict_iter}
    return options


async def connect_pg():
    options = get_options("db_settings")
    host_addr = options['host_addr']
    port_num = int(options['port_num'])
    passwd = options['password']
    connection = await asyncpg.connect(host=host_addr,
                                       port=port_num,
                                       user='postgres',
                                       database='postgres',
                                       password=passwd)
    return connection
