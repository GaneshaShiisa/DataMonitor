"""Data Monitor

〇ファイルの更新で再読み込みする
再読み込みしても、見ている範囲は変えない
〇ファイルを読み込める
〇グラフが描画できる
二段以上の表示が切り替えられる
描画データの選択ができる
表示窓の時間的移動ができる
表示窓の縦軸を変更できる
画像として保存できる。
画像保存時に文字や線をかえる。
マウスで示した点のデータ値を表示する
"""
import tkinter
from tkinter import ttk
import tkinter.font

import os
import time
import hashlib
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import json

import numpy
import pandas as pd


class DataMonitor(tkinter.Frame):
    """
    """
    setting_file = "data_monitor_setting.json"

    def __init__(self, master=None):
        super().__init__(master)
        self.width = master.winfo_screenwidth()
        self.height = master.winfo_screenheight()
        self.master = master
        # ショートカットの設定
        # master.bind("<Alt-w>", self.evt_button_work_start)
        # master.bind("<Alt-q>", self.evt_button_break_start)

        # self.create_shortcat(master)
        # ウィジェットの配置
        self.create_widgets()

        # 初期値の設定
        # self.base_time = time.time()
        # self.pause_time = 0
        # self.pause_time_buf = 0
        # self.status = self.STATUS_STOP
        # self.flash_count = 0
        # self.previous_position = pyautogui.position()
        # self.active_time = time.time()

        # スケジューラの起動
        # self.time_buf = round(time.time(), 0)
        # self.time_event()

        # ファイル更新管理準備
        self.observer = Observer()

        # 設定ファイル読み込み

        if os.path.exists(self.setting_file):
            with open(self.setting_file, 'r') as fp:
                setting_data = json.load(fp)
                self.file_path = setting_data["file_path"]
                self.data_name = setting_data["data_name"]
                self.data_setting = setting_data["data_setting"]

                self.open_file(self.file_path)
        else:
            self.file_path = ""
            self.data_name = ""
            self.data_setting = ""

        #
        self.master.protocol("WM_DELETE_WINDOW", self.delete_window)

    def delete_window(self):
        print("終了")
        data_monitor_setting = {
            "file_path": self.file_path, "data_name": self.data_name, "data_setting": self.data_setting}

        with open(self.setting_file, 'w') as fp:
            json.dump(data_monitor_setting, fp, indent=4)

        if self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
        self.master.destroy()

    # def create_shortcat(self, master):

    def create_widgets(self):
        """Widgetの配置
        """
        frame = tkinter.Frame(self)

        # matplotlibの描画領域の作成
        fig = Figure(figsize=(self.width/100, self.height/100))

        fig.canvas.mpl_connect('button_press_event', self.onclick)

        # 座標軸の作成
        self.ax = fig.add_subplot(1, 1, 1)
        # matplotlibの描画領域とウィジェット(Frame)の関連付け
        self.fig_canvas = FigureCanvasTkAgg(fig, frame)
        # matplotlibのツールバーを作成
        # self.toolbar = NavigationToolbar2Tk(self.fig_canvas, frame)
        # matplotlibのグラフをフレームに配置
        self.fig_canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)

        frame.pack()

        # # データ読み込み
        # data = pd.read_csv(
        #     R'data.csv', header=0, index_col=0)
        # data_name = self.data.columns.values

        # # data[data_name[2]].plot()

        # self.ax.plot(data['Time']/1e6, data[data_name[2]])
        # self.ax.grid()
        # self.ax.set_ylabel(data_name[2])
        # self.fig_canvas.draw()

        # self.label_window_size = ttk.Label(
        #     self, text='')
        # self.label_window_size.grid(row=0, column=0)
        # self.label_window_size.pack(side=tkinter.BOTTOM, anchor=tkinter.W)
        # self.label_window_size.place(x=10, y=10, width=50, height=50)
        # self.label_colon = tkinter.Label(self, text=':', font=font_timer)
        # self.label_colon.grid(row=0, column=1, rowspan=2)
        # self.label_ss = tkinter.Label(
        #     self, text='{:02}'.format(0), font=font_timer, width=2)
        # self.label_ss.grid(row=0, column=2, rowspan=2)

        # self.blank = tkinter.Label(self, text=' ')
        # self.blank.grid(row=0, column=3, rowspan=2)

        # font_button = tkinter.font.Font(family="游ゴシック", size=12)
        # self.button_work_start = tkinter.Button(
        #     self, text="作業 ▶", font=font_button, width=6,
        #     command=self.evt_button_work_start)

        # self.button_work_start.grid(row=0, column=4)
        # self.button_break_start = tkinter.Button(
        #     self, text="休憩 ▶", font=font_button, width=6,
        #     command=self.evt_button_break_start)
        # self.button_break_start.grid(row=1, column=4)
        # self.button_pause = tkinter.Button(
        #     self, text="一時停止", font=font_button, width=6,
        #     command=self.evt_button_pause)
        # self.button_pause.grid(row=0, column=5)
        # self.button_stop = tkinter.Button(
        #     self, text="停止", font=font_button, width=6,
        #     command=self.evt_button_stop)
        # self.button_stop.grid(row=1, column=5)

    def set_background_colour(self, color_name):
        """背景色を設定する

        Args:
            color_name (int): 色名称
        """
        # self['bg'] = color_name
        # self.label_mm['bg'] = color_name
        # self.label_colon['bg'] = color_name
        # self.label_ss['bg'] = color_name
        # self.blank['bg'] = color_name

    def set_window_active(self):
        """Windowのアクティブ化
        """
        # # Windowを最前面に移動する
        # self.master.attributes("-topmost", True)
        # self.master.attributes("-topmost", False)
        # # Windowをアクティブにする
        # x, y = pyautogui.position()
        # pyautogui.moveTo(self.master.winfo_x(), self.master.winfo_y())
        # pyautogui.click()
        # pyautogui.moveTo(x, y)  # 元の位置にマウスを戻す

    def onclick(self, event):
        print('button=%d, x=%d, y=%d' % (
            event.button, event.x, event.y))
        print(event.inaxes == self.ax)
        if event.inaxes != None:
            print('xdata=%f, ydata=%f' % (
                event.xdata, event.ydata))

    def open_file(self, file_path):

        # データ読み込み
        if self.read_data(file_path):
            # ファイル更新監視
            event_handler = PatternMatchingEventHandler(
                [os.path.basename(file_path)])
            event_handler.on_modified = self.on_modified

            if self.observer.is_alive():
                self.observer.stop()
                self.observer.join()

            self.observer = Observer()
            self.observer.schedule(event_handler, os.path.dirname(
                file_path), recursive=True)
            self.observer.start()

            self._hash_cur = self._get_hash(file_path)

            self.file_path = file_path

            # データ描画
            self.plot_data()

    def read_data(self, file_path) -> bool:

        # ファイルの存在確認
        if os.path.exists(file_path) == False:
            return False

        # データ読み込み
        data = pd.read_csv(
            file_path, header=0, index_col=0)
        data_name = list(data.columns.values)

        if 'Time' not in data_name:
            return False

        self.data = data

        if self.data_name != data_name:
            self.data_name = data_name
            self.data_setting = {}
            for name in self.data_name:
                self.data_setting[name] = dict(enable=False, test=100)

        return True

    def plot_data(self):
        self.ax.cla()
        for name in self.data_name:
            if self.data_setting[name]['enable']:
                self.ax.plot(self.data['Time']/1e6,
                             self.data[name])
        self.ax.grid()
        self.fig_canvas.draw()

    def on_modified(self, event):
        file_path = event.src_path
        file_name = os.path.basename(file_path)
        time.sleep(0.1)

        hash_new = self._get_hash(file_path)
        hash_old = self._hash_cur
        if hash_old != hash_new:
            print(F'{file_path} changed')
            self._hash_cur = hash_new
            # データ読み込み
            self.read_data(file_path)
            # データ描画
            self.plot_data()

    def _get_hash(self, file_path: str) -> str:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def command_open_file(self):
        file_path = tkinter.filedialog.askopenfilename(
            initialdir=R'C:\Users\kota\Documents\Python\DataMonitor')
        self.open_file(file_path)

    def command_data_select(self):
        win = tkinter.Toplevel(self.master)
        win.geometry("+"+str(self.master.winfo_x())+"+" +
                     str(self.master.winfo_y()+self.master.winfo_height()))

        self.data_enable = []
        for i in range(len(self.data_name)):
            # チェックボックスの設置
            bln = tkinter.BooleanVar()
            bln.set(self.data_setting[self.data_name[i]]['enable'])
            c = tkinter.Checkbutton(
                win, variable=bln, width=5, text='', background='white')
            self.data_enable.append(bln)  # チェックボックスの初期値
            c.grid(row=i, column=0, padx=0, pady=0, ipadx=0, ipady=0)  # 0列目
            # データ名
            a1 = self.data_name[i]
            b1 = tkinter.Label(win, width=20, text=a1,
                               background='white', anchor='w')
            b1.grid(row=i, column=1, padx=0, pady=0, ipadx=0, ipady=0)  # 1列目
        plotButton = tkinter.Button(
            win, text='make plot', command=self.make_plot)
        plotButton.grid(row=len(self.data_name)+1, column=3)  # 3列目

    def make_plot(self):
        for i in range(len(self.data_name)):
            self.data_setting[self.data_name[i]
                              ]['enable'] = self.data_enable[i].get()
        self.ax.cla()
        for name in self.data_name:
            if self.data_setting[name]['enable']:
                self.ax.plot(self.data['Time']/1e6,
                             self.data[name])
        self.ax.grid()
        self.ax.set_ylabel("pitch")  # self.data_name[2]
        self.fig_canvas.draw()


