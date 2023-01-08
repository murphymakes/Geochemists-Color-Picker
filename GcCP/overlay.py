#!/usr/bin/python3

# # Imports # #
from typing import Optional
import tkinter as tk
from tkinter import ttk
import numpy as np


class OverlayUI(tk.Frame):
    """UI for adding overlay to processed image for display"""
    verbose: bool
    debug: bool
    
    enable: tk.IntVar  # Overlay Flag
    check: ttk.Checkbutton  # Toggle Overlay
    
    def __init__(self, master: Optional[tk.Frame] = None,
                 verbose: bool = False, debug: bool = False):
        super().__init__(master)
        self.master = master

        self.verbose = verbose
        self.debug = debug
        
        self.enable = tk.IntVar()
        self.enable.set(0)
        self.check = ttk.Checkbutton(
            self,
            text="Overlay",
            variable=self.enable,
            onvalue=1,
            offvalue=0,
            command=self.callback,
            width=8
        )
        self.check.configure(state=tk.DISABLED)

    def grid(self, column=0, row=0, columnspan=1, rowspan=1):
        super().grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=tk.EW)
        self.check.pack(side=tk.LEFT, padx=(18, 0))

    def pack(self, side=tk.LEFT):
        super().pack(side=side)
        self.check.pack(side=tk.LEFT, padx=(0, 3))

    def set(self, value=0, state=tk.DISABLED):
        """Set value and state of widgets"""
        if value is not None:
            self.enable.set(value)
        # else:
            # value = self.enable.get()
        if state is not None:
            self.check.configure(state=state)

    def clear(self):
        """Reset widgets to default state"""
        self.set(value=0, state=tk.DISABLED)

    def callback(self):
        """Update canvas based on enable state"""
        app = self.master

        if app.thresh.enable.get():
            app.canvas.update_img(app.thresh.thresh_img)
        else:
            app.canvas.update_img(app.img)

    def add_overlay(self, img_arr: Optional[np.array] = None):
        """Combine original image with processed image array for display"""
        app = self.master
        original_img = app.open.img

        display_img = original_img

        if img_arr is None:
            return display_img

        if img_arr.dtype == bool:
            if img_arr.ndim == 2:
                # Use threshold array as mask
                # # TO DO # #
                # Maybe more efficient way to do this
                # Try to combine this all into one line, maybe weighted average???
                mask = ~img_arr
                display_img = display_img.astype(np.float64)
                display_img[mask, 0] *= 0.25
                display_img[mask, 1] *= 0.25
                display_img[mask, 2] *= 0.25
                display_img = display_img.astype(np.uint8)
            else:
                # This case should not happen
                print('\n???\n')
        else:
            # Overlay median image with original image
            if img_arr is not original_img and (img_arr != original_img).any():
                display_img = (original_img / 2.0 + img_arr / 2.0).astype(np.uint8)

        return display_img
