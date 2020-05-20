import itertools


def join_lists(list_of_lists: list) -> list:
    return list(itertools.chain.from_iterable(list_of_lists))
