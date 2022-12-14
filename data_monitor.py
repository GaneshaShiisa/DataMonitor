"""Data Monitor

〇ファイルの更新で再読み込みする
再読み込みしても、見ている範囲は変えない
〇ファイルを読み込める
〇グラフが描画できる
〇二段以上の表示が切り替えられる
〇描画データの選択ができる
表示窓の時間的移動ができる
表示窓の縦軸を変更できる
画像として保存できる。
画像保存時に文字や線をかえる。
マウスで示した点のデータ値を表示する
legendの表示
"""
import tkinter
from tkinter import W, ttk
import tkinter.font

import os
import time
import hashlib
from turtle import pos
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import json
import numpy
import pandas as pd

import file_control
import plot_control


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

        # ファイル更新管理準備
        self.observer = Observer()

        # 設定ファイル読み込み
        if os.path.exists(self.setting_file):
            with open(self.setting_file, 'r') as fp:
                setting_data = json.load(fp)
                self.file_path = setting_data["file_path"]
                self.data_name = setting_data["data_name"]
                self.data_setting = setting_data["data_setting"]
                geometry = setting_data["geometry"]
        else:
            self.file_path = ""
            self.data_name = ""
            self.data_setting = ""
            geometry = str(1000)+"x"+str(500) + "+" + \
                str(master.winfo_screenwidth()-1000-10)+"+0"

        root.geometry(geometry)

        file_control.open_file(self, self.file_path)
        #
        self.master.protocol("WM_DELETE_WINDOW", self.delete_window)

    def delete_window(self):
        print("終了")
        data_monitor_setting = {
            "file_path": self.file_path, "data_name": self.data_name, "data_setting": self.data_setting, "geometry": self.master.geometry()}

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

        plot_control.ini(self, frame)

        frame.pack()

    def onclick(self, event):
        print('button=%d, x=%d, y=%d' % (
            event.button, event.x, event.y))
        # print(event.inaxes == self.ax)
        # if event.inaxes != None:
        #     print('xdata=%f, ydata=%f' % (
        #         event.xdata, event.ydata))

    def mouse_move(self, event):
        if event.inaxes != self.ax:
            self.ax_ln.set_linestyle('none')
        else:
            x, y = event.xdata, event.ydata
            self.ax_ln.set_linestyle('solid')
            self.ax_ln.set_xdata(x)
        self.fig_canvas.draw()

    def on_modified(self, event):
        file_control.on_modified(self, event)

    def command_open_file(self):
        file_path = tkinter.filedialog.askopenfilename()
        file_control.open_file(self, file_path)

    def command_data_select(self):
        win = tkinter.Toplevel(self.master)
        win.geometry("+"+str(self.master.winfo_x())+"+" +
                     str(self.master.winfo_y()+self.master.winfo_height()))

        self.data_enable = []
        self.data_position = []
        for i in range(len(self.data_name)):
            # チェックボックスの設置
            bln = tkinter.BooleanVar()
            bln.set(self.data_setting[self.data_name[i]]['enable'])
            c = tkinter.Checkbutton(
                win, variable=bln, width=0, text='', background='white')
            self.data_enable.append(bln)  # チェックボックスの初期値
            c.grid(row=i, column=0, padx=0, pady=0, ipadx=0, ipady=0)  # 0列目
            # グラフポジション
            cb = ttk.Combobox(win, values=[1, 2, 3, 4], width=1)
            cb.set(self.data_setting[self.data_name[i]]['position'])
            self.data_position.append(cb)
            cb.grid(row=i, column=1, padx=0, pady=0, ipadx=0, ipady=0)  # 1列目
            # データ名
            a1 = self.data_name[i]
            b1 = tkinter.Label(win, width=20, text=a1,
                               background='white', anchor='w')
            b1.grid(row=i, column=2, padx=0, pady=0, ipadx=0, ipady=0)  # 2列目
        plotButton = tkinter.Button(
            win, text='make plot', command=self.make_plot)
        plotButton.grid(row=len(self.data_name)+1, column=3)  # 3列目

    def make_plot(self):
        for i in range(len(self.data_name)):
            self.data_setting[self.data_name[i]
                              ]['enable'] = self.data_enable[i].get()
            self.data_setting[self.data_name[i]
                              ]['position'] = self.data_position[i].get()
        # データ描画
        plot_control.plot_data(self)


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
