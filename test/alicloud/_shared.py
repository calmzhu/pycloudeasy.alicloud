from functools import reduce
from typing import List, Iterable


def page_collector(pages: Iterable[List]) -> List:
    """
    extend list of list to list.
    :param pages:
    :return:
    """
    return reduce(lambda x, y: x.extend(y) or x, pages, [])
