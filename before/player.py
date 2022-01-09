import random


class Player(object):
    def __init__(self):
        self.__color = 0
        self.__tactics = 0

    def set_color(self, c):
        self.__color = c

    def get_color(self):
        return self.__color

    def set_tactics(self, t):
        self.__tactics = t

    def get_tactics(self):
        return self.__tactics

    def next_move(self, bd):
        if self.__tactics == 1:
            return self.tactics1(bd)
        elif self.__tactics == 2:
            return self.tactics2(bd)
        return [-1, -1]

    def tactics1(self, bd):
        # ランダム
        candidacy = []
        for i in range(8):
            for j in range(8):
                if self.__color == 'black' and bd.eval_black[i][j] > 0:
                    candidacy.append([i, j])
                if self.__color == 'white' and bd.eval_white[i][j] > 0:
                    candidacy.append([i, j])

        x = random.randint(0, len(candidacy) - 1)
        p = candidacy[x]

        return p

    def tactics2(self, bd):
        # 取れる最大枚数を取りたい
        p = [-1, -1]
        max_stone = 0
        for i in range(8):
            for j in range(8):
                if self.__color == 'black' and bd.eval_black[i][j] > max_stone:
                    max_stone = bd.eval_black[i][j]
                    p = [i, j]
                if self.__color == 'white' and bd.eval_white[i][j] > max_stone:
                    max_stone = bd.eval_white[i][j]
                    p = [i, j]
        return p
