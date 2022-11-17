def numeric_names():
    n = 0
    while True:
        yield str(n).zfill(5)
        n += 1
