import copy
from tabulate import tabulate


class SimplexMethod:

    def __init__(self, A, c, b):
        self.SimplexTable = A
        for i in range(len(self.SimplexTable)):
            self.SimplexTable[i].append(b[i])
        self.SimplexTable.append(c)
        self.SimplexTable[len(self.SimplexTable) - 1].append(0)
        self.SimplexTable[len(self.SimplexTable) - 1] = [-i for i in self.SimplexTable[len(self.SimplexTable) - 1]]
        self.OldSimplexTable = copy.deepcopy(self.SimplexTable)
        self.IdxRow = 0
        self.IdxCol = 0

    def get_pivot(self):
        return self.SimplexTable[self.IdxRow][self.IdxCol]

    def perm_col(self):
        free_members = []
        for i in range(len(self.SimplexTable) - 1):
            free_members.append(self.SimplexTable[i][len(self.SimplexTable[0]) - 1])
        if min(free_members) < 0:
            min_col, temp_ind_row = min((val, idx) for (idx, val) in enumerate(free_members))

        min_abs_el = None

        for i in range(len(self.SimplexTable[temp_ind_row]) - 1):
            if min_abs_el == None and self.SimplexTable[temp_ind_row][i] < 0:
                min_abs_el = abs(self.SimplexTable[temp_ind_row][i])
                self.IdxCol = i
            elif self.SimplexTable[temp_ind_row][i] < 0 and abs(self.SimplexTable[temp_ind_row][i]) > min_abs_el:
                min_abs_el = abs(self.SimplexTable[temp_ind_row][i])
                self.IdxCol = i

        return self.IdxCol

    def perm_row(self):
        min_row = None
        for i in range(len(self.SimplexTable) - 1):
            flag = self.SimplexTable[i][self.IdxCol] != 0
            a = self.SimplexTable[i][len(self.SimplexTable[0]) - 1]
            b = self.SimplexTable[i][self.IdxCol]
            if min_row == None and flag and self.SimplexTable[i][len(self.SimplexTable[0]) - 1] / \
                    self.SimplexTable[i][self.IdxCol] > 0:
                min_row = self.SimplexTable[i][len(self.SimplexTable[0]) - 1] / self.SimplexTable[i][self.IdxCol]
                self.IdxRow = i
            elif flag and self.SimplexTable[i][len(self.SimplexTable[0]) - 1] / self.SimplexTable[i][
                self.IdxCol] > 0 and self.SimplexTable[i][
                len(self.SimplexTable[0]) - 1] / self.SimplexTable[i][self.IdxCol] <= min_row:
                min_row = self.SimplexTable[i][len(self.SimplexTable[0]) - 1] / self.SimplexTable[i][self.IdxCol]
                self.IdxRow = i
        return self.IdxRow

    def jordan_transform(self):

        pivot = self.get_pivot()
        self.SimplexTable[self.IdxRow] = [self.SimplexTable[self.IdxRow][i] / pivot for i in
                                          range(len(self.SimplexTable[0]))]
        for i in range(len(self.SimplexTable)):
            self.SimplexTable[i][self.IdxCol] /= -pivot
        self.SimplexTable[self.IdxRow][self.IdxCol] *= -1

        for i in range(len(self.SimplexTable)):
            for j in range(len(self.SimplexTable[0])):
                if i == self.IdxRow or j == self.IdxCol:
                    continue
                else:
                    self.SimplexTable[i][j] = (pivot * self.SimplexTable[i][j] -
                                               self.OldSimplexTable[self.IdxRow][j] *
                                               self.OldSimplexTable[i][self.IdxCol]) / pivot

        self.OldSimplexTable = copy.deepcopy(self.SimplexTable)

    def check_free_members(self):
        flag = True
        for i in range(len(self.SimplexTable) - 1):
            if self.SimplexTable[i][len(self.SimplexTable[0]) - 1] < 0:
                flag = False
                break
        return flag

    def check_obj_func(self):
        flag = True
        for i in range(len(self.SimplexTable[len(self.SimplexTable) - 1]) - 1):
            if self.SimplexTable[len(self.SimplexTable) - 1][i] > 0:
                flag = False
                break
        return flag

    def ref_solution(self):
        iteration = 1
        while self.check_free_members() == False:
            self.perm_col()
            self.perm_row()
            self.jordan_transform()
            print()
            self.__repr__()
            print(f'iteration: {iteration}')
            print("permission col: ", self.IdxCol)
            print("permission row: ", self.IdxRow)
            iteration += 1
        self.optimal()

    def permission_col(self):
        last_row = len(self.SimplexTable) - 1
        min_abs_el = None
        for i in range(len(self.SimplexTable[0]) - 1):
            if min_abs_el == None and self.SimplexTable[last_row][i] > 0:
                min_abs_el = abs(self.SimplexTable[last_row][i])
                self.IdxCol = i
            elif self.SimplexTable[last_row][i] > 0 and abs(self.SimplexTable[last_row][i]) > min_abs_el:
                min_abs_el = abs(self.SimplexTable[last_row][i])
                self.IdxCol = i

        return self.IdxCol

    def optimal(self):
        iteration = 1
        while self.check_obj_func() == False:
            self.permission_col()
            self.perm_row()
            self.jordan_transform()
            print()
            self.__repr__()
            print(f'iteration: {iteration}')
            print("permission col: ", self.IdxCol)
            print("permission row: ", self.IdxRow)
            iteration += 1

    def __repr__(self):
        column_list = ['    '] + [f'    x{i}    ' for i in range(1, len(self.SimplexTable[0]))] + ['  C   ']
        value_list = [[f'x{i}'] for i in range(1, len(self.SimplexTable))] + [['F']]
        for i in range(len(value_list)):
            for j in range(len(column_list) - 1):
                value_list[i].append(self.SimplexTable[i][j])

        return print(tabulate(value_list, column_list, tablefmt='grid', stralign='center'))