class StatusBar(tkinter.Frame):
    """
    """

    def __init__(self, master=None):
        super().__init__(master)
        # 親のウィンドウサイズを取得
        self.width = master.winfo_width()
        self.height = master.winfo_height()

        # 表示ラベル作成
        self.status_bar = tkinter.Label(
            self, text=F'width={self.width} height={self.height}', borderwidth=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
        self.status_bar.pack(fill=tkinter.X)

        # イベント登録
        master.bind("<Configure>", self.callback)

    def callback(self, event):
        if(event.type != 'configure') and (event.widget != self.master):
            return

        if (event.width == self.width) and (event.height == self.height):
            return

        self.width = event.width
        self.height = event.height

        self.status_bar['text'] = F'width={self.width} height={self.height}'


if __name__ == "__main__":
    root = tkinter.Tk()
    # Windowsサイズの設定
    root.title("Data Monitor")
    width = 1000
    height = 500
    screen_width = root.winfo_screenwidth()
    root.geometry(str(width)+"x"+str(height) +
                  "+"+str(screen_width-width-10)+"+0")
    # master.resizable(0, 0)

    status_bar = StatusBar(master=root)
    status_bar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    app = DataMonitor(master=root)
    app.pack(side=tkinter.TOP, padx=5, pady=5)

    # メニューバー
    menu = tkinter.Menu(root)
    menu_file = tkinter.Menu(menu, tearoff=0)
    menu_file.add_command(label='ファイルを開く', command=app.command_open_file)
    menu_edit = tkinter.Menu(menu, tearoff=0)
    menu_edit.add_command(label='データ選択', command=app.command_data_select)
    menu.add_cascade(label='ファイル', menu=menu_file)
    menu.add_cascade(label='編集', menu=menu_edit)
    root.config(menu=menu)

    app.mainloop()
