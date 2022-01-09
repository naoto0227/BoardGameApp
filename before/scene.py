import tkinter as tk
import tkinter.ttk as ttk
import board

TITLE = 'オセロゲーム'
WIDTH = board.UNIT_SIZE * 10
HEIGHT = board.UNIT_SIZE * 10
SIZE = '800x600'
MENU = 'メニュー'
MODE1 = '対戦モード'
MODE2 = '棋譜読み込みモード'
MODE3 = 'アプリの終了'
VALUES = 'プレイヤー', 'COM1(ランダム)', 'COM2(最大)'
WID = 10


class Scene(tk.Frame):

    def __init__(self, master, sc):
        super().__init__(master)
        # 継承元クラス（tk.Frame）のコンストラクタを呼び出し super()=tk.Frame

        self.master.title(TITLE)
        self.master.geometry(SIZE)
        self.sc = sc

        self.scene1_frame = tk.Frame(self.master, borderwidth=2, relief=tk.SUNKEN)
        self.scene2_frame = tk.Frame(self.master, borderwidth=2, relief=tk.SUNKEN)
        self.scene3_frame = tk.Frame(self.master, borderwidth=2, relief=tk.SUNKEN)
        self.scene4_frame = tk.Frame(self.master, borderwidth=2, relief=tk.SUNKEN)
        self.bt = tk.Button(self.scene3_frame, width=10, height=2, bg='yellow', text='リトライ',
                            state=tk.DISABLED, command=self.sc.retry_game)
        self.canvas = tk.Canvas(self.scene3_frame, width=WIDTH, height=HEIGHT, bg='white')
        self.canvas2 = tk.Canvas(self.scene4_frame, width=WIDTH, height=HEIGHT, bg='white')
        self.restart = False

        self.create_scene1()
        self.create_scene2()
        self.create_scene3()
        self.create_scene4()
        self.scene1_frame.tkraise()

    def set_restart(self, flag):
        self.restart = flag

    def create_scene1(self):
        self.scene1_frame.grid(row=0, column=0, sticky="nsew")
        button1 = tk.Button(self.scene1_frame, text=MODE1, width=15,
                            command=lambda: [self.sc.change_scene(self.scene2_frame)])
        button2 = tk.Button(self.scene1_frame, text=MODE2, width=15,
                            command=lambda: [self.sc.read_kihu()])
        button3 = tk.Button(self.scene1_frame, text=MODE3, width=15,
                            command=lambda: [self.master.destroy()])

        button1.pack(expand=True)
        button2.pack(expand=True)
        button3.pack(expand=True)

    def create_scene2(self):
        self.scene2_frame.grid(row=0, column=0, sticky="nsew")
        frame_left = tk.Frame(self.scene2_frame)
        frame_right = tk.Frame(self.scene2_frame)
        label1 = tk.Label(frame_left, text='先手：')
        label2 = tk.Label(frame_right, text='後手：')
        combobox1 = ttk.Combobox(frame_left, state="readonly", values=VALUES)
        combobox2 = ttk.Combobox(frame_right, state="readonly", values=VALUES)
        s1 = tk.Spinbox(frame_left, from_=0, to=59, increment=1, width=WID)
        s2 = tk.Spinbox(frame_left, from_=0, to=59, increment=1, width=WID)
        s3 = tk.Spinbox(frame_right, from_=0, to=59, increment=1, width=WID)
        s4 = tk.Spinbox(frame_right, from_=0, to=59, increment=1, width=WID)
        button = tk.Button(self.scene2_frame, text="決定", width=60,
                           command=lambda: [self.sc.play_game(combobox1.current(), combobox2.current(),
                                                              int(s1.get()), int(s2.get()), int(s3.get()),
                                                              int(s4.get()), self.restart), self.bt.pack_forget()])
        button.pack(expand=True, side=tk.BOTTOM)
        s2.pack(side=tk.BOTTOM)
        s1.pack(side=tk.BOTTOM)
        s4.pack(side=tk.BOTTOM)
        s3.pack(side=tk.BOTTOM)
        frame_left.pack(side=tk.LEFT, pady=100)
        frame_right.pack(side=tk.RIGHT, pady=100)
        combobox1.pack(side=tk.RIGHT)
        label1.pack(side=tk.RIGHT)
        label2.pack(side=tk.LEFT)
        combobox2.pack(side=tk.LEFT)

    def create_scene3(self):
        self.scene3_frame.grid(row=0, column=0, sticky="nsew")
        self.canvas.pack()
        self.bt.pack_forget()

    def create_button_panel(self, frame):
        button_panel = tk.Frame(frame, borderwidth=2, relief=tk.SUNKEN)
        bt1 = tk.Button(button_panel, width=10, height=2, bg='red', text='初期盤面へ',
                        command=lambda: self.sc.kihu_replay(1))
        bt1.pack(pady=10)
        bt2 = tk.Button(button_panel, width=10, height=2, bg='red', text='一手戻る',
                        command=lambda: self.sc.kihu_replay(2))
        bt2.pack(pady=10)
        bt3 = tk.Button(button_panel, width=10, height=2, bg='red', text='一手進む',
                        command=lambda: self.sc.kihu_replay(3))
        bt3.pack(pady=10)
        bt4 = tk.Button(button_panel, width=10, height=2, bg='red', text='終了盤面へ',
                        command=lambda: self.sc.kihu_replay(4))
        bt4.pack(pady=10)
        bt5 = tk.Button(button_panel, width=10, height=2, bg='yellow', text='対局を再開',
                        command=lambda: [self.sc.change_scene(self.scene2_frame),
                                         self.set_restart(True), self.sc.timer_stop()])
        bt5.pack(pady=10)
        bt6 = tk.Button(button_panel, width=10, height=2, bg='yellow', text='初期画面に戻る',
                        command=lambda: self.sc.change_scene(self.scene1_frame))
        bt6.pack(pady=10)

        button_panel.pack(side=tk.TOP, expand=True)

        return button_panel

    def create_scene4(self):
        self.scene4_frame.grid(row=0, column=0, sticky="nsew")
        self.canvas2.pack(side=tk.LEFT)
        kihu_control_panel = self.create_button_panel(self.scene4_frame)
        kihu_control_panel.pack()
