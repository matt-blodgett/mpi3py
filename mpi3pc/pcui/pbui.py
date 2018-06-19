import logging
import tkinter as tk
from mpi3pc import gui
from mpi3 import settings
from mpi3 import playback


class PlaybackManager(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.volumebar = VolumeControl(self)
        self.dashboard = PlaybackDashboard(self)
        self.searchbar = SearchBar(self)

        playback.update['song'] = self.dashboard.update_display
        playback.update['position'] = self.dashboard.update_position
        playback.update['volume'] = self.volumebar.update_volume
        playback.update['active'] = self.dashboard.update_active
        playback.update['loaded'] = self.dashboard.initiate_bindings

    def initiate(self):
        self._layout()
        self.dashboard.initiate()
        self.volumebar.initiate()
        self.searchbar.initiate()
        self.set_theme()

        init_vol = settings['PLAYBACK']['INITIALVOLUME']
        self.volumebar.slider.tick(init_vol*100)
        playback.volume_ratio(init_vol)

    def _layout(self):
        self.volumebar.grid(row=0, column=0, sticky=tk.NS + tk.W)
        self.dashboard.grid(row=0, column=1, sticky=tk.NS)
        self.searchbar.grid(row=0, column=2, sticky=tk.NS + tk.E)

        self.volumebar.grid(padx=5, pady=0)
        self.dashboard.grid(padx=5, pady=0)
        self.searchbar.grid(padx=5, pady=0)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.update_idletasks()

    def set_theme(self):
        bg = '#BABABA'
        self.config(background=bg)
        self.volumebar.set_theme(bg)
        self.dashboard.set_theme('#F7F7F7')
        self.searchbar.config(background=bg)


class PlaybackDashboard(tk.Canvas):

    def __init__(self, master, width=400, height=55):
        tk.Canvas.__init__(self, master)
        self.config(width=width, height=height)
        self.config(bd=0, highlightthickness=0)

    def initiate(self):
        self._layout()
        self._animate()

    def initiate_bindings(self, initiated):
        if not self.btn_playpaus.fade:
            self.bind('<Motion>', self._on_motion)
            self.bind('<ButtonPress-1>', self._on_press)
            self.btn_playpaus.bind('<ButtonPress-1>', self._on_press)
            self.btn_playpaus.bind('<ButtonRelease-1>', self._on_release)
            self.btn_next.bind('<ButtonRelease-1>', lambda e: playback.play_next())
            self.btn_prev.bind('<ButtonRelease-1>', lambda e: playback.play_prev())
            self.slider.bind('<ButtonPress-1>', lambda e: playback.pause(), add=True)
            self.slider.update_callback = self.update_time

            self.btn_playpaus.fade = True
            self.btn_playpaus.set_icon(self.icn_paus)
            self.btn_playpaus.start_fade()

    def _on_release(self, event):
        if playback.active: playback.pause()
        else: playback.unpause()

    def _on_motion(self, event):
        if event.y < self.bbox(self.wnd_playpaus)[3]:
            self._show_playpaus(event)

    def _on_press(self, event=None):
        self._show_playpaus(event)

    def _show_playpaus(self, event=None):
        si = self.btn_playpaus.set_icon

        if str(event.type) == 'Motion':
            si(self.icn_paus) if playback.active else si(self.icn_play)
            self.itemconfig(self.wnd_playpaus, state=tk.NORMAL)
        else:
            si(self.icn_play) if playback.active else si(self.icn_paus)

    def _animate(self):
        if playback.active:
            self.slider.tick(1000)
            self.after(1000, self._animate)

        #
        # MASSIVE PERFORMANCE ISSUE
        #
        # a = 1000 if playback.active else 1
        # self.after(a, self._animate)
        #

    def update_display(self, song):
        logging.getLogger('MPI3').info('Play File: {}'.format(song.path))
        self.itemconfig(self.lbl_name, text=song.name)
        self.itemconfig(self.lbl_artist, text=song.artist)
        self.itemconfig(self.lbl_total, text=song.f_time)
        self.slider.set_maximum(song.time)

    def update_position(self, pos):
        self.slider.tick(pos, False)

    def update_active(self, active):
        pass

    def update_time(self, time, event):
        if event:
            if str(event.type) == 'ButtonRelease':
                playback.unpause(time)

        if time == playback.song.time:
            curr_time = playback.song.f_time
            playback.play_next()
        else:
            m, s = divmod(time / 1000, 60)
            curr_time = '%2d:%02d' % (m, s)

        self.itemconfig(self.lbl_currpos, text=curr_time)

    def _layout(self):
        w_unit = self.winfo_width() / 20
        h_unit = self.winfo_height() / 20

        def w_pos(units):
            return int(w_unit*units)

        def h_pos(units):
            return int(h_unit*units)

        def pos(wu, hu):
            return int(w_unit*wu), int(h_unit*hu)

        self.lbl_name = self.create_text(pos(10, 5), font=(gui.font(10, 'bold')))
        self.lbl_artist = self.create_text(pos(10, 10), font=gui.font(8))
        self.lbl_currpos = self.create_text((w_pos(4)+2, h_pos(12)), font=gui.font(9))
        self.lbl_total = self.create_text((w_pos(16)-2, h_pos(12)), font=gui.font(9))

        self.slider = gui.tkit.Slider(self)
        self.slider.draw(pos(13, 3), '#BCBCBC')

        self.icn_play = gui.icon('play')
        self.icn_paus = gui.icon('paus')
        self.btn_playpaus = gui.tkit.HoverFadeButton(self)
        self.btn_prev = gui.tkit.Mpi3ButtonIcon(self)
        self.btn_next = gui.tkit.Mpi3ButtonIcon(self)
        self.btn_playpaus.set_icon(self.icn_play)
        self.btn_playpaus.draw(pos(14, 14))
        self.btn_prev.config(width=w_pos(3), height=h_pos(21))
        self.btn_next.config(width=w_pos(3), height=h_pos(21))
        self.btn_prev.set_icon(gui.icon('prev'))
        self.btn_next.set_icon(gui.icon('next'))
        self.btn_prev.set_theme('#D8D8D8', True)
        self.btn_next.set_theme('#D8D8D8', True)

        wnd_play = self.create_window(pos(10, 8), window=self.btn_playpaus)
        wnd_next = self.create_window(pos(20, 0), window=self.btn_next)
        wnd_prev = self.create_window(pos(0, 0), window=self.btn_prev)
        wnd_slid = self.create_window(pos(10, 17), window=self.slider)

        self.wnd_playpaus = wnd_play
        self.itemconfig(wnd_play, anchor=tk.CENTER, width=w_pos(14), height=h_pos(14))
        self.itemconfig(wnd_next, anchor=tk.NE, width=w_pos(3), height=h_pos(21))
        self.itemconfig(wnd_prev, anchor=tk.NW, width=w_pos(3), height=h_pos(21))
        self.itemconfig(wnd_slid, anchor=tk.CENTER, width=w_pos(13), height=h_pos(3))

        self.itemconfig(self.lbl_currpos, text='0:00')
        self.itemconfig(self.lbl_total, text='0:00')
        self.itemconfig(self.wnd_playpaus, state=tk.NORMAL)

        self.btn_playpaus.window_id = self.wnd_playpaus

    def set_theme(self, bg):
        self.config(background=bg)
        self.slider.config(background=bg)
        self.btn_playpaus.config(background=bg)


class VolumeControl(tk.Canvas):

    def __init__(self, master, width=150, height=55):
        tk.Canvas.__init__(self, master, width=width, height=height)
        self.config(bd=0, highlightthickness=0)

    def initiate(self):
        self._layout()

        def volume_change(tick, event):
            playback.volume_ratio(tick / 100)

        self.slider.update_callback = volume_change
        self.slider.set_scrollable(True)

    def update_volume(self, volume):
        self.lbl_volume.config(text=str(int(volume*100)))

    def _layout(self):
        w = self.winfo_width() / 20
        h = self.winfo_height() / 20

        w_label, h_label = (w*3), (h*3)
        dim_slider = (w*15), (h*4)
        pos_slider = ((w*9), (h*10))
        pos_label = ((w*18)+2, (h*10))

        self.lbl_volume = tk.Label(self)
        self.lbl_volume.config(font=gui.font(8))

        self.slider = gui.tkit.Slider(self)
        self.slider.draw(dim_slider, '#686868')
        self.slider.set_maximum(100)

        wnd_slide = self.create_window(pos_slider, window=self.slider)
        wnd_label = self.create_window(pos_label, window=self.lbl_volume)

        self.itemconfig(wnd_slide, width=(w*15), height=(h*4))
        self.itemconfig(wnd_label, width=w_label, height=h_label)

    def set_theme(self, bg):
        self.config(background=bg)
        self.slider.config(background=bg)
        self.lbl_volume.config(background=bg)


class SearchBar(tk.Frame):

    def __init__(self, master, width=150, height=55):
        tk.Frame.__init__(self, master, width=width, height=height)
        self.container = tk.Frame(self, bd=0, highlightthickness=0)
        self.btn_search = gui.tkit.Mpi3ButtonIcon(self.container)
        self.box_search = tk.Entry(self.container)

    def initiate(self):
        self._layout()

    def _layout(self):
        self.box_search.config(relief='flat')
        self.btn_search.set_theme('#FFFFFF', True)
        self.btn_search.set_icon(gui.icon('search'))
        self.box_search.config(width=18)

        self.btn_search.grid(row=0, column=0, sticky=tk.NSEW)
        self.box_search.grid(row=0, column=1, sticky=tk.NSEW)

        self.container.grid(row=0, column=0, sticky=tk.EW)
        self.container.grid(padx=5)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
