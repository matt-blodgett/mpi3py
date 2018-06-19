import tkinter as tk
from mpi3pi import gui
from mpi3 import playback


class VolumeControl(tk.Canvas):

    def __init__(self, master):
        tk.Canvas.__init__(self, master)

        self.config(bg='#000000')
        self.config(borderwidth=0)
        self.config(highlightthickness=0)

    def initiate(self):
        self.update()

        w, h = self.winfo_width(), self.winfo_height()
        self.btn_volumeup = tk.Button(self)
        self.btn_volumedown = tk.Button(self)
        self.slider = VolumeSlider(self)

        self.btn_volumeup.config(text='+')
        self.btn_volumedown.config(text='-')

        self.create_window((0, 0), width=60, height=60, anchor=tk.NW, window=self.btn_volumeup)
        self.create_window((0, 60), width=60, height=300, anchor=tk.NW, window=self.slider)
        self.create_window((0, h-60), width=60, height=60, anchor=tk.NW, window=self.btn_volumedown)

        self.update()
        self.slider.update_callback = self.pcall
        self.slider.set_colours(trough='#7197e2', shade='#aac7ff')
        self.slider.set_maximum(100)
        self.slider.draw((60, 300))

        self.btn_volumeup.bind('<ButtonRelease-1>', lambda e: self.slider.tick(5))
        self.btn_volumedown.bind('<ButtonRelease-1>', lambda e: self.slider.tick(-5))

    def pcall(self, tick, event):
        # print(tick)
        pass


class VolumeSlider(tk.Canvas):

    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        self.config(highlightthickness=0, bd=0)

        self._tick_curr = 0
        self._tick_max = 0
        self._h_cursor = None
        self._h_height = None
        self._x_trough = None

        self._fill = {
            'trough': '#000000',
            'shade': '#000000'
        }

    def draw(self, dimensions):
        width, height = dimensions
        self.config(width=width, height=height)

        self._h_cursor = (height/100) * 7
        self._h_height = height - self._h_cursor

        w_ratio, w_trough = width/100, 30
        self._x_trough = w_ratio*w_trough, w_ratio*(100-w_trough)

        coords = 0, 0, width, height-1
        self.create_rectangle(*coords, fill=self._fill['trough'], outline='')

        self._indicator_image = gui.tkpil.slider_indicator((width, int(self._h_cursor)))
        self._indicator = self.create_image((0, 0), image=self._indicator_image, anchor=tk.NW)

        self.bind('<ButtonPress-1>', self._draw_cursor)
        self.bind('<ButtonRelease-1>', self._draw_cursor)
        self.bind('<B1-Motion>', self._draw_cursor)

    def update_callback(self, tick, event):
        pass

    def set_colours(self, trough=None, shade=None):
        if trough: self._fill['trough'] = trough
        if shade: self._fill['shade'] = shade

    def set_maximum(self, max_tick):
        self._tick_max = max_tick

    def tick(self, tick, increment=True):
        if increment: self._tick_curr += tick
        else: self._tick_curr = tick
        self._draw_cursor()

    def _draw_cursor(self, event=None):
        if not self._tick_max: return

        if event:
            y_event = event.y-(self._h_cursor/2)
            tick_change = self._tick_max * (1 - (y_event / self._h_height))
            self._tick_curr = int(tick_change)

        self._tick_curr = max(0, min(self._tick_curr, self._tick_max))
        y_draw = self._h_height * (1 - (self._tick_curr/self._tick_max))

        self.delete('shade')
        coords = 0, 0, self.winfo_width(), y_draw
        self.create_rectangle(*coords, tags='shade', fill=self._fill['shade'], outline='')
        self.coords(self._indicator, (0, y_draw))

        self.update_callback(self._tick_curr, event)


class PlaybackInterface(gui.tkit.Mpi3Frame):

    def __init__(self, master):
        gui.tkit.Mpi3Frame.__init__(self, master)

        self.frm_pbdisplay = PlaybackDisplay(self)
        self.frm_pbcontrol = PlaybackControl(self)

        self.frm_pbdisplay.grid(row=0, column=0, sticky=tk.NSEW)
        self.frm_pbcontrol.grid(row=1, column=0, sticky=tk.NSEW)

        self.grid_rowconfigure(0, weight=1)


class PlaybackControl(gui.tkit.Mpi3Frame):

    def __init__(self, master):
        gui.tkit.Mpi3Frame.__init__(self, master)

        self.config(bg='#f2c1ec')
        self.config(width=680, height=160)  # 90 for next/prev 70 for seek
        self.grid_propagate(False)


class PlaybackDisplay(gui.tkit.Mpi3Frame):

    def __init__(self, master):
        gui.tkit.Mpi3Frame.__init__(self, master)
