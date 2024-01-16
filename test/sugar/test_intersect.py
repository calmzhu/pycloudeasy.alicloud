from cloudeasy.sugar.intersect import intersect


def test_intersect_with_equal():
    x = intersect([1, 3, 4, 7], [4, 7, 91])
    assert x.l == [1, 3] and x.r == [91]


def test_intersect_empty():
    x = intersect([1, 3, 5], [1, 9, 19], lambda l, r: r == pow(l, 2))

    assert x.l == [5] and x.r == [19] and x.intersection == [(1, 1), (3, 9)]
