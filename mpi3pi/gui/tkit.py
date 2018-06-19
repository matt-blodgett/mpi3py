import tkinter as tk


class Mpi3Frame(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(borderwidth=0)
        self.config(highlightthickness=0)


class Mpi3Button(tk.Label):

    def __init__(self, master):
        tk.Label.__init__(self, master)
        super().bind('<ButtonRelease-1>', self._on_release)
        self._br1_bindings = []

        self.config(relief=tk.SOLID)
        self.config(borderwidth=1)

    def bind(self, sequence=None, func=None, add=None):
        if sequence == '<ButtonRelease-1>': self._br1_bindings.append(func)
        else: super().bind(sequence=sequence, func=func, add=add)

    def _on_release(self, event):
        x, y, w, h = event.x, event.y, self.winfo_width(), self.winfo_height()
        if not (x < 0 or x > w or y < 0 or y > h):
            for br1 in self._br1_bindings: br1(event)
