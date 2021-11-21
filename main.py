import from_input
import simplex_method

if __name__ == '__main__':
    A, c, b = from_input.get_data(open("input.txt", "r"))
    res = simplex_method.SimplexMethod(A, c, b)
    # print(res.simplex_table)
    res.__repr__()
    print()
    res.iteration()
# rs = 1
# ij = int(input())
# rj = int(input())
# i_s = int(input())
# print((rs * ij - rj * i_s), '/', rs)
