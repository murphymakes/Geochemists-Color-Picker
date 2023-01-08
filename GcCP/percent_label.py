#!/usr/bin/python3

# # Imports # #
from typing import Optional, List
import tkinter as tk
from tkinter import ttk


class Percent(tk.Frame):
    """Labels to show percent result"""
    label: List[ttk.Label]
    
    def __init__(self, master: Optional[tk.Frame] = None):
        super().__init__(master)
        self.master = master

        self.label = []
        self.label.append(ttk.Label(
            self,
            text="Percent:",
            anchor=tk.E,
            width=12
        ))
        self.label.append(ttk.Label(
            self,
            text="0.0%",
            anchor=tk.W,
            width=12
        ))

    def grid(self, column: int = 0, row: int = 0, columnspan: int = 1, rowspan: int = 1):
        super().grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)
        self.label[0].grid(column=0, row=0)
        self.label[1].grid(column=1, row=0)

    def pack(self, side: str = tk.LEFT):
        super().pack(side=side)
        self.label[0].pack(side=tk.LEFT)
        self.label[1].pack(side=tk.LEFT)
