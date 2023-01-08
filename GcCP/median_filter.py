#!/usr/bin/python3

# # Imports # #
from typing import Optional
import tkinter as tk
from tkinter import ttk
from scipy.ndimage import median_filter


class MedianUI(tk.Frame):
    """UI for applying median filter"""
    verbose: bool
    debug: bool

    enable: tk.IntVar  # Median Flag
    check: ttk.Checkbutton  # Toggle Median Filter
    frame: tk.Frame  # Median Neighbors Frame
    spinbox: ttk.Spinbox  # Median Neighbors Selection
    var: tk.StringVar  # self.spinbox Value
    label: ttk.Label  # Median Neighbors Display

    def __init__(self, master: Optional[tk.Frame] = None,
                 verbose: bool = False, debug: bool = False):
        # Initialize tk.Frame
        super().__init__(master)
        self.master = master

        self.verbose = verbose
        self.debug = debug

        self.enable = tk.IntVar()
        self.enable.set(0)
        self.check = ttk.Checkbutton(
            self,
            text="Median Filter",
            variable=self.enable,
            onvalue=1,
            offvalue=0,
            command=self.callback
        )
        self.check.configure(state=tk.DISABLED)

        # Frame to contain Spinbox and Label
        self.frame = ttk.Frame(
            self
        )

        self.var = tk.StringVar()
        self.var.set(3)
        self.spinbox = ttk.Spinbox(
            self.frame,
            from_=3,
            to=13,
            values=(3, 5, 7, 9, 11, 13),
            textvariable=self.var,
            command=self.callback,
            wrap=False,
            width=4
        )
        self.spinbox.configure(state=tk.DISABLED)

        self.label = ttk.Label(
            self.frame,
            text="Neighbors"
        )
        self.label.configure(state=tk.DISABLED)

    def grid(self, column: int = 0, row: int = 0, columnspan: int = 1, rowspan: int = 1):
        super().grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=tk.EW)
        self.check.grid(column=0, row=0, padx=(18, 0))
        self.frame.grid(column=1, row=0, padx=(12, 0))
        self.spinbox.pack(side=tk.LEFT)
        self.label.pack(side=tk.LEFT, padx=(10, 0))

    def pack(self, side=tk.LEFT):
        self.check.pack(side=side)
        self.frame.pack(side=side)
        self.spinbox.pack(side=tk.LEFT)
        self.label.pack(side=tk.LEFT, padx=(12, 0))

    def set(self, value=0, state=tk.DISABLED):
        if value is not None:
            self.enable.set(value)
        else:
            value = self.enable.get()
        if state is not None:
            self.check.config(state=state)
            if value == 0:
                state = tk.DISABLED
            self.label.config(state=state)
            self.spinbox.config(state=state)

    def clear(self):
        self.set(0, tk.DISABLED)

    def callback(self):
        app = self.master
        original_img = app.open.img

        if self.enable.get() == 1:
            self.label.config(state=tk.NORMAL)
            self.spinbox.config(state=tk.NORMAL)
            self.process()
            app.thresh.make_distance_img()
            if app.thresh.enable.get() == 1:
                app.thresh.process()
            else:
                app.thresh.dist_img = []
        else:
            self.label.config(state=tk.DISABLED)
            self.spinbox.config(state=tk.DISABLED)
            app.img = original_img
            app.thresh.make_distance_img()
            if app.thresh.enable.get() == 1:
                app.thresh.process()
            else:
                app.canvas.update_img(app.img)

    def process(self):
        app = self.master

        M = int(self.var.get())
        print('Median Filter:\t', M, 'x', M)

        app.set_busy_state(True)

        app.img = median_filter(app.open.img, size=(M, M, 1))

        if not app.thresh.enable.get():
            app.canvas.update_img(app.img)
            app.set_busy_state(False)
