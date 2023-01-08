#!/usr/bin/python3

# # Imports # #
from typing import Optional
import tkinter as tk
from tkinter import ttk


class Progress(tk.Frame):
    """Label to show processing progress"""
    label: ttk.Label
    
    def __init__(self, master: Optional[tk.Frame] = None):
        super().__init__(master)
        self.master = master

        self.label = ttk.Label(
            self,
            text="Done",
            anchor=tk.W,
            width=12
        )

    def grid(self, column: int = 0, row: int = 0, columnspan: int = 1, rowspan: int = 1) -> None:
        super().grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=tk.EW)
        self.label.pack(side=tk.LEFT, padx=(18, 0))

    def pack(self, side: str = tk.LEFT):
        super().pack(side=side)
        self.label.pack(side=tk.LEFT)
