#!/usr/bin/python3

# # Imports # #
from typing import Optional
import tkinter as tk
from tkinter import ttk
import numpy as np

import os
from traceback import format_exc
from tkinter import filedialog as fd
from matplotlib.image import imread


class OpenUI(tk.Frame):
    verbose: bool
    debug: bool

    img: Optional[np.array]  # Original Image
    button: ttk.Button  # Open File Dialog
    label: ttk.Label  # Current File Name

    def __init__(self, master: Optional[tk.Frame] = None,
                 verbose: bool = False, debug: bool = False):
        super().__init__(master)
        self.master = master

        self.verbose = verbose
        self.debug = debug

        self.button = ttk.Button(
            self,
            text='Open Files',
            command=self.select_files
        )

        self.label = ttk.Label(
            self,
            text="No file selected",
            wraplength=100
        )

        # save original image
        self.img = []

    def grid(self, column: int = 0, row: int = 0, columnspan: int = 1, rowspan: int = 1):
        super().grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=tk.EW)
        self.button.grid(column=0, row=0, padx=(18+1, 0))
        self.label.grid(column=1, row=0, padx=(32, 0))

    def pack(self, side=tk.LEFT):
        self.button.pack(side=side)
        self.label.grid(side=side)

    def select_files(self):
        app = self.master

        # File types for system dialog
        file_types = (
            ('All Image Types', '*.jpg'),
            ('All Image Types', '*.png'),
            ('JPEG', '*.jpg'),
            ('PNG', '*.png'),
            ('All files', '*.*')
        )

        try:
            # Invoke system dialog
            if self.verbose or self.debug:
                print('Open File:\t', 'Waiting for System Dialog')
            file_names = fd.askopenfilenames(
                title='Open files',
                initialdir='./',
                filetypes=file_types
            )

            # Load image from file
            if self.verbose or self.debug:
                print('\t\t', 'Loading File')
            self.load_img(file_names[0])

            if self.verbose or self.debug:
                print('\t\t', 'Done!')

        except IndexError:
            if self.debug:
                print(format_exc())
            if self.verbose or self.debug:
                print('\t\t', 'User Canceled')
            # Only reset if no old data exists
            if type(self.img) is list:
                self.label.config(text="No file selected")
                
                # This should all be in app.clear()
                app.canvas.clear()
                app.median.clear()
                app.thresh.clear()
                app.color.clear()
                app.overlay.clear()

    def load_img(self, filename=''):
        app = self.master

        print('\t\t', filename)
        try:
            app.img = imread(filename)
            if app.img.dtype == np.float64 or app.img.dtype == np.float32:
                if self.verbose or self.debug:
                    print('\t\t', 'Converting to uint8')
                app.img = 255.0 * app.img
                app.img = app.img.astype(np.uint8)

            if self.debug:
                print(app.img)
                print(type(app.img))
                print(app.img.dtype)
            self.img = np.copy(app.img)
            app.canvas.update_img(app.img)
            if self.verbose or self.debug:
                print('\t\t', app.img.shape)
            self.label.config(text=os.path.basename(os.path.realpath(filename)))
            app.median.set(0, tk.NORMAL)
            app.thresh.set(0, tk.NORMAL)
            app.color.set(tk.NORMAL, tk.NORMAL)
            app.overlay.set(0, tk.NORMAL)
            # reset_color_oval()
        except OSError:
            if self.debug:
                print(format_exc())
            if self.verbose or self.debug:
                print('\t\t', 'Unable to open file')

            # Only reset if no old data exists
            if type(self.img) is list:
                self.label.config(text="No file selected")
                
                # This should all be in app.clear()
                app.canvas.clear()
                app.median.clear()
                app.thresh.clear()
                app.color.clear()
                app.overlay.clear()
                
            # Should add message box warning when file open fails
