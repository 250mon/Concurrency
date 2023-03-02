from multiprocessing import Pool


def say_hello(name: str) -> str:
    return f'Hi there, {name}'

if __name__ == '__main__':
    with Pool() as process_pool:
        # apply_async() is a nonblocking method
        hi_jeff = process_pool.apply_async(say_hello, args=('Jeff',))
        hi_john = process_pool.apply_async(say_hello, args=('John',))
        # need to call get() explicitly
        print(hi_jeff.get())
        print(hi_john.get())
