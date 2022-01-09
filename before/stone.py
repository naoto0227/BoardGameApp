class Stone(object):
    BLACK = 1
    WHITE = 2

    def __init__(self):
        # Stoneのコンストラクタ
        self.__obverse = 0
        self.__color = None

    def set_color(self, col):
        # 石の色を設定
        self.__color = col

    def get_color(self):
        # 石の色を返す
        return self.__color

    def set_obverse(self, state):
        # 石の色を設定
        self.__obverse = state

    def get_obverse(self):
        # 石の色を返す
        return self.__obverse

    def draw_stone(self, canvas, x, y, size):
        # 石を描画
        if self.__obverse == 1:
            canvas.create_oval((x + 1) * size + 5, (y + 1) * size + 5, (x + 2) * size - 5, (y + 2) * size - 5,
                               fill='black')
        if self.__obverse == 2:
            canvas.create_oval((x + 1) * size + 5, (y + 1) * size + 5, (x + 2) * size - 5, (y + 2) * size - 5,
                               fill='white')
