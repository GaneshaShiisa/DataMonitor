import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import hashlib
import pandas as pd
import time

import plot_control


def open_file(self, file_path):
    # データ読み込み
    if read_data(self, file_path):
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

        self._hash_cur = _get_hash(file_path)

        self.file_path = file_path

        # データ描画
        plot_control.plot_data(self)


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
            self.data_setting[name] = dict(enable=False, position="1")
    return True


def _get_hash(file_path: str) -> str:
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def on_modified(self, event):
    file_path = event.src_path
    # file_name = os.path.basename(file_path)
    time.sleep(0.1)

    hash_new = _get_hash(file_path)
    hash_old = self._hash_cur
    if hash_old != hash_new:
        print(F'{file_path} changed')
        self._hash_cur = hash_new
        # データ読み込み
        read_data(self, file_path)
        # データ描画
        plot_control.plot_data(self)
