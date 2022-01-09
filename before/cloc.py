import tkinter as tk
import time


class Timer(tk.Frame):
    def __init__(self, master, sc):  # 各ボタンの配置とか
        super().__init__(master)
        self.master = master
        self.started = False
        self.finish = 0
        self.s3 = 0
        self.base_time = 0
        self.n = 0
        self.t = 0
        self.sc = sc

        self.tokei = tk.Label(self, text='00:00', font='Arial, 25')

        self.tokei.grid(row=2, column=0, columnspan=4, padx=5, pady=2, sticky=tk.W + tk.E)

    def start(self):  # Startを押したときの動作
        self.started = True
        self.base_time = time.time()
        self.finish = self.base_time + self.s3
        self.count()

    def count(self):
        if self.started:
            self.t = self.finish - time.time()
            if self.t <= 0:
                self.started = False
                self.sc.msg_dialog()
            else:
                self.tokei.config(text='%02d:%02d' % (self.t / 60, self.t % 60))  # 表示時間を1秒毎に書き換え
                self.master.after(100, self.count)
        else:
            self.master.after(100, self.count)

    def stop(self):  # 停止処理
        self.started = False
        self.tokei.config(text='00:00')

    def set_time(self, minutes, seconds):
        self.s3 = minutes * 60 + seconds

    def change_started(self, flag):
        self.started = flag
