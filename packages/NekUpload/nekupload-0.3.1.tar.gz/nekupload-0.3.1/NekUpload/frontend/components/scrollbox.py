import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ScrolledListbox(ttk.Frame):
    def __init__(self,parent):
        super().__init__(
            master=parent
        )

        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)

        self._listbox = tk.Listbox(self,selectmode=EXTENDED)
        scrollbar_y= ttk.Scrollbar(self,command=self._listbox.yview)
        scrollbar_x = ttk.Scrollbar(self,command=self._listbox.xview,orient=HORIZONTAL)
        self._listbox.config(yscrollcommand=scrollbar_y.set,xscrollcommand=scrollbar_x)
        scrollbar_y.config(command=self._listbox.yview)
        scrollbar_x.config(command=self._listbox.xview)

        self._listbox.grid(row=0,column=0,sticky=(NSEW))
        scrollbar_x.grid(row=1,column=0,sticky=(W,E))
        scrollbar_y.grid(row=0,column=1,sticky=(N,S,W))

    @property
    def listbox(self):
        return self._listbox