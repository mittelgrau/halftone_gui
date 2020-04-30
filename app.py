import os
import sys
import glob
import halftone
import threading
import webview
import shortuuid


def on_closing():
    files = glob.glob('./images/*')
    for f in files:
        os.remove(f)


def turnhalftone(path, sample, scale, cyan=5):
    sample = int(sample)
    scale = int(scale)

    h = halftone.Halftone(path)
    h.make(angles=[24, 75, 0, 45],
           antialias=False,
           filename_addition='_halftone',
           percentage=50,
           sample=sample,
           scale=scale,
           style='grayscale')


class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False

    def open_file_dialog(self):
        file_types = ('Image Files (*.jpg;*.png;*.jpeg)', 'All files (*.*)')
        result = window.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
        return result

    def halftoneImage(self, path, sample=1, scale=2, alias=False, cyan=5):
        # path, sample

        base = os.path.basename(path)
        f, e = os.path.splitext(base)
        try:
            os.remove(f"./images/{f}_halftone{e}")
        except:
            print("No File to delete")
        finally:
            filename = f"./images/{f}_halftone{e}"

            turnhalftone(path, sample, scale, cyan)

            uuid = shortuuid.uuid()

            os.rename(filename, f"./images/{f}_{uuid}_{e}")

            response = {
                'message': f"../images/{f}_{uuid}_{e}",
                'cyan': cyan,
            }

            return response

    def error(self):
        raise Exception('This is a Python exception')


if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        'Halftone', './views/index.html', width=700, height=430, resizable=False, fullscreen=False, frameless=False, y=0, x=1440, js_api=api, background_color="#1E1E1E", text_select=False)
    window.closing += on_closing
    webview.start(debug=True)
