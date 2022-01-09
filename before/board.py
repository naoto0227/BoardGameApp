import stone

UNIT_SIZE = 60
BETWEEN_TIME = 4000


class Board(object):

    def __init__(self, root, canvas, sc):
        # Boardのコンストラクタ
        self.root = root
        self.canvas = canvas
        self.sc = sc

        self.move = 1
        self.m_color = '黒'
        # 手番
        self.num_black = 4
        self.num_white = 4
        # 各盤面におけるひっくりかえせる場所の数
        self.eval_black = [[0 for i in range(8)] for j in range(8)]
        self.eval_white = [[0 for i in range(8)] for j in range(8)]
        # ひっくり返せる石の数

        self.stone = [[stone.Stone() for i in range(8)] for j in range(8)]
        # 石の色を記憶する配列
        self.direction = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
        # 単位ベクトルの配列

        for i in range(8):
            for j in range(8):
                canvas.create_rectangle((i + 1) * UNIT_SIZE, (j + 1) * UNIT_SIZE, (i + 2) * UNIT_SIZE,
                                        (j + 2) * UNIT_SIZE, fill='green', tag=f'{i},{j}')

        canvas.create_oval(3 * UNIT_SIZE - 5, 3 * UNIT_SIZE - 5, 3 * UNIT_SIZE + 5, 3 * UNIT_SIZE + 5, fill='black')
        canvas.create_oval(7 * UNIT_SIZE - 5, 3 * UNIT_SIZE - 5, 7 * UNIT_SIZE + 5, 3 * UNIT_SIZE + 5, fill='black')
        canvas.create_oval(3 * UNIT_SIZE - 5, 7 * UNIT_SIZE - 5, 3 * UNIT_SIZE + 5, 7 * UNIT_SIZE + 5, fill='black')
        canvas.create_oval(7 * UNIT_SIZE - 5, 7 * UNIT_SIZE - 5, 7 * UNIT_SIZE + 5, 7 * UNIT_SIZE + 5, fill='black')

        self.paint(3, 4, 1)
        self.paint(4, 3, 1)
        self.paint(3, 3, 2)
        self.paint(4, 4, 2)
        # 石の描画

        self.sc.fd_kihu()
        # 棋譜の消去

        self.board_val()
        # 初期盤面の評価

        canvas.bind('<Button-1>', self.mouse_canvas)
        self.root.after(BETWEEN_TIME, self.cpu_canvas)

    def cpu_canvas(self):
        if self.sc.player[self.move - 1].get_tactics() != 0:
            if self.move == 1 and self.num_black != 0:
                coordinate = self.sc.player[self.move - 1].next_move(self)
                self.paint(coordinate[0], coordinate[1], self.move)
                self.change_move()
                self.board_val()
            elif self.move == 2 and self.num_white != 0:
                coordinate = self.sc.player[self.move - 1].next_move(self)
                self.paint(coordinate[0], coordinate[1], self.move)
                self.change_move()
                self.board_val()

    def mouse_canvas(self, event):
        # キャンバスを左クリックしたときの処理
        x = event.x // UNIT_SIZE - 1
        y = event.y // UNIT_SIZE - 1
        # マスのインデックスとして使える

        if self.is_on_board(x, y) and self.sc.player[self.move - 1].get_tactics() == 0:
            # 盤面内かどうか
            if self.move == 1 and self.eval_black[x][y] > 0:
                # 手番が黒で、石を置いたときほかの石をひっくり返せるなら
                self.paint(x, y, 1)
                self.change_move()
                self.board_val()
                # 描画、手番の変更、盤面評価
            elif self.move == 2 and self.eval_white[x][y] > 0:
                self.paint(x, y, 2)
                self.change_move()
                self.board_val()

    @staticmethod
    def is_on_board(x, y):
        # 盤面内かどうか
        if (0 <= x <= 7) and (0 <= y <= 7):
            return True
        else:
            return False

    def set_stone(self, x, y, col):
        # マスの石の色を設定
        self.stone[x][y].set_obverse(col)

    def get_line(self, x, y, d):
        # マスから決められた方向に何色の石が何個あるか
        line = []
        px = x + d[0]
        py = y + d[1]
        # 引数のマスのdirection方向の隣マス
        while self.is_on_board(px, py) and self.stone[px][py].get_obverse() != 0:
            # 隣マスが盤面外か、隣マスが空白でないかどうか
            line.append(self.stone[px][py].get_obverse())
            px += d[0]
            py += d[1]
        return line

    def count_reverse_stone(self, x, y, s):
        # このマスに手番の色の石を置いたとき何個ひっくり返せるか
        if self.stone[x][y].get_obverse() != 0:
            return -1
        line = []
        cnt = 0
        for i in range(8):
            # それぞれの方向について調べる
            line.append(self.get_line(x, y, self.direction[i]))
            tmp = 0
            while tmp < len(line[i]) and line[i][tmp] != s:
                tmp += 1
            if tmp < len(line[i]) and tmp != 0 and line[i][tmp] == s:
                cnt += tmp
        return cnt

    def change_move(self):
        # 手番の入れ替え
        if self.move == 1:
            self.sc.timer[self.move - 1].started = False
            self.sc.timer[self.move].start()
            self.move = 2
            self.m_color = '白'
        else:
            self.sc.timer[self.move - 2].start()
            self.sc.timer[self.move - 1].started = False
            self.move = 1
            self.m_color = '黒'

    def count_stone(self, s):
        # 引数となった色の石が盤面に何個あるか
        count = 0
        for i in range(8):
            for j in range(8):
                if self.stone[i][j].get_obverse() == s:
                    count += 1
        return count

    def board_val(self):
        # 盤面評価
        self.num_black = 0
        self.num_white = 0
        self.canvas.delete('eval')
        # 盤面上の手番と石の数のテキスト消去

        for i in range(8):
            for j in range(8):
                self.canvas.itemconfig(f'{i},{j}', fill='green')
                # 前のターンに置けた場所の色を元に戻す

                self.eval_black[i][j] = self.count_reverse_stone(i, j, 1)
                # 添え字のマスに黒を置いたとき、ひっくりかえせる数を返す
                if self.eval_black[i][j] > 0:
                    self.num_black += 1
                    # もしそのマスに黒をおいてもひっくりかえせるなら、ひっくりかえせる場所の数を増やす
                    if self.move == 1:
                        self.canvas.itemconfig(f'{i},{j}', fill='#90ee90')
                        # 手番が黒であれば、次におけるマスの候補としてマスの色を変える

                self.eval_white[i][j] = self.count_reverse_stone(i, j, 2)
                if self.eval_white[i][j] > 0:
                    self.num_white += 1
                    if self.move == 2:
                        self.canvas.itemconfig(f'{i},{j}', fill='#90ee90')

        self.canvas.create_text(300, 30, text=f'{self.m_color}の手番です　　　'
                                              f'黒石：{self.count_stone(1)}  白石：{self.count_stone(2)}', tag='eval')
        # 盤面上の手番と石の数のテキスト
        if self.num_black == 0 and self.num_white == 0:
            # もし、白も黒もどちらも置けないなら、
            self.sc.msg_dialog()
            # ダイアログを出す
        elif self.move == 1 and self.num_black == 0:
            # もし、黒の手番で黒のおけるマスがないなら、
            self.change_move()
            self.board_val()
            # 手番を飛ばして、盤面評価
        elif self.move == 2 and self.num_white == 0:
            self.change_move()
            self.board_val()

        #self.root.after(BETWEEN_TIME, self.cpu_canvas)

    def paint(self, x, y, s):
        # 盤面描画 (count_reverse_stoneと大部分が同じで、冗長性がある)
        self.set_stone(x, y, s)
        self.stone[x][y].draw_stone(self.canvas, x, y, UNIT_SIZE)

        line = []
        for i in range(8):
            # それぞれの方向について調べる
            line.append(self.get_line(x, y, self.direction[i]))
            tmp = 0
            while tmp < len(line[i]) and line[i][tmp] != s:
                tmp += 1
            if tmp < len(line[i]) and tmp != 0 and line[i][tmp] == s:
                for n in range(len(line[i])):
                    if line[i][n] != s:
                        px = x + self.direction[i][0] * (n + 1)
                        py = y + self.direction[i][1] * (n + 1)
                        self.set_stone(px, py, self.move)
                        self.stone[px][py].draw_stone(self.canvas, px, py, UNIT_SIZE)
                    else:
                        break
        self.sc.fw_kihu(x, y, self.move)
        # 棋譜の書き込み

    def copy_stone_info(self, cv):
        b = Board(self.root, cv, self.sc)
        for i in range(8):
            for j in range(8):
                b.stone[i][j] = self.stone[i][j]
        return b
