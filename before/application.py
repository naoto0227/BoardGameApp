import tkinter as tk
import scene_controller


class Application(tk.Frame):

    # tk.Frameを継承したApplicationクラスを作成
    def __init__(self, master=None):
        super().__init__(master)
        scene_controller.SceneController(root)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
