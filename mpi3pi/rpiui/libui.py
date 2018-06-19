import tkinter as tk
from mpi3pi import gui


class LibraryInterface(tk.Canvas):

    def __init__(self, master):
        tk.Canvas.__init__(self, master)

        self.config(borderwidth=0)
        self.config(highlightthickness=0)

        self.frm_containers = ContainersInterface(self)
        self.frm_songlist = SongListInterface(self)

        self.create_window((0, 0), width=338, height=420, anchor=tk.NW, window=self.frm_containers)
        self.create_line((339, 0, 339, 420), fill='#000000')
        self.create_window((340, 0), width=338, height=420, anchor=tk.NW, window=self.frm_songlist)
        self.create_line((679, 0, 679, 420), fill='#000000')


class ContainersInterface(gui.tkit.Mpi3Frame):

    def __init__(self, master):
        gui.tkit.Mpi3Frame.__init__(self, master)
        self.config(background='#ffc4a5')

        self.frm_banner = ContainerNavigate(self)
        self.frm_scroll = ContainersScroll(self)

        self.frm_banner.grid(row=0, column=0, sticky=tk.NSEW)
        self.frm_scroll.grid(row=1, column=0, sticky=tk.NSEW)
        self.grid_rowconfigure(1, weight=1)


class ContainersScroll(gui.tkit.Mpi3Frame):

    def __init__(self, master):
        gui.tkit.Mpi3Frame.__init__(self, master)

        self.btn = ContainerDisplay(self, 'Folder')
        self.btn.grid(row=0, column=0, sticky=tk.NSEW)


class SongListInterface(gui.tkit.Mpi3Frame):

    def __init__(self, master):
        gui.tkit.Mpi3Frame.__init__(self, master)
        self.config(background='#ffe3b7')

        self.frm_navigate = SongNavigate(self)

        self.btn = SongDisplay(self, 'Song')

        self.frm_navigate.grid(row=0, column=0, sticky=tk.NSEW)

        self.btn.grid(row=1, column=0, sticky=tk.NSEW)



class RaspiLibraryButton(tk.Canvas):

    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        self.config(background='#FFFFFF')
        self.config(highlightthickness=0)
        self.config(borderwidth=0)
        self.config(height=60)


class ContainerNavigate(RaspiLibraryButton):

    def __init__(self, master):
        RaspiLibraryButton.__init__(self, master)

        self.config(background='#cedbef')
        self.create_text((30, 30), text='Raspi Library', font=('Helvetica', 11), fill='#000000', anchor=tk.W)
        self.create_line((20, 50, 300, 50), fill='#000000')


class ContainerDisplay(RaspiLibraryButton):

    def __init__(self, master, container):
        RaspiLibraryButton.__init__(self, master)

        container = '123456789abcdefghijklmnopqrstuvwxyz123456789'

        if len(container) > 35:
            container = container[:32] + '...'

        self.create_rectangle((6, 6, 54, 54), fill='#000000', outline='')
        self.create_text((60, 30), text=container, font=('Helvetica', 11), fill='#000000', anchor=tk.W)


class SongNavigate(RaspiLibraryButton):

    def __init__(self, master):
        RaspiLibraryButton.__init__(self, master)


class SongDisplay(RaspiLibraryButton):

    def __init__(self, master, container):
        RaspiLibraryButton.__init__(self, master)

        container = '123456789abcdefghijklmnopqrstuvwxyz123456789'
        self.create_rectangle((6, 6, 54, 54), fill='#000000', outline='')
        self.create_text((60, 30), text=container, font=('Helvetica', 11), fill='#000000', anchor=tk.W)
