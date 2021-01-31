import os


def resolve(lg_rt, t1_rt, t2_rt):
    return lg_rt + (t1_rt + t2_rt - 2 * lg_rt)


def rand():
    """Return a random number between 0 and 1."""
    return int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
