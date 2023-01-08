#!/usr/bin/python3

# # Imports # #
from typing import Optional
import tkinter as tk
from tkinter import ttk
import numpy as np


class ThresholdUI(tk.Frame):
    """UI for applying threshold"""
    verbose: bool
    debug: bool

    thresh_img: np.array  # Bool Image
    dist_img: np.array  # RGB Distance Values

    enable: tk.IntVar  # Threshold Flag
    check: ttk.Checkbutton  # Toggle Threshold
    frame: tk.Frame  # Threshold Cutoff Frame
    slider: ttk.Scale  # Threshold Cutoff Slider
    var: tk.DoubleVar  # self.slider Value
    entry: ttk.Entry  # Threshold Cutoff Display

    def __init__(self, master: Optional[tk.Frame] = None,
                 verbose: bool = False, debug: bool = False):
        # Initialize tk.Frame
        super().__init__(master)
        self.master = master

        self.verbose = verbose
        self.debug = debug

        # Initialize image data
        self.thresh_img = np.empty(0)
        self.dist_img = np.empty(0)

        # Initialize Widgets
        self.enable = tk.IntVar()
        self.enable.set(0)
        self.check = ttk.Checkbutton(
            self,
            text="Threshold",
            variable=self.enable,
            onvalue=1,
            offvalue=0,
            command=self.check_callback
        )
        self.check.configure(state=tk.DISABLED)

        self.frame = ttk.Frame(
            self
        )

        self.var = tk.DoubleVar()
        self.var.set(0.0)
        self.slider = ttk.Scale(
            self.frame,
            variable=self.var,
            from_=0,
            to=1,
            orient=tk.HORIZONTAL,
            command=self.slider_callback
        )
        self.slider.bind('<ButtonRelease-1>', self.slider_released)
        self.slider.configure(state=tk.DISABLED)

        self.entry = ttk.Entry(
            self.frame,
            # Need to validate input:
            # https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter/4140988#4140988
            # command=entry_callback,
            width=6
        )
        self.entry.insert(0, '0.00')
        self.entry.configure(state=tk.DISABLED)

    def grid(self, column: int = 0, row: int = 0, columnspan: int = 1, rowspan: int = 1):
        super().grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=tk.EW)
        self.check.grid(column=0, row=0, padx=(18, 0))
        self.slider.pack(side=tk.LEFT)
        self.entry.pack(side=tk.LEFT, padx=(4, 0))
        self.frame.grid(column=1, row=0, padx=(6, 6))

    def pack(self, side: str = tk.LEFT):
        super().pack(side=side)
        self.check.pack(side=tk.LEFT)
        self.slider.pack(side=tk.LEFT)
        self.entry.pack(side=tk.LEFT, padx=(4, 0))
        self.frame.pack(side=tk.LEFT, padx=(6, 6))

    def set(self, value: Optional[int] = 0, state: str = tk.DISABLED):
        """Set value and state of widgets"""
        if value is not None:
            self.enable.set(value)
        else:
            value = self.enable.get()
        if state is not None:
            self.check.config(state=state)
            if value == 0:
                state = tk.DISABLED
            self.entry.config(state=state)
            self.slider.config(state=state)

    def clear(self):
        """Reset widgets to default state"""
        self.set(0, tk.DISABLED)

    def check_callback(self):
        """Process image based on Enable flag"""
        app = self.master

        if self.enable.get() == 1:
            self.slider.config(state=tk.NORMAL)
            self.entry.config(state=tk.NORMAL)
            self.make_distance_img()
            self.process()
        else:
            self.slider.config(state=tk.DISABLED)
            self.entry.config(state=tk.DISABLED)
            if app.median.enable.get() == 1:
                # process_median()
                pass
            else:
                app.img = app.open.img
                self.make_distance_img()
            app.canvas.update_img(app.img)

    def slider_callback(self, value: str):
        """Updates value displayed in Entry"""
        self.entry.delete(0, 'end')
        self.entry.insert(0, f'{float(value):.2f}')

    def slider_released(self, event):
        """Process image using new value"""
        self.var.set(round(self.var.get(), 2))
        if self.debug:
            print("Slider Release:", event)
            print("Released value = " + str(self.var.get()))
        self.process()

    def process(self):
        """Preforms Thresholding and calculates Percent"""
        app = self.master

        threshold = self.var.get()

        if self.verbose or self.debug:
            print('Threshold:\t', threshold)
        app.set_busy_state(True)

        img_n = self.dist_img / 255.0
        self.thresh_img = img_n >= threshold
        percent = self.thresh_img.sum() / self.thresh_img.size * 100.0
        if self.verbose or self.debug:
            print('\t\t', 'Percent =', percent)
        app.percent.label[1].config(text=str(round(percent, 2)) + ' %')
        app.canvas.update_img(self.thresh_img)

        app.set_busy_state(False)

    def make_distance_img(self):
        """Calculate RGB distance to be thresholded"""
        # Add an enum for different color spaces as input arg!!!
        app = self.master

        # get rgb value from entry
        color = list()
        for rgb in app.color.rgb[:]:
            color.append(int(rgb.entry.get()))
        # print(color)
        if self.verbose or self.debug:
            print('RGB Distance:\t', color)
        app.set_busy_state(True)
        r = app.img[:, :, 0].astype(int) - color[0]
        g = app.img[:, :, 1].astype(int) - color[1]
        b = app.img[:, :, 2].astype(int) - color[2]
        self.dist_img = 255.0 - ((r * r + g * g + b * b) ** 0.5) / (3 ** 0.5)

        self.dist_img = self.dist_img.astype(np.uint8)

        app.set_busy_state(False)
