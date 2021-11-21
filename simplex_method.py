import copy
from tabulate import tabulate


class SimplexMethod:
    def __init__(self, A, c, b):
        self.simplex_table = A
        for i in range(len(self.simplex_table)):
            self.simplex_table[i].append(b[i])
        self.simplex_table.append([-i for i in c])
        self.simplex_table[len(self.simplex_table) - 1].append(0)

        self.old_simplex_table = copy.deepcopy(self.simplex_table)
        self.ind_row = 0
        self.ind_col = 0

    def get_pivot(self):
        return self.simplex_table[self.ind_row][self.ind_col]

    def perm_col(self):
        # индекс последней строки симплекс таблицы (F)
        last_row_ind = len(self.simplex_table) - 1

        # наименьший отрицательный по модулю элемент в последней строке (F)
        min_c = -abs(self.simplex_table[last_row_ind][0])

        # размер строки в симплекс таблице
        row_size = len(self.simplex_table[0]) - 1
        for i in range(row_size):
            if -abs(self.simplex_table[last_row_ind][i]) <= min_c:
                min_c = -abs(self.simplex_table[last_row_ind][i])
                self.ind_col = i

    # def perm_row(self):
    #
    #     min_r = 0
    #     # проходимся по всем строчкам симплекс таблицы
    #     for i in range(len(self.simplex_table) - 1):
    #         flag = self.simplex_table[i][self.ind_col] != 0
    #         if min_r == 0 and flag and self.simplex_table[i][self.ind_col] > 0:
    #             min_r = self.simplex_table[i][len(self.simplex_table[0]) - 1] / self.simplex_table[i][self.ind_col]
    #             self.ind_row = i
    #         elif flag and self.simplex_table[i][self.ind_col] > 0 and self.simplex_table[i][
    #             len(self.simplex_table[0]) - 1] / self.simplex_table[i][self.ind_col] <= min_r:
    #             min_r = self.simplex_table[i][len(self.simplex_table[0]) - 1] / self.simplex_table[i][self.ind_col]
    #             self.ind_row = i

    def perm_row(self):
        min_r = 0
        for i in range(len(self.simplex_table) - 1):
            flag = self.simplex_table[i][self.ind_col] != 0
            if min_r == 0 and flag and self.simplex_table[i][len(self.simplex_table[0]) - 1] / self.simplex_table[i][
                self.ind_col] > 0:
                min_r = self.simplex_table[i][len(self.simplex_table[0]) - 1] / self.simplex_table[i][self.ind_col]
                self.ind_row = i
            elif flag and self.simplex_table[i][len(self.simplex_table[0]) - 1] / self.simplex_table[i][
                self.ind_col] > 0 and self.simplex_table[i][len(self.simplex_table[0]) - 1] / self.simplex_table[i][
                self.ind_col] <= min_r:

                min_r = self.simplex_table[i][len(self.simplex_table[0]) - 1] / self.simplex_table[i][self.ind_col]
                self.ind_row = i

    def jordan_transform(self):
        pivot = self.get_pivot()
        for i in range(len(self.simplex_table[0])):
            self.simplex_table[self.ind_row][i] /= pivot
        for i in range(len(self.simplex_table)):
            self.simplex_table[i][self.ind_col] /= -pivot
        self.simplex_table[self.ind_row][self.ind_col] = -self.simplex_table[self.ind_row][self.ind_col]

        for i in range(len(self.simplex_table)):
            for j in range(len(self.simplex_table[0])):
                if i == self.ind_row or j == self.ind_col:
                    continue
                else:
                    self.simplex_table[i][j] = (pivot * self.simplex_table[i][j] -
                                                self.old_simplex_table[self.ind_row][j] *
                                                self.old_simplex_table[i][self.ind_col]) / pivot

        self.old_simplex_table = copy.deepcopy(self.simplex_table)

    def boolich(self):
        flag = True
        for i in range(len(self.simplex_table[0]) - 1):
            if self.simplex_table[len(self.simplex_table) - 1][i] < 0:
                flag = False
                break

        return flag

    def iteration(self):
        iteration = 1
        while self.boolich() == False:
            self.perm_col()
            self.perm_row()
            self.jordan_transform()
            print()
            self.__repr__()
            print(f'iteration: {iteration}')
            print("permission col: ", self.ind_col + 1)
            print("permission row: ", self.ind_row + 1)
            iteration += 1

    def __repr__(self):
        column_list = ['    '] + [f'    x{i}    ' for i in range(1, len(self.simplex_table[0]))] + ['  C   ']
        value_list = [[f'x{i}'] for i in range(1, len(self.simplex_table))] + [['F']]
        for i in range(len(value_list)):
            for j in range(len(column_list) - 1):
                value_list[i].append(self.simplex_table[i][j])

        return print(tabulate(value_list, column_list, tablefmt='grid', stralign='center'))
