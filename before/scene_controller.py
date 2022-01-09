import tkinter as tk
import board
import player
import scene
import tkinter.filedialog
import tkinter.messagebox
import shutil
from cloc import Timer

KIHU = 'KIHU.txt'
MENU = 'メニュー'
MODE1 = '対戦モード'
MODE2 = '棋譜読み込みモード'
MODE3 = 'アプリの終了'
TYP = [('テキストファイル', '*.txt')]
DIR = '__file__'
EXTENSION = 'txt'
FILE_TYPE = [('Text', '*.txt'), ('Markdown', '*.md')]
TACTICS = [0, 1, 2]


class SceneController(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        # 継承元クラス（tk.Frame）のコンストラクタを呼び出し super()=tk.Frame
        self.side_frame = tk.Frame(self.master)
        self.side_frame.grid(column=1)
        self.timer = [Timer(self.side_frame, self) for i in range(2)]
        self.timer[0].set_time(720, 0)
        self.timer[1].set_time(720, 0)
        self.scene = scene.Scene(self.master, self)
        self.create_menu()

        self.player = [player.Player() for i in range(2)]
        self.player[0].set_color('black')
        self.player[1].set_color('white')

        self.b = board.Board(master, self.scene.canvas, self)
        self.kihu = []
        self.tmp = 0
        self.turn = 1

    @staticmethod
    def change_scene(page):
        page.tkraise()

    def timer_stop(self):
        # タイマーを後で追加したせいで何度も繰り返し呼び出す羽目になったので関数化(timer_grid_forgetも同様)
        self.timer[0].change_started(False)
        self.timer[1].change_started(False)

    def timer_grid_forget(self):
        self.timer[0].grid_forget()
        self.timer[1].grid_forget()

    def create_menu(self):
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=tk.OFF)
        menu_bar.add_cascade(label=MENU, menu=file_menu)

        file_menu.add_command(label=MODE1, command=lambda: [self.change_scene(self.scene.scene2_frame),
                                                            self.timer_stop(), self.timer_grid_forget()])

        file_menu.add_command(label=MODE2, command=lambda: [self.read_kihu()])
        file_menu.add_separator()  # セパレータ
        file_menu.add_command(label=MODE3, command=self.master.destroy)

        # 親のメニューに設定
        self.master.config(menu=menu_bar)

    @staticmethod
    def fd_kihu():
        # 棋譜の消去
        with open(KIHU, mode='w') as f:
            pass

    @staticmethod
    def fw_kihu(x, y, move):
        # 棋譜の書き込み
        with open(KIHU, mode='a') as f:
            f.write(f'{x}, {y}, {move},\n')

    def fs_kihu(self):
        # 棋譜の保存
        try:
            ret = tkinter.filedialog.asksaveasfile(defaultextension=EXTENSION,
                                                   filetypes=FILE_TYPE, initialdir=DIR, title='棋譜を保存')
            shutil.copy(KIHU, ret.name)
        except:
            self.scene.bt['state'] = tk.NORMAL
            self.scene.canvas.pack_forget()
            self.scene.bt.pack(side=tk.RIGHT)
            self.scene.canvas.pack()

    def read_kihu(self):
        # ボタンが押されたらテキストファイルを選べるファイルダイアログを表示
        self.timer_stop()
        self.timer_grid_forget()
        try:
            file = tkinter.filedialog.askopenfilename(filetypes=TYP, initialdir=DIR)
            self.player[0].set_tactics(0)
            self.player[1].set_tactics(0)
            board.Board(self.master, self.scene.canvas2, self)
            self.kihu.clear()
            self.tmp = 0
            with open(file) as f:
                while True:
                    s_line = f.readline()
                    sp_line = s_line.split(',')
                    if s_line == '':
                        break
                    self.kihu.append(sp_line)
            self.change_scene(self.scene.scene4_frame)
        except:
            tkinter.messagebox.showerror('エラー', 'ファイル読み込み失敗\n初期画面に戻ります')
            self.change_scene(self.scene.scene1_frame)

    def kihu_replay(self, n):
        if n == 1:
            self.tmp = 0
        if n == 2 and 0 < self.tmp <= len(self.kihu):
            self.tmp -= 1
        if n == 3 and 0 <= self.tmp < len(self.kihu):
            self.tmp += 1
        if n == 4:
            self.tmp = len(self.kihu)

        self.kihu_paint()

    def kihu_paint(self):
        self.b = board.Board(self.master, self.scene.canvas2, self)
        for i in range(self.tmp):
            board.Board.paint(self.b, int(self.kihu[i][0]), int(self.kihu[i][1]), int(self.kihu[i][2]))
            self.b.change_move()
            self.b.board_val()

    def play_game(self, b, w, s1, s2, s3, s4, restart):
        if b != -1 and w != -1:
            self.player[0].set_tactics(b)
            self.player[1].set_tactics(w)
        if b not in TACTICS or w not in TACTICS or (s1 == 0 and s2 == 0) or (s3 == 0 and s4 == 0):
            # 今までは不正な値が入力されたときに対処できていなかったので、設定しなおしてもらえるようにした
            # (どちらかのプレイヤーの戦術が選ばれなかった場合と、どちらかのタイマーが0秒の時は設定画面に戻る)
            self.change_scene(self.scene.scene2_frame)
        else:
            self.timer[0].set_time(s1, s2)
            self.timer[1].set_time(s3, s4)
            self.timer[0].start()
            self.timer[1].start()
            self.timer[1].change_started(False)
            if b == 0 or w == 0:
                # コンピュータ同士の対戦でタイマーあっても意味ないので人の時のみ表示
                self.timer[0].grid(column=1, row=0, pady=10)
                self.timer[1].grid(column=1, row=1, pady=10)
            else:
                self.timer[0].started = False
            if restart:
                # 対局再開か普通の対局かの判定
                self.b = self.b.copy_stone_info(self.scene.canvas)
                # 棋譜をリプレイするときは対局時と別のキャンパスを使っていたためこのような書き方に・・・
                # やっていることとしては対局再開ボタンが押された時の盤面の色の情報をコピーしています。
                for i in range(8):
                    for j in range(8):
                        self.b.stone[i][j].draw_stone(self.scene.canvas, i, j, board.UNIT_SIZE)
                self.b.board_val()
            else:
                self.b = board.Board(self.master, self.scene.canvas, self)
            self.scene.set_restart(False)
            self.change_scene(self.scene.scene3_frame)

    def retry_game(self):
        self.timer_grid_forget()
        msg = tkinter.messagebox.askquestion('もう一度対戦しますか?')
        if msg == tkinter.messagebox.YES:
            self.change_scene(self.scene.scene2_frame)

    def msg_dialog(self):
        self.timer_stop()
        # ゲーム終了のダイアログ表示 (かなりの冗長性あり)
        if self.timer[1].t <= 0:
            msg = tkinter.messagebox.askquestion('ゲーム終了!', f'時間切れで黒の勝ち!\n \n   棋譜を保存しますか?')
            # 結果とともに、質問形式のダイアログを表示
            if msg == tkinter.messagebox.YES:
                # はい、と答えたなら、
                self.fs_kihu()
        if self.timer[0].t <= 0:
            msg = tkinter.messagebox.askquestion('ゲーム終了!', f'時間切れで白の勝ち!\n \n   棋譜を保存しますか?')
            if msg == tkinter.messagebox.YES:
                self.fs_kihu()
        elif self.b.count_stone(1) > self.b.count_stone(2):
            # もし、黒石のほうが白石よりも多かったら、
            msg = tkinter.messagebox.askquestion('ゲーム終了!', f'黒石：{self.b.count_stone(1)}  '
                                                           f'白石：{self.b.count_stone(2)}で黒の勝ち!\n \n   棋譜を保存しますか?')
            # 結果とともに、質問形式のダイアログを表示
            if msg == tkinter.messagebox.YES:
                # はい、と答えたなら、
                self.fs_kihu()
        elif self.b.count_stone(1) < self.b.count_stone(2):
            msg = tkinter.messagebox.askquestion('ゲーム終了!', f'黒石：{self.b.count_stone(1)}  '
                                                           f'白石：{self.b.count_stone(2)}で白の勝ち!\n \n   棋譜を保存しますか?')
            if msg == tkinter.messagebox.YES:
                self.fs_kihu()
        else:
            msg = tkinter.messagebox.askquestion('ゲーム終了!', f'黒石：{self.b.count_stone(1)}  '
                                                           f'白石：{self.b.count_stone(2)}で引き分け!\n \n   棋譜を保存しますか?')
            if msg == tkinter.messagebox.YES:
                self.fs_kihu()

        self.scene.bt['state'] = tk.NORMAL
        self.scene.canvas.pack_forget()
        self.scene.bt.pack(side=tk.RIGHT)
        self.scene.canvas.pack()
