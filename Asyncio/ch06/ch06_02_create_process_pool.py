from multiprocessing import Pool


def say_hello(name: str) -> str:
    return f'Hi there, {name}'

'''
The difference b/w Process() and Pool()
1. Pool does not need to call start or join
2. Pool returns results
'''
if __name__ == '__main__':
    with Pool() as process_pool:
        # apply() is a blocking method though
        hi_jeff = process_pool.apply(say_hello, args=('Jeff',))
        hi_john = process_pool.apply(say_hello, args=('John',))
        print(hi_jeff)
        print(hi_john)
