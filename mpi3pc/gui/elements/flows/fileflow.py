import os
import tkinter as tk
from tkinter import ttk
from mpi3pc.util import fileutil
from mpi3pc import gui


class ImportFiles(tk.Toplevel):

    def __init__(self, songs):
        tk.Toplevel.__init__(self)
        self.resizable(False, False)
        self.title('Import Options')
        self._layout()

        self._songs = songs
        ct = str(len(songs))
        txt = 'Audio Files: ' + ct + ' new songs detected'

        self.lbl_info.config(text=txt)
        self.lbl_info.config(font=('Helvetica', 11))

        self.opt_create.config(style=gui.MPI3_CHECKBUTTON)
        self.opt_delete.config(style=gui.MPI3_CHECKBUTTON)

        self._create = tk.BooleanVar()
        self._delete = tk.BooleanVar()
        self.opt_create.config(variable=self._create)
        self.opt_delete.config(variable=self._delete)
        self.opt_delete.config(state=tk.DISABLED)
        self.btn_continue.config(state=tk.DISABLED)
        self._create.set(False)
        self._delete.set(False)

        self.opt_create.bind('<ButtonRelease-1>', self._on_click)
        self.btn_continue.bind('<ButtonRelease-1>', lambda e: self._continue())
        self.btn_cancel.bind('<ButtonRelease-1>', lambda e: self.destroy())

    def _on_click(self, event):
        if self._create.get(): self._delete.set(False)
        s = tk.DISABLED if self._create.get() else tk.NORMAL
        self.btn_continue.config(state=s)
        self.opt_delete.config(state=s)

    def _continue(self):
        if self._create.get():
            self.withdraw()
            Fileflow(self._songs)
            self._delete.get()
        self.destroy()

    def _close(self, event):
        self.destroy()

    def _layout(self):
        self.frm = tk.Frame(self)

        self.lbl_info = tk.Label(self.frm)
        self.btn_continue = gui.tkit.Mpi3TButton(self.frm)
        self.btn_cancel = gui.tkit.Mpi3TButton(self.frm)

        self.frm_check = tk.Frame(self.frm)
        self.opt_create = ttk.Checkbutton(self.frm_check)
        self.opt_delete = ttk.Checkbutton(self.frm_check)
        self.opt_create.grid(row=0, column=0, sticky=tk.NSEW)
        self.opt_delete.grid(row=1, column=0, sticky=tk.NSEW)

        self.img_import = tk.PhotoImage(file=gui.icon('import'))
        self.icn_import = tk.Label(self, image=self.img_import)

        self.lbl_info.grid(row=0, column=0, sticky=tk.NS + tk.W)
        self.frm_check.grid(row=1, column=0, sticky=tk.NSEW)
        self.btn_continue.grid(row=2, column=0, sticky=tk.NSEW)
        self.btn_cancel.grid(row=2, column=1, sticky=tk.NSEW)
        self.frm_check.grid(pady=10)

        self.icn_import.grid(row=0, column=0, sticky=tk.NSEW)
        self.frm.grid(row=0, column=1, sticky=tk.NSEW)
        self.icn_import.grid(padx=10, pady=10)
        self.frm.grid(padx=10, pady=10)

        self.opt_create.config(text='Create Local Copies')
        self.opt_delete.config(text='Delete Source Files')
        self.btn_cancel.config(text='Cancel')
        self.btn_continue.config(text='Continue')


