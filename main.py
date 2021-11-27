import from_input
from SimplexMethod import SimplexMethod

if __name__ == '__main__':
    A, c, b = from_input.get_data(open('input.txt', 'r'))
    res = SimplexMethod(A, c, b)
    res.__repr__()
    print()
    res.ref_solution()


# c=[8 2 6]
# [-2 -1 0]
# [-1 -2 -0.5]
# [-1 0 -4]
# b=[-7 -7 -6]
