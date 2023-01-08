#!/usr/bin/python3

# # Imports # #
from typing import Optional
import tkinter as tk
import numpy as np

from GcCP import ImgCanvas, Progress, Percent, ColorUI, OverlayUI, ThresholdUI, MedianUI, OpenUI

verbose = True
debug = False


class ColorPicker(tk.Frame):
    canvas: ImgCanvas
    open: OpenUI
    median: MedianUI
    thresh: ThresholdUI
    overlay: OverlayUI
    color: ColorUI
    percent: Percent
    progress: Progress

    img: Optional[np.array]
    scale_factor: float # why does this exist in ColorPicker. Maybe move to Canvas? Definitely for pan and zoom.

    def __init__(self, master=None):
        # Initialize tk.Frame
        super().__init__(master)
        self.master = master
        self.master.title("Geochemist's Color Picker")
        self.master.iconbitmap('./icon/icon.ico')
        self.pack()

        # variables to be used
        # self.original_img = [] Not used anymore. Use self.open.img
        self.img = None
        self.scale_factor = 1
        # self.dist_img = []  # Move inside Threshold class?
        # self.thresh_img = []  # Move inside Threshold class?

        # Initialize widget objects
        self.create_widgets(self)

    def create_widgets(self, master=None):
        # Creates all widget objects, then adds them to frame
        self.canvas = ImgCanvas(master)
        self.canvas.grid(column=2, row=0, rowspan=10)

        self.open = OpenUI(master)
        self.open.grid(column=0, row=0, columnspan=2)

        self.median = MedianUI(master)
        self.median.grid(column=0, row=1, columnspan=2)

        self.thresh = ThresholdUI(master, verbose=True)
        self.thresh.grid(column=0, row=2, columnspan=2)

        self.overlay = OverlayUI(master)
        self.overlay.grid(column=0, row=3)

        self.color = ColorUI(master)
        self.color.grid(column=0, row=4, columnspan=2, rowspan=3)

        self.percent = Percent(master)
        self.percent.grid(column=0, row=8, columnspan=2)

        self.progress = Progress(master)
        self.progress.grid(column=0, row=9)

    def set_busy_state(self, busy=False):
        if busy:
            print('\t\t', 'Processing...')
            self.progress.label.config(text="Processing...")
            self.median.set(None, tk.DISABLED)
            self.thresh.set(None, tk.DISABLED)
            self.overlay.set(None, tk.DISABLED)
            self.color.set(tk.DISABLED, tk.DISABLED)
        else:
            print('\t\t', 'Done!')
            self.progress.label.config(text="Done")
            self.median.set(None, tk.NORMAL)
            self.thresh.set(None, tk.NORMAL)
            self.overlay.set(None, tk.NORMAL)
            self.color.set(tk.NORMAL, tk.NORMAL)
        self.master.update_idletasks()


def main(verbose_flag: bool = True, debug_flag: bool = False):
    # TK init (GUI Start)
    global verbose, debug
    verbose = verbose_flag
    debug = debug_flag
    root = tk.Tk()
    application = ColorPicker(master=root)
    application.mainloop()


if __name__ == '__main__':
    main()
