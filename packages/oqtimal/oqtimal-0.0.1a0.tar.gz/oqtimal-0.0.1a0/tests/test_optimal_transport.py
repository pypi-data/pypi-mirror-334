
def test_optimal_transport():
    from oqtimal import optimal_transport

    x = [1, 2, 3]
    y = [4, 5, 6]

    x, y = optimal_transport(x, y)
