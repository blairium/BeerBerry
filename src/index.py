import os
import threading
import webview

import numpy as np
import pandas as pd

from pathlib import Path
from time import time

class Api:
    def fullscreen(self):
        webview.windows[0].toggle_fullscreen()

    def save_content(self, content):
        filename = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG)
        if not filename:
            return

        with open(filename, 'w') as f:
            f.write(content)

    def ls(self):
        return os.listdir('.')

    def open_file_dialog(self):
        file_types = ('csv (*.csv)', 'All files (*.*)')
        filename = webview.windows[0].create_file_dialog(webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types)
        x = filename[0]
        filename = Path(x)
        print(filename.exists())

        f = open(filename, "r")
        line = f.read()

        #f = pd.read_csv(filename, sep=" ", header=None)
        #line = np.asarray(f)

        return line



def get_entrypoint():
    def exists(path):
        return os.path.exists(os.path.join(os.path.dirname(__file__), path))

    if exists('../gui/index.html'): # unfrozen development
        return '../gui/index.html'

    if exists('../Resources/gui/index.html'): # frozen py2app
        return '../Resources/gui/index.html'

    if exists('./gui/index.html'):
        return './gui/index.html'

    raise Exception('No index.html found')


def set_interval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator

entry = get_entrypoint()

if __name__ == '__main__':
    window = webview.create_window('pywebview-react boilerplate', entry, js_api=Api())
    webview.start()