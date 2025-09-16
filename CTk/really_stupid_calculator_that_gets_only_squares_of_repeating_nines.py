def square_of_repeating_nines(n):
    s = str(n)
    if not all(i == "9" for i in s) or s == "":
        return None
    length = len(s)
    return int("9" * (length - 1) + "8" + "0" * (length - 1) + "1")

