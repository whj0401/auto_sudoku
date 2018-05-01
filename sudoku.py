from enum import Enum
import copy


class CellStatus(Enum):
    BLANK = 0
    STATIC = 1
    CONFIRM = 2
    TRY = 3


class Cell:

    def __init__(self, _x=0, _y=0):
        self.x = _x
        self.y = _y
        self.status = CellStatus.BLANK
        self.v = 0
        self.prediction = {i for i in range(1, 10)}

    def get_3x3_idx(self) -> list:
        br = int(self.x / 3)
        bc = int(self.y / 3)
        li = []
        br = br * 3
        bc = bc * 3
        for i in range(3):
            for j in range(3):
                if br + i == self.x and bc + j == self.y:
                    continue
                li.append((br + i, bc + j))
        return li


M = 9
N = 9


class Sudoku:

    def __init__(self):
        # s is a 9x9 matrix
        self.s = [[Cell(row, column) for column in range(N)] for row in range(M)]

    def init_sudoku(self, _l: list):
        # l must be a 9x9 matrix
        for row in range(M):
            for col in range(N):
                c = self.s[row][col]
                c.v = _l[row][col]
                if c.v != 0:
                    c.status = CellStatus.STATIC
                    c.prediction = {c.v}

    def single_perspective_step(self, row, col):
        c = self.s[row][col]
        # remove false predictions in row
        for i in range(N):
            if i == col or self.s[row][i].status == CellStatus.BLANK:
                continue
            c.prediction -= self.s[row][i].prediction
        # remove false predictions in column
        for i in range(M):
            if i == row or self.s[i][col].status == CellStatus.BLANK:
                continue
            c.prediction -= self.s[i][col].prediction
        # remove false predictions in 3x3 box
        l = c.get_3x3_idx()
        for idx in l:
            tmpC = self.s[idx[0]][idx[1]]
            if tmpC.status == CellStatus.BLANK:
                continue
            c.prediction -= tmpC.prediction
        # return length of predictions
        # if return 0, there is no proper value
        return len(c.prediction)

    def total_perspective_step(self, row, col):
        c = self.s[row][col]
        p = copy.deepcopy(c.prediction)
        l = c.get_3x3_idx()
        for idx in l:
            tmpC = self.s[idx[0]][idx[1]]
            if tmpC.status == CellStatus.BLANK:
                p -= tmpC.prediction
        if len(p) == 1:
            # value is confirmed
            return list(p)[0]
        else:
            # value still cannot be confirmed
            return 0

    def __confirm_cell(self, row, col):
        self.s[row][col].status = CellStatus.CONFIRM
        self.s[row][col].v = list(self.s[row][col].prediction)[0]

    def work_a_step(self):
        for i in range(M):
            for j in range(N):
                if self.s[i][j].status == CellStatus.BLANK:
                    res = self.single_perspective_step(i, j)
                    if res == 1:
                        self.__confirm_cell(i, j)
                        return True
        for i in range(M):
            for j in range(N):
                if self.s[i][j].status == CellStatus.BLANK:
                    res = self.total_perspective_step(i, j)
                    if res > 0:
                        self.s[i][j].prediction = {res}
                        self.__confirm_cell(i, j)
                        return True
        return False

    def work(self):
        has_blank = True
        while(has_blank):
            has_blank = self.work_a_step()
            self.print_sudoku_detail()
        self.print_soduku()

    def print_soduku(self):
        for i in range(M):
            line = str()
            for j in range(N):
                line += '|' + str(self.s[i][j].v)
            line += '|'
            print(line)
        print()

    def print_sudoku_detail(self):
        for i in range(M):
            for j in range(N):
                print('('+str(i)+','+str(j)+') : ' + str(self.s[i][j].prediction) + '->' + str(self.s[i][j].status))
        print()


def num_str_2_int_list(s: str) -> list:
    __l = []
    for idx in range(len(s)):
        __l.append(int(s[idx]))
    return __l


'''
some test_cases
    l1 = [
        [0, 0, 9, 7, 1, 3, 2, 5, 0],
        [0, 3, 0, 8, 0, 2, 0, 6, 0],
        [0, 0, 8, 5, 0, 4, 3, 0, 0],
        [0, 0, 3, 9, 5, 7, 1, 2, 0],
        [0, 1, 4, 2, 0, 0, 7, 3, 0],
        [5, 2, 0, 3, 0, 0, 9, 8, 0],
        [7, 5, 1, 4, 0, 0, 6, 0, 0],
        [0, 0, 0, 0, 7, 0, 8, 0, 0],
        [0, 8, 6, 1, 3, 0, 0, 0, 0]
    ]
    l2 = [
        [0, 2, 8, 0, 0, 0, 1, 0, 9],
        [0, 0, 1, 0, 0, 9, 0, 0, 2],
        [7, 0, 0, 0, 6, 0, 0, 8, 4],
        [4, 1, 2, 0, 0, 0, 0, 9, 0],
        [0, 0, 0, 0, 9, 0, 4, 2, 1],
        [0, 8, 0, 0, 0, 0, 3, 6, 5],
        [1, 9, 0, 0, 0, 3, 7, 5, 6],
        [0, 7, 0, 0, 5, 0, 2, 1, 3],
        [2, 5, 3, 0, 7, 0, 0, 4, 8]
    ]
'''

if __name__ == "__main__":
    S = Sudoku()
    str_list = [
        '000080000',
        '000020879',
        '090706000',
        '205037060',
        '007410290',
        '340008510',
        '030071006',
        '060842035',
        '574690100'
    ]
    li = []
    for s in str_list:
        li.append(num_str_2_int_list(s))
    S.init_sudoku(li)
    S.work()


