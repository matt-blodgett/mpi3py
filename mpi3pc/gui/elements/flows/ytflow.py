import tkinter as tk
from tkinter import ttk
from mpi3pc import gui


class PytubeInterface(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title('Youtube Rip')
        self._layout()

        self.btn_download.bind('<ButtonRelease-1>', lambda: print('download'))
        self.btn_batch.bind('<ButtonRelease-1>', self._batch_urls)

    def _batch_urls(self):
        BatchEntry(self)

    def _layout(self):
        self.frm_options = tk.Frame(self)
        self.tree_progress = PytubeActionTreeview(self)
        self.bar_scroll = ttk.Scrollbar(self)

        self.tree_progress.config(yscrollcommand=self.bar_scroll.set)
        self.bar_scroll.config(command=self.tree_progress.yview)

        self.lbl_title = tk.Label(self.frm_options, anchor=tk.W)
        self.box_url = tk.Entry(self.frm_options)
        self.btn_download = gui.tkit.Mpi3TButton(self.frm_options)
        self.btn_batch = gui.tkit.Mpi3TButton(self.frm_options)

        self.lbl_title.config(font=gui.font(16))
        self.lbl_title.config(text='Youtube Downloader')
        self.btn_download.config(text='Download')
        self.btn_batch.config(text='Batch')

        self.btn_download.config(width=10)
        self.btn_batch.config(width=10)

        self.lbl_title.grid(row=0, column=0, sticky=tk.NSEW)
        self.box_url.grid(row=1, column=0, sticky=tk.NSEW)
        self.btn_download.grid(row=1, column=1, sticky=tk.NSEW)
        self.btn_batch.grid(row=1, column=2, sticky=tk.NSEW)

        self.frm_options.grid(row=0, column=0, sticky=tk.NSEW)
        self.tree_progress.grid(row=1, column=0, sticky=tk.NSEW)
        self.bar_scroll.grid(row=1, column=1, sticky=tk.NSEW)
        self.frm_options.grid(padx=10, pady=10)

        self.tree_progress.grid_rowconfigure(0, weight=1)
        self.tree_progress.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)


class PytubeActionTreeview(gui.tkit.ActionTreeview):
    def __init__(self, master):
        gui.tkit.ActionTreeview.__init__(self, master)
        self.config(style=gui.MPI3_TREEVIEW_ACTION)

        self['columns'] = [
            'title', 'status', 'prog', 'size',
            'out', 'dest', 'url', 'fill']

        self.column('title', width=100)
        self.column('status', width=100)
        self.column('prog', width=100)
        self.column('size', width=100)
        self.column('out', width=100)
        self.column('dest', width=100)
        self.column('url', width=100)

        for col in self['columns']:
            self.column(col, minwidth=30, stretch=False, anchor=tk.W)

        self.heading('title', text='Title')
        self.heading('status', text='Status')
        self.heading('prog', text='Progress')
        self.heading('size', text='Size')
        self.heading('out', text='Output')
        self.heading('dest', text='Destination')
        self.heading('url', text='URL')
        self['show'] = 'headings'

        self.bind('<Double-Button-1>', self._open)

    def _open(self, event):
        path = self.item(self.selection(), 'values')[0]
        print(path)
        # futil.show_explore(path)


class BatchEntry(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.title('Batch Download')

        self.frm = tk.Frame(self)
        self.lbl_title = tk.Label(self.frm, anchor=tk.W)
        self.box_urls = tk.Text(self.frm)
        self.btn_enter = gui.tkit.Mpi3TButton(self.frm)
        self.btn_cancel = gui.tkit.Mpi3TButton(self.frm)

        self.lbl_title.config(text='Enter batch urls:')
        self.lbl_title.config(font=gui.font(12))
        self.btn_enter.config(text='Download')
        self.btn_cancel.config(text='Cancel')

        self.lbl_title.grid(row=0, column=0, sticky=tk.NSEW)
        self.box_urls.grid(row=1, column=0, sticky=tk.NSEW)
        self.btn_enter.grid(row=2, column=0, sticky=tk.NSEW)
        self.btn_cancel.grid(row=2, column=1, sticky=tk.NSEW)

        self.lbl_title.grid(columnspan=2)
        self.box_urls.grid(columnspan=2)

        self.frm.grid(row=0, column=0, sticky=tk.NSEW)
        self.frm.grid(padx=10, pady=10)

        self.btn_enter.bind('<ButtonRelease-1>', self._on_enter)
        self.btn_cancel.bind('<ButtonRelease-1>', self.destroy)

    def _on_enter(self):
        print(self.box_urls.get(1.0, tk.END))
