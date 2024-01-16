from cloudeasy.sugar.intersect import intersect


def test_intersect_with_equal():
    x = intersect([1, 3, 4, 7], [4, 7, 91])
    assert x.l == [1, 3] and x.r == [91]


def test_intersect_customer_compare():
    x = intersect([1, 3, 5], [1, 9, 19], lambda l, r: r == pow(l, 2))

    assert x.l == [5] and x.r == [19] and x.intersection == [(1, 1), (3, 9)]


def test_bool_intersection():
    case1 = intersect([1, 3], [1, 3])
    assert bool(case1) is True

    case2 = intersect([1, 3, 5], [2, 4, 6])
    assert bool(case2) is False
