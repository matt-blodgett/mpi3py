import tkinter as tk
from . import ui
from mpi3 import medialib


def initiate_interface():
    root = MainRoot()
    root.initiate()
    root.mainloop()


class MainRoot(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-alpha', 0.0)
        self.minsize(width=800, height=480)
        self.resizable(False, False)
        # self.overrideredirect(True)
        self.grid_propagate(False)

    def initiate(self):
        self._layout()
        self.center()
        self.update()
        self.focus_force()
        self.attributes('-alpha', 1.0)

    def center(self):
        self.update()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        rw, rh = self.winfo_width(), self.winfo_height()
        x = str(max(0, int((sw-rw)/2)))
        y = str(max(0, int((sh-rh)/2)))
        self.geometry('+{}+{}'.format(x, y))

    def _layout(self):
        self.frm_interface = ui.RaspiInterface(self)
        self.frm_interface.grid(row=0, column=0, sticky=tk.NSEW)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frm_interface.frm_media.initiate()
        self.frm_interface.frm_taskbar.btn7.bind('<ButtonRelease-1>', lambda e: self.destroy())
