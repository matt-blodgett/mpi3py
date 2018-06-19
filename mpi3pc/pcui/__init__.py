import logging
import tkinter as tk
from mpi3pc import gui
from mpi3 import settings
from . import libui
from . import pbui


def initiate_interface():
    root = HiddenRoot()
    main = MainRoot(root)

    def show(event):
        main.deiconify()
        root.iconify()

    root.protocol('WM_DELETE_WINDOW', main.exit)
    root.bind('<Map>', show)
    root.iconify()
    main.initiate()
    gui.initiate()
    root.mainloop()


class HiddenRoot(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-alpha', 0.0)
        self.wm_iconbitmap(gui.icon('mario', '.ico'))


class MainRoot(gui.tktop.WindowToplevel):

    def __init__(self, master):
        gui.tktop.WindowToplevel.__init__(self, master)
        self.frm_playback = pbui.PlaybackManager(self)
        self.frm_libtree = libui.LibraryManager(self)
        self.minsize(750, 300)

    def initiate(self):
        self.attributes('-alpha', 0.0)
        logging.getLogger('MPI3').info('Initialize MainRoot')

        self._layout()
        self.frm_playback.initiate()
        self.frm_libtree.initiate()
        libui.main_menu(self.border_top.menu)

        self.update()
        self.focus_force()
        self.attributes('-alpha', 1.0)
        self.frm_libtree.load()

        # print(list(self.border_top.menu.children)[0])

    def center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        rw, rh = self.winfo_width(), self.winfo_height()
        x = str(max(0, int((sw-rw)/2)))
        y = str(max(0, int((sh-rh)/2)))
        self.geometry('+{}+{}'.format(x, y))

    def exit(self):
        logging.getLogger('MPI3').info('Begin Exit Protocol')
        self.save()
        self.master.destroy()

    def save(self):
        logging.getLogger('MPI3').info('Save Root Dimensions')
        settings['ROOT']['DIMENSIONS'] = self.winfo_width(), self.winfo_height()
        self.frm_libtree.save()

    def report_callback_exception(self, exc, val, tb):
        logging.getLogger('MPI3').exception('Callback Exception')

    def _layout(self):
        w, h = settings['ROOT']['DIMENSIONS']
        self.border_top.grid(row=0, column=0, sticky=tk.NSEW)
        self.frm_playback.grid(row=1, column=0, sticky=tk.NSEW)
        self.frm_libtree.grid(row=2, column=0, sticky=tk.NSEW)
        self.border_bottom.grid(row=3, column=0, sticky=tk.NSEW)
        self.frm_playback.grid(padx=2)
        self.frm_libtree.grid(padx=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.config(width=w, height=h)
        self.grid_propagate(False)
        self.center()
