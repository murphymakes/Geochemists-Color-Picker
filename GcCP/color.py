#!/usr/bin/python3

# # TO DO # #
# Move Color Oval to Canvas (decouple)
# Return color data to main app (decouple)

# # Imports # #
from typing import Optional, List
import tkinter as tk
from tkinter import ttk
import numpy as np


class Color(tk.Frame):
    """Subclass with Entry and Label for R,G, and B in Color UI"""
    entry: ttk.Entry
    label: ttk.Label
    
    def __init__(self, master: Optional[tk.Frame] = None, value: int = 255, label: str = ''):
        super().__init__(master)
        self.master = master

        self.entry = ttk.Entry(
            self,
            width=6
        )
        self.entry.insert(0, "{:.0f}".format(round(value)))

        self.label = ttk.Label(
            self,
            text=label
        )
        
    def grid(self, column: int = 0, row: int = 0, columnspan: int = 1, rowspan: int = 1):
        super().grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)
        self.entry.grid(column=1, row=0)
        self.label.grid(column=2, row=0)
    
    def pack(self, side: str = tk.LEFT):
        super().pack(side=side)
        self.entry.pack(side=tk.LEFT)
        self.label.grid(side=tk.LEFT)


class ColorUI(tk.Frame):
    """UI for selecting a color to threshold from"""
    verbose: bool
    debug: bool
    
    enable: bool
    oval: List[int]  # should move to canvas...
    value: np.array  # Array to store RGB value
    button: ttk.Button  # Button to start color picking
    rgb_frame: tk.Frame  # Frame to display RGB values
    rgb: List[Color]  # Widgets for RGB
    canvas: tk.Canvas  # Canvas for drawing selected color
    
    def __init__(self, master: Optional[tk.Frame] = None,
                 verbose: bool = False, debug: bool = False):
        super().__init__(master)
        self.master = master
        
        self.verbose = verbose
        self.debug = debug

        self.enable = False
        self.oval = []
        self.value = np.array([255, 255, 255])

        self.button = ttk.Button(
            self,
            text='Choose Color',
            command=self.toggle
        )
        self.button.config(state=tk.DISABLED)

        self.rgb_frame = tk.Frame(
            self
        )

        self.rgb = []
        
        self.rgb.append(Color(
            master=self.rgb_frame,
            value=255,
            label='R'
        ))
        self.rgb.append(Color(
            master=self.rgb_frame,
            value=255,
            label='G'
        ))
        self.rgb.append(Color(
            master=self.rgb_frame,
            value=255,
            label='B'
        ))

        self.canvas = tk.Canvas(
            self.rgb_frame,
            width=50,
            height=50
        )

        self.draw_rect([255, 255, 255])

    def grid(self, column: int = 0, row: int = 0, columnspan: int = 1, rowspan: int = 1):
        super().grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=tk.EW)
        self.button.grid(column=0, row=0, rowspan=rowspan, padx=(18+1, 0))
        self.rgb_frame.grid(column=1, row=0, rowspan=rowspan, padx=(18, 0))
        
        self.canvas.grid(column=0, row=0, rowspan=rowspan, padx=(0, 4))
        for row, rgb in enumerate(self.rgb):
            rgb.grid(column=1, row=row)

    def pack(self, side: str = tk.LEFT):
        super().pack(side=side)
        self.button.pack(side=tk.LEFT)
        self.rgb_frame.pack(side=tk.LEFT)
        
        self.canvas.pack(side=tk.LEFT, padx=(0, 4))
        for row, rgb in enumerate(self.rgb):
            rgb.grid(column=1, row=row)

    def set(self, button: Optional[str] = tk.DISABLED, state: Optional[str] = tk.NORMAL):
        """Set value and state of widgets"""
        if button is not None:
            self.button.config(state=button)
        if state is not None:
            for rgb in self.rgb:
                rgb.entry.config(state=state)

    def clear(self):
        """Reset widgets to default state"""
        self.set(tk.DISABLED, tk.NORMAL)

    def toggle(self):
        """Toggles Enable flag for enabling/disabling color selection on canvas"""
        app = self.master

        if self.enable:
            self.enable = False
        else:
            self.enable = True
            self.set(button=tk.DISABLED, state=None)
            app.canvas.update_img(app.img)  # need to change to app.update_img
            if self.verbose or self.debug:
                print('Color Selector:\t', 'Enabled')

    def reset_oval(self):  # Maybe color oval should be in canvas???
        """Clears Color Selection Oval from canvas and underlying data"""
        app = self.master

        if len(self.oval) > 0:
            app.canvas.delete(self.oval[0])
            self.oval = []

    def draw_rect(self, color: List[int]):
        """Draw selected color over canvas"""
        # clear canvas
        self.canvas.delete('all')
        
        # make hex string
        hex_color = '#'
        for rgb in color:
            value = self.clamp(0, int(rgb), 255)
            hex_rgb = hex(value)[2:]
            if len(hex_rgb) < 2:
                hex_color += '0'
            hex_color += hex_rgb
        
        # draw
        self.canvas.create_rectangle(0, 0, 50, 50, fill=hex_color)
    
    @staticmethod
    def clamp(minimum: int, x: int, maximum: int) -> int:
        """Bounds int x between a minimum and maximum"""
        return max(minimum, min(x, maximum))