class Fileflow(tk.Toplevel):

    def __init__(self, songs):
        tk.Toplevel.__init__(self)
        self.resizable(False, True)
        self.title('Create Local Files')
        self._layout()

        self._tsize = 0
        self._psize = 0
        self._songs = songs
        self._dest_path = None

    def setup(self, dest_path):
        self._dest_path = dest_path
        for song in self._songs:
            self._tsize += fileutil.file_size(song.path)

        count = str(len(self._songs))
        txt = 'Moving ' + count + ' songs to ' + self._dest_path
        self.lbl_info.config(text=txt)

        tsize = fileutil.file_size_format(self._tsize)
        self.lbl_size_prog.config(text='0.00 / ' + tsize)
        self.bar_progress.config(maximum=self._tsize + 1)
        self.update()
        self.focus_set()
        self.grid_propagate(False)
        self.btn_close.bind('<ButtonRelease-1>', self._close)

    def start(self):
        for song in self._songs:
            self._check_local_dir(song)

        for song in self._songs:
            action = 'Copying ' + song.path
            self.lbl_action.config(text=action)

            srce = song.path
            dest = fileutil.path_song_local(song, self._dest_path)

            iid = self.tree_progress.insert(
                '', tk.END, text='Create File', values=(dest, ''))

            self.tree_progress.see(iid)
            self.tree_progress.selection_set(iid)

            update = lambda p, s=song, i=iid: self._update(p, s, i)
            try:
                fileutil.file_copy(srce, dest, update)
                song.path = dest
            except FileNotFoundError:
                fs = fileutil.file_size(srce)
                self.bar_progress.step(fs)
                self._tsize -= fs
                col = self.tree_progress.column('detail', 'id')
                self.tree_progress.set(iid, col, 'Error')

        self.lbl_action.config(text='Completed')
        self.btn_close.config(state='normal')
        tk.messagebox.showinfo(title='Completed', message='File transfer complete!')

    def _check_local_dir(self, song):
        dest_dir = fileutil.path_song_local_dir(song, self._dest_path)
        if not os.path.exists(dest_dir):
            action = 'New directory: ' + dest_dir
            self.lbl_action.config(text=action)
            self.update()

            os.makedirs(dest_dir)

            self.tree_progress.insert(
                '', tk.END, text='Create Path',
                values=(dest_dir, 'Success'))

            self.update()

    def _update(self, prog, song, iid):
        step, total = prog
        self._psize += step

        percent = '{:.0%}'.format(total / fileutil.file_size(song.path))
        col = self.tree_progress.column('detail', 'id')
        self.tree_progress.set(iid, col, percent)

        tsize = fileutil.file_size_format(self._tsize)
        psize = fileutil.file_size_format(self._psize)
        progress = psize + ' / ' + tsize
        self.lbl_size_prog.config(text=progress)

        percent = '{:.0%}'.format(self._psize / self._tsize)
        self.lbl_percent.config(text=percent)

        self.bar_progress.step(step)
        self.update()

    def _close(self):
        self.destroy()

    def _layout(self):
        self.frm = tk.Frame(self)

        self.frm_misc = tk.Frame(self.frm)
        self.btn_close = gui.tkit.Mpi3TButton(self.frm_misc)
        self.lbl_size_prog = tk.Label(self.frm_misc)
        self.lbl_size_prog.grid(row=0, column=0, sticky=tk.NS + tk.W)
        self.btn_close.grid(row=0, column=1, sticky=tk.NS + tk.E)
        self.frm_misc.grid_columnconfigure(0, weight=1)

        self.frm_info = tk.Frame(self.frm)
        self.lbl_title = tk.Label(self.frm_info)
        self.lbl_info = tk.Label(self.frm_info)
        self.lbl_title.grid(row=0, column=0, sticky=tk.NS + tk.W)
        self.lbl_info.grid(row=1, column=0, sticky=tk.NS + tk.W)

        self.frm_progress = tk.Frame(self.frm)
        self.lbl_action = tk.Label(self.frm_progress)
        self.lbl_percent = tk.Label(self.frm_progress)
        self.bar_progress = ttk.Progressbar(self.frm_progress)
        self.lbl_action.grid(row=0, column=0, sticky=tk.NS + tk.W)
        self.bar_progress.grid(row=1, column=0, sticky=tk.NSEW)
        self.lbl_percent.grid(row=1, column=1, sticky=tk.NS + tk.E)
        self.frm_progress.grid_columnconfigure(0, weight=1)

        self.frm_treeview = tk.Frame(self.frm, bg='#FFFFFF')
        self.tree_progress = FileflowActionTreeview(self.frm_treeview)
        self.bar_scroll = ttk.Scrollbar(self.frm_treeview)
        self.tree_progress.grid(row=0, column=0, sticky=tk.NSEW)
        self.bar_scroll.grid(row=0, column=1, sticky=tk.NSEW)

        self.frm_info.grid(row=0, column=0, sticky=tk.NSEW)
        self.frm_progress.grid(row=1, column=0, sticky=tk.NSEW)
        self.frm_treeview.grid(row=2, column=0, sticky=tk.NSEW)
        self.frm_misc.grid(row=3, column=0, sticky=tk.NSEW)

        self.frm_progress.grid(pady=10)
        self.frm_treeview.grid(pady=5)
        self.frm.grid(row=0, column=0, sticky=tk.NSEW)
        self.frm.grid(padx=15, pady=10)

        self.frm_treeview.grid_rowconfigure(0, weight=1)
        self.frm_treeview.grid_columnconfigure(0, weight=1)

        self.frm.grid_rowconfigure(2, weight=1)
        self.frm.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.lbl_title.config(font=gui.font(16), anchor=tk.W)
        self.lbl_action.config(font=gui.font(9), anchor=tk.W)
        self.lbl_percent.config(font=gui.font(9), anchor=tk.W)
        self.lbl_size_prog.config(font=gui.font(9), anchor=tk.W)
        self.lbl_info.config(font=gui.font(9), anchor=tk.W)

        self.lbl_percent.config(text='0%')
        self.lbl_title.config(text='Making local file copies')
        self.btn_close.config(text='Close', width=20, state=tk.DISABLED)

        self.frm_treeview.config(highlightthickness=1, highlightbackground='#000000')
        self.bar_progress.config(mode='determinate')
        self.tree_progress.config(yscrollcommand=self.bar_scroll.set)
        self.bar_scroll.config(command=self.tree_progress.yview)


class FileflowActionTreeview(gui.tkit.ActionTreeview):

    def __init__(self, master):
        gui.tkit.ActionTreeview.__init__(self, master)
        self.config(style=gui.MPI3_TREEVIEW_ACTION)

        self['columns'] = ['desc', 'detail']

        self.column('#0', width=85, stretch=False, anchor=tk.NW)
        self.column('desc', width=400, stretch=True, anchor=tk.W)
        self.column('detail', width=60, stretch=False, anchor=tk.W)

        self.heading('#0', text='Action')
        self.heading('desc', text='Description')
        self.heading('detail', text='Detail')

        self.bind('<Double-Button-1>', lambda e: self._open())
        self.bind('<ButtonPress-1>', self._on_lclick)
        self.bind('<Motion>', self._on_motion)

    def _open(self):
        path = self.item(self.selection(), 'values')[0]
        fileutil.path_show_explorer(path)

    def _on_motion(self, event):
        region_id = self.identify_region(event.x, event.y)
        if region_id in ['separator', 'heading']:
            return 'break'

    def _on_lclick(self, event):
        region_id = self.identify_region(event.x, event.y)
        if region_id in ['separator', 'heading']:
            return 'break'
