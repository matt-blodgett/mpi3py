import tkinter as tk
from mpi3pc import gui


class WindowToplevel(tk.Toplevel):

    def __repr__(self):
        c, m = self.__module__, self.__class__.__name__
        return '<{} {}>'.format(c, m)

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.overrideredirect(True)
        self.config(highlightthickness=0, bd=0)
        self.config(bg='#000000')
        self.border_top = WindowBorderTop(self)
        self.border_bottom = WindowBorderBottom(self)
        self.maximized = None

    def exit(self):
        self.destroy()


class WindowBorderEdge(tk.Canvas):

    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        self.config(bd=0, highlightthickness=0)
        self._border = '#000000'
        self._fade = '#282828'

    def set_orientation(self, top):
        if top: self._border, self._fade = self._fade, self._border
        self.bind('<Configure>', self._on_configure)

    def _on_configure(self, event):
        self._draw_lines()

    def _draw_lines(self):
        self.delete('gradient')
        w, h = self.winfo_width(), self.winfo_height()

        limit = int(h)
        for y in range(limit):
            colour = gui.tkpil.mix_hex(self._border, self._fade, limit, y - 1)
            self.create_line(0, y, w, y, tags='gradient', fill=colour)
        self.tag_lower('gradient')


class WindowBorder(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(bg='#000000')

        self.edge = WindowBorderEdge(self)
        self.edge.config(height=10)

        self.stretch = tk.Frame(self)
        self.stretch.config(bg='#000000')

        self._xy_clicked_root = None
        self._xy_window_origin = None

        self.stretch.bind('<Button-1>', self._on_lclick)
        self.stretch.bind('<B1-Motion>', self._on_b1_motion)
        self.stretch.bind('<ButtonRelease>', self._on_release)

        self.edge.bind('<Button-1>', self._on_lclick)
        self.edge.bind('<B1-Motion>', self._on_b1_motion)
        self.edge.bind('<ButtonRelease>', self._on_release)

    def _on_lclick(self, event):
        self._xy_clicked_root = event.x_root, event.y_root
        self._xy_window_origin = (
            self.master.winfo_rootx(), self.master.winfo_rooty())

    def _on_release(self, event):
        self._xy_clicked_root = None
        self._xy_window_origin = None

    def _on_b1_motion(self, event):
        if self.master.maximized is None:
            x_click, y_click = self._xy_clicked_root
            x_origin, y_origin = self._xy_window_origin
            x_event, y_event = event.x_root, event.y_root

            x_offset = -(x_click - x_event)
            y_offset = -(y_click - y_event)

            x_move = x_origin + x_offset
            y_move = y_origin + y_offset

            geometry = '+{}+{}'.format(str(x_move), str(y_move))
            self.master.geometry(geometry)


class WindowBorderBottom(WindowBorder):

    def __init__(self, master):
        WindowBorder.__init__(self, master)

        self.stretch.config(height=5)
        self.edge.set_orientation(False)

        self.sizegrip = tk.ttk.Sizegrip(self)
        self.sizegrip.config(style=gui.MPI3_SIZEGRIP)
        self.stretch.grid(row=0, column=0, sticky=tk.NSEW)
        self.sizegrip.grid(row=0, column=1, sticky=tk.NSEW)
        self.edge.grid(row=1, column=0, sticky=tk.NSEW)
        self.sizegrip.grid(rowspan=2, columnspan=2)
        self.edge.grid(columnspan=2)

        self.grid_columnconfigure(0, weight=1)


class WindowBorderTop(WindowBorder):

    def __init__(self, master):
        WindowBorder.__init__(self, master)

        self.menu = tk.Frame(self)
        self.wbuttons = tk.Frame(self)

        self.edge.set_orientation(True)
        self.menu.config(bg='#000000')
        self.wbuttons.config(bg='#000000')

        self.btn_minimize = gui.tkit.Mpi3ButtonIcon(self.wbuttons)
        self.btn_maximize = gui.tkit.Mpi3ButtonIcon(self.wbuttons)
        self.btn_close = gui.tkit.Mpi3ButtonIcon(self.wbuttons)

        self.btn_minimize.set_icon(gui.icon('minimize'))
        self.btn_maximize.set_icon(gui.icon('maximize'))
        self.btn_close.set_icon(gui.icon('close'))

        self.btn_minimize.config(width=20, height=10)
        self.btn_maximize.config(width=20, height=10)
        self.btn_close.config(width=20, height=10)

        self.btn_minimize.set_theme('#000000', False)
        self.btn_maximize.set_theme('#000000', False)
        self.btn_close.set_theme('#000000', False)

        self.btn_minimize.grid(row=0, column=0, sticky=tk.NSEW)
        self.btn_maximize.grid(row=0, column=1, sticky=tk.NSEW)
        self.btn_close.grid(row=0, column=2, sticky=tk.NSEW)

        self.edge.grid(row=0, column=0, sticky=tk.NSEW)
        self.menu.grid(row=1, column=0, sticky=tk.NSEW)
        self.stretch.grid(row=1, column=1, sticky=tk.NSEW)
        self.wbuttons.grid(row=1, column=2, sticky=tk.NSEW)
        self.edge.grid(rowspan=1, columnspan=3)
        self.menu.grid(padx=2, pady=0)
        self.wbuttons.grid(padx=2, pady=0)

        self.menu.grid_rowconfigure(0, weight=1)
        self.wbuttons.grid_rowconfigure(0, weight=1)
        self.stretch.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.btn_minimize.bind('<ButtonRelease-1>', lambda e: self.master.withdraw())
        self.btn_maximize.bind('<ButtonRelease-1>', lambda e: self.maximize())
        self.btn_close.bind('<ButtonRelease-1>', lambda e: self.master.exit())

    def maximize(self):
        if self.master.maximized is None:
            x, y = self.master.winfo_rootx(), self.master.winfo_rooty()
            w, h = self.master.winfo_width(), self.master.winfo_height()

            self.master.maximized = x, y, w, h
            self.master.overrideredirect(False)
            self.master.state('zoomed')

            w_border = 22
            x, y = self.master.winfo_rootx(), self.master.winfo_rooty() - w_border
            w, h = self.master.winfo_width(), self.master.winfo_height() + w_border

            self.master.state('normal')
            self.master.overrideredirect(True)
            self.btn_maximize.set_icon(gui.icon('demaximize'))
        else:
            x, y, w, h = self.master.maximized
            self.master.maximized = None
            self.btn_maximize.set_icon(gui.icon('maximize'))

        geometry = '{}x{}+{}+{}'.format(str(w), str(h), str(x), str(y))
        self.master.geometry(geometry)
