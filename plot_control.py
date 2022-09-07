from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter


def ini(self, frame):
    # matplotlibの描画領域の作成
    self.fig = Figure(figsize=(self.width/100, self.height/100))

    self.fig.canvas.mpl_connect('button_press_event', self.onclick)
    # fig.canvas.mpl_connect('motion_notify_event', self.mouse_move)

    # matplotlibの描画領域とウィジェット(Frame)の関連付け
    self.fig_canvas = FigureCanvasTkAgg(self.fig, frame)
    # matplotlibのグラフをフレームに配置
    self.fig_canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)


def plot_data(self):
    self.fig.clear()
    # 座標軸の作成
    positions = []
    for name in self.data_name:
        positions.append(int(self.data_setting[name]["position"]))
    subplot_num = max(positions)
    for i in range(subplot_num):
        ax = self.fig.add_subplot(subplot_num, 1, 1+i)
        for name in self.data_name:
            if self.data_setting[name]['enable'] and int(self.data_setting[name]['position']) == (i+1):
                ax.plot(self.data['Time']/1e6,
                        self.data[name], label=name)
        ax.grid()
        ax.legend()
    self.fig_canvas.draw()
