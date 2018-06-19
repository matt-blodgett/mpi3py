import tkinter as tk
from mpi3pi import gui
from . import libui
from . import pbui


class RaspiInterface(tk.Canvas):

    def __init__(self, master):
        tk.Canvas.__init__(self, master)

        self.config(borderwidth=0)
        self.config(highlightthickness=0)

        self.frm_taskbar = Taskbar(self)
        self.frm_media = MediaInterface(self)

        self.create_window((0, 0), width=800, height=59, anchor=tk.NW, window=self.frm_taskbar)
        self.create_window((0, 60), width=800, height=420, anchor=tk.NW, window=self.frm_media)
        self.create_line((0, 59, 800, 59), fill='#000000')

        self.frm_taskbar.btn1.bind('<ButtonRelease-1>', lambda e: self.frm_media.view_library())
        self.frm_taskbar.btn2.bind('<ButtonRelease-1>', lambda e: self.frm_media.view_playback())


class Taskbar(gui.tkit.Mpi3Frame):

    def __init__(self, master):
        gui.tkit.Mpi3Frame.__init__(self, master)

        # self.config(cursor='None')

        self.btn1 = gui.tkit.Mpi3Button(self)
        self.btn2 = gui.tkit.Mpi3Button(self)
        self.btn3 = gui.tkit.Mpi3Button(self)
        self.btn4 = gui.tkit.Mpi3Button(self)
        self.btn5 = gui.tkit.Mpi3Button(self)
        self.btn6 = gui.tkit.Mpi3Button(self)
        self.btn7 = gui.tkit.Mpi3Button(self)

        self.btn1.config(text='BTN1')
        self.btn2.config(text='BTN2')
        self.btn3.config(text='BTN3')
        self.btn4.config(text='BTN4')
        self.btn5.config(text='BTN5')
        self.btn6.config(text='BTN6')
        self.btn7.config(text='BTN7')

        w = 10
        self.btn1.config(width=w)
        self.btn2.config(width=w)
        self.btn3.config(width=w)
        self.btn4.config(width=w)
        self.btn5.config(width=w)
        self.btn6.config(width=w)
        self.btn7.config(width=w)

        self.grid_rowconfigure(0, weight=1)
        self.btn1.grid(row=0, column=0, sticky=tk.NSEW)
        self.btn2.grid(row=0, column=1, sticky=tk.NSEW)
        self.btn3.grid(row=0, column=2, sticky=tk.NSEW)
        self.grid_columnconfigure(4, weight=1)
        self.btn4.grid(row=0, column=5, sticky=tk.NSEW)
        self.btn5.grid(row=0, column=6, sticky=tk.NSEW)
        self.btn6.grid(row=0, column=7, sticky=tk.NSEW)
        self.btn7.grid(row=0, column=8, sticky=tk.NSEW)


class MediaInterface(tk.Canvas):

    def __init__(self, master):
        tk.Canvas.__init__(self, master)

        self.config(background='#000000')
        self.config(borderwidth=0)
        self.config(highlightthickness=0)

        self.frm_panel = gui.tkit.Mpi3Frame(self)
        self.frm_volume = pbui.VolumeControl(self)
        self.frm_playback = pbui.PlaybackInterface(self)
        self.frm_library = libui.LibraryInterface(self)

        self.frm_panel.config(bg='#A1FF91')

        self.wnd_panel = self.create_window((0, 0),  width=60, height=420, anchor=tk.NW, window=self.frm_panel)
        self.wnd_volume = self.create_window((740, 0), width=60, height=420, anchor=tk.NW, window=self.frm_volume)
        self.wnd_playback = self.create_window((60, 0), width=680, height=420, anchor=tk.NW, window=self.frm_playback)
        self.wnd_library = self.create_window((-680, 0), width=680, height=420, anchor=tk.NW, window=self.frm_library)

        self.frm_panel.lift()

        self._w_center = 680
        self._x_slide = None
        self.view_library()

        self.frm_panel.bind('<ButtonPress-1>', self._on_lclick)
        self.frm_panel.bind('<B1-Motion>', self._on_b1_motion)
        self.frm_panel.bind('<ButtonRelease-1>', self._on_release)

    def initiate(self):
        self.frm_volume.initiate()

    def view_library(self):
        self.coords(self.wnd_panel, (self._w_center, 0))
        self.coords(self.wnd_library, (0, 0))
        self.current_view = self.frm_library

    def view_playback(self):
        self.coords(self.wnd_panel, (0, 0))
        self.coords(self.wnd_library, (-self._w_center, 0))
        self.current_view = self.frm_playback

    def _on_lclick(self, event):
        self._x_slide = event.x_root

    def _on_release(self, event):
        x = -(self._x_slide - event.x_root)
        p = self.current_view is self.frm_playback
        w = self._w_center
        self._x_slide = None

        x_panel, x_library = 0, 0

        if p and x == 0:
            x_panel, x_library = w, 0
            self.current_view = self.frm_library

        elif not p and x == 0:
            x_panel, x_library = 0, -w
            self.current_view = self.frm_playback

        elif (p and x > (w/6)) or (not p and x >= -(w/6)):
            x_panel, x_library = w, 0
            self.current_view = self.frm_library

        elif (p and x <= (w/6)) or (not p and x < -(w/6)):
            x_panel, x_library = 0, -w
            self.current_view = self.frm_playback

        self.coords(self.wnd_panel, (x_panel, 0))
        self.coords(self.wnd_library, (x_library, 0))

    def _on_b1_motion(self, event):
        x_offset = -(self._x_slide - event.x_root)
        w_center = self._w_center

        x_view = w_center if self.current_view is self.frm_library else 0

        if w_center + 1 > x_offset + x_view > 0:
            self.coords(self.wnd_panel, (x_offset + x_view, 0))
            self.coords(self.wnd_library, (x_offset + x_view - w_center, 0))

        elif x_offset < 0 - x_view:
            self.coords(self.wnd_panel, (0, 0))
            self.coords(self.wnd_library, (-w_center, 0))

        elif x_offset > w_center - x_view:
            self.coords(self.wnd_panel, (w_center, 0))
            self.coords(self.wnd_library, (0, 0))
