import time
import tkinter as tk
from tkinter import ttk
from mpi3pc import gui


def check_state(element_function):
    def allow(*args, **kwargs):
        element = args[0]
        if isinstance(element, ttk.Widget):
            if tk.DISABLED not in element.state():
                element_function(*args, **kwargs)
        else:
            if str(element['state']) != tk.DISABLED:
                element_function(*args, **kwargs)
    return allow


class Mpi3TButton(ttk.Button):

    def __repr__(self):
        n, m = self.__class__.__name__, self.master
        return '<{} {}>'.format(n, m)

    def __init__(self, master):
        ttk.Button.__init__(self, master)
        self.config(style=gui.MPI3_BUTTON)
        super().bind('<ButtonRelease-1>', self._on_release)
        self._br1_bindings = []

    def bind(self, sequence=None, func=None, add=None):
        if sequence == '<ButtonRelease-1>': self._br1_bindings.append(func)
        else: super().bind(sequence=sequence, func=func, add=add)

    @check_state
    def _on_release(self, event):
        x, y, w, h = event.x, event.y, self.winfo_width(), self.winfo_height()
        if not (x < 0 or x > w or y < 0 or y > h):
            for b in self._br1_bindings: b(event)


class Mpi3Button(tk.Label):

    def __repr__(self):
        n, m = self.__class__.__name__, self.master
        return '<{} {}>'.format(n, m)

    def __init__(self, master):
        tk.Label.__init__(self, master)
        super().bind('<ButtonRelease-1>', self._on_release)
        self._br1_bindings = []

    def bind(self, sequence=None, func=None, add=None):
        if sequence == '<ButtonRelease-1>': self._br1_bindings.append(func)
        else: super().bind(sequence=sequence, func=func, add=add)

    @check_state
    def _on_release(self, event):
        x, y, w, h = event.x, event.y, self.winfo_width(), self.winfo_height()
        if not (x < 0 or x > w or y < 0 or y > h):
            for br1 in self._br1_bindings: br1(event)


class Mpi3ButtonIcon(Mpi3Button):

    def __init__(self, master):
        Mpi3Button.__init__(self, master)

        self.icon = None
        self.colour_bg = '#000000'
        self.colour_icon = (255, 255, 255)

        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<ButtonPress-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_enter)

    @check_state
    def _on_enter(self, event):
        if event.state not in [1032, 1038]:
            self.config(background='#CECECE')

    @check_state
    def _on_leave(self, event):
        self.config(background=self.colour_bg)
        self.icon.colour_pixels(self.colour_icon)
        self.config(image=self.icon.image)

    @check_state
    def _on_press(self, event):
        if self.colour_icon[0] == 255: invert = (0, 0, 0), '#FFFFFF'
        else: invert = (255, 255, 255), '#000000'

        self.icon.colour_pixels(invert[0])
        self.config(image=self.icon.image)
        self.config(background=invert[1])

    def set_theme(self, colour, black_icon):
        self.colour_icon = (255, 255, 255) if not black_icon else (0, 0, 0)
        self.colour_bg = colour
        self.config(background=self.colour_bg)

    def set_icon(self, path):
        self.icon = gui.tkpil.PngIcon(path)
        self.config(image=self.icon.image)


class CanvasButton(tk.Canvas):

    def __repr__(self):
        n, m = self.__class__.__name__, self.master
        return '<{} {}>'.format(n, m)

    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        super().bind('<ButtonRelease-1>', self._on_release)
        self._br1_bindings = []

    def bind(self, sequence=None, func=None, add=None):
        if sequence == '<ButtonRelease-1>': self._br1_bindings.append(func)
        else: super().bind(sequence=sequence, func=func, add=add)

    @check_state
    def _on_release(self, event):
        x, y, w, h = event.x, event.y, self.winfo_width(), self.winfo_height()
        if not (x < 0 or x > w or y < 0 or y > h):
            for br1 in self._br1_bindings: br1(event)


class HoverFadeButton(CanvasButton):

    def __init__(self, master):
        CanvasButton.__init__(self, master)
        self._interrupt = False
        self.window_id = None
        self.icon = None
        self.fade = False
        self._img = None

    def draw(self, dimensions):
        width, height = dimensions
        self.config(width=width, height=height)
        self.config(bd=0, highlightthickness=0)

        x, y = (width/2), (height/2)
        self._img = self.create_image((x, y), image=self.icon.image)
        self.bind('<Leave>', self.start_fade)

    def set_icon(self, pngpath):
        self.icon = gui.tkpil.PngIcon(pngpath)
        self._reset()

    def _recolour(self, event=None):
        self.icon.reset()
        self.icon.colour_pixels((0, 97, 255))
        self.itemconfig(self._img, image=self.icon.image)

    def _reset(self, event=None):
        self._interrupt = True
        self.icon.reset()
        self.itemconfig(self._img, image=self.icon.image)

    def start_fade(self, event=None):
        if self.fade:
            self._interrupt = False
            self._fade()

    def _fade(self):
        if not self.icon.is_transparent() and not self._interrupt:
            self.icon.fade(10)
            self.itemconfig(self._img, image=self.icon.image)
            self.update()
            self.after(10, self._fade)
        elif not self._interrupt and self.window_id:
            self.master.itemconfig(self.window_id, state=tk.HIDDEN)


class StorageSpaceDisplay(tk.Canvas):

    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        self.config(bd=0, highlightthickness=0)
        self.config(highlightbackground='#000000')
        self.config(height=20)

    def refresh(self, allocated, available, capacity):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()

        ratio_allocated = allocated/capacity
        ratio_reserved = 1-((allocated+available)/capacity)

        width_allocated = int(width*ratio_allocated)
        width_reserved = int(width*ratio_reserved)
        width_available = int(width-width_allocated-width_reserved)

        self.delete('fill')
        self.delete('text')

        x = 0
        self._draw_section(x, width_allocated, height, '#8EBFF9')
        self._draw_text(x, width_allocated, height, 'Media')

        x += width_allocated
        self._draw_section(x, width_reserved, height, '#F7BE42')
        self._draw_text(x, width_reserved, height, 'Other')

        x += width_reserved
        self._draw_section(x, width_available, height, '#BABABA')
        text_available = 'Available: {}'.format(self.b2gb(available))
        self._draw_text(x, width_available, height, text_available, center=True)

    def _draw_text(self, x, w, h, text, center=False):
        if not center:
            x += 10
            anchor = tk.W
        else:
            x += w/2
            anchor = tk.CENTER

        h /= 2
        font = ('Calibri', 9, 'bold')
        text_element = self.create_text((x, h), text=text)
        self.itemconfig(text_element, anchor=anchor, font=font, tags='text')
        text_bbox = self.bbox(text_element)
        text_width = text_bbox[2] - text_bbox[0]
        if text_width > w - 10: self.delete(text_element)

    def _draw_section(self, x, w, h, fill):
        self.create_rectangle((x, 0, x+w, h), fill=fill, outline='', tags='fill')
        fade = gui.tkpil.mix_hex(fill, '#FFFFFF', 100, 25)
        for y in range(5):
            colour = gui.tkpil.mix_hex(fade, fill, 4, y)
            self.create_line((x, y, x+w, y), fill=colour, tags='fill')
            self.create_line((x, h-y, x+w, h-y), fill=colour, tags='fill')

    @staticmethod
    def b2gb(byte):
        return '{} GB'.format(str(round(int(byte)/(1024**3), 2)))


class Slider(tk.Canvas):

    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        self.config(highlightthickness=0, bd=0)
        self._tick_curr = 0
        self._tick_max = None
        self._w_cursor = None
        self._w_width = None
        self._y_trough = None

    def draw(self, dimensions, trough_fill):
        width, height = dimensions
        self.config(width=width, height=height)

        self._w_cursor = (width/100)*7
        self._w_width = width-self._w_cursor

        h_ratio, h_trough = height/100, 30
        self._y_trough = h_ratio*h_trough, h_ratio*(100-h_trough)

        coords = 0, self._y_trough[0], width-1, self._y_trough[1]
        self.create_rectangle(*coords, fill=trough_fill, outline='')

        self._indicator_image = gui.tkpil.slider_indicator((int(self._w_cursor), int(height*2)))
        self._indicator = self.create_image((0, 0), image=self._indicator_image, anchor=tk.NW)

        self.bind('<ButtonPress-1>', self._draw_cursor)
        self.bind('<ButtonRelease-1>', self._draw_cursor)
        self.bind('<B1-Motion>', self._draw_cursor)

    def update_callback(self, tick, event):
        pass

    def set_scrollable(self, scrollable):
        if scrollable:
            def _on_scroll(event):
                self.tick(int((self._tick_max/100)*(event.delta/120)))
            self.bind('<MouseWheel>', _on_scroll)
        else: self.unbind('<MouseWheel>')

    def set_maximum(self, max_tick):
        self._tick_max = max_tick

    def tick(self, tick, increment=True):
        if increment: self._tick_curr += tick
        else: self._tick_curr = tick
        self._draw_cursor()

    def _draw_cursor(self, event=None):
        if not self._tick_max: return

        if event:
            x_event = event.x-(self._w_cursor/2)
            tick_change = self._tick_max*(x_event/self._w_width)
            self._tick_curr = int(tick_change)

        self._tick_curr = max(0, min(self._tick_curr, self._tick_max))
        x_draw = self._w_width*(self._tick_curr/self._tick_max)

        self.delete('shade')
        coords = 0, self._y_trough[0], x_draw, self._y_trough[1]
        self.create_rectangle(*coords, tags='shade', fill='#000000', outline='')
        self.coords(self._indicator, (x_draw, 0))

        self.update_callback(self._tick_curr, event)


class Mpi3Treeview(ttk.Treeview):

    def __repr__(self):
        n, m = self.__class__.__name__, self.master
        return '<{} {}>'.format(n, m)

    def __init__(self, master):
        ttk.Treeview.__init__(self, master)


class ActionTreeview(Mpi3Treeview):

    def __init__(self, master):
        ttk.Treeview.__init__(self, master)

    def visible_width(self):
        w = self.column('#0')['width']
        for c in self['columns']:
            w += self.column(c)['width']
        return w


class MediaTreeview(Mpi3Treeview):

    def __init__(self, master):
        Mpi3Treeview.__init__(self, master)
        self.config(height=20, selectmode=tk.EXTENDED)

        self.opened = []
        self.column_schema = []

        self._click_time = 0
        self._click_time_spacing = 0
        self._click_event_origin = None
        self._enter_edit_cell = None, None
        self._last_selected_cell = None, None
        self._last_dragged_column = None
        self._held_column = None

        self._rclick_menu = tk.Menu(self)
        self._box_popup = EditPopup(self)
        self._drag_drop = DragDrop(self)
        self._drag_pos = DragPosition(self)

        self._box_popup.bind('<Tab>', self.edit_cell_next)
        self.bind('<Control-a>', self._select_all)
        self.bind('<MouseWheel>', self._on_scroll)
        self.bind('<ButtonPress-1>', self._on_lclick)
        self.bind('<ButtonPress-3>', self._on_rclick)
        self.bind('<B1-Motion>', self._on_b1motion)
        self.bind('<ButtonRelease>', self._on_release)
        self.bind('<Double-Button-1>', self._on_dbl_click)
        self.bind('<<TreeviewOpen>>', self._on_open)
        self.bind('<<TreeviewClose>>', self._on_close)
        self.bind('<<TreeviewSelect>>', self._on_select)

    def _on_scroll(self, event):
        direction = int(-1*(event.delta/120))
        self.yview_scroll(direction, 'units')

        tree_items = self.get_children()

        try:
            if not self.bbox(tree_items[0]) and direction < 0:
                return 'break'
            elif not self.bbox(tree_items[-1]) and direction > 0:
                return 'break'
        except IndexError:
            pass

    def _on_open(self, event):
        self.opened.append(self.selected_pid())
        self._click_time = 0

    def _on_close(self, event):
        pid = self.selected_pid()
        if pid in self.opened:
            self.opened.remove(pid)
        self._click_time = 0

    def _on_select(self, event):
        if len(self.selection()) > 0:
            self.select_action(event)

    @check_state
    def _select_all(self, event):
        if not self.all_selected:
            self.selection_add(self.get_children())
        else:
            self.selection_remove(self.selection())

    @property
    def all_selected(self):
        for row in self.get_children():
            if row not in self.selection():
                return False
        return True

    def cmd_dbl_click(self, tree):
        pass

    @check_state
    def _on_dbl_click(self, event):
        self.cmd_dbl_click(self)

    @check_state
    def _on_b1motion(self, event):
        if self._held_column:
            x = 0 if event.x < 0 else event.x
            col_curr = self.column(self.identify_column(x))
            if col_curr != self._last_dragged_column:
                self._last_dragged_column = None
                self._drag_heading(col_curr)
        else:
            self.drag_action(event)

    def _drag_heading(self, col_curr):
        col_drag = self._held_column

        if col_curr != col_drag and col_curr['id'] not in ['fill', '']:

            def col_get(attr, value):
                for c in self.column_schema:
                    if c[attr] == value: return c
                return None

            c_from = col_get('id', col_drag['id'])
            c_dest = col_get('id', col_curr['id'])

            dest_index = self.column_schema.index(c_dest)
            self.column_schema.remove(c_from)
            self.column_schema.insert(dest_index, c_from)

            self._last_dragged_column = col_curr
            self._columns_disp()

    def _on_lclick(self, event):
        region_id = self.identify_region(event.x, event.y)
        region_row = self.identify_row(event.y)
        region_column = self.column(self.identify_column(event.x))

        if ((region_id == 'heading' and region_column == self.column('#0'))
            or (region_row in self.selection() and len(self.selection()) > 1)):
            return 'break'
        else:
            self._on_lclick_cont(event)

    @check_state
    def _on_lclick_cont(self, event):
        self._click_time_spacing = time.time() - self._click_time
        self._click_time = time.time()

        region_id = self.identify_region(event.x, event.y)
        region_row = self.identify_row(event.y)
        region_column = self.column(self.identify_column(event.x))

        if region_id == 'heading' and not region_column == self.column('#0'):
            self._held_column = region_column

        if region_id == 'separator':
            self.unbind('<B1-Motion>')
        else:
            self.bind('<B1-Motion>', self._on_b1motion)

        if ((region_id in ['cell', 'tree']
             and not self._last_selected_cell == (region_row, region_column))
            or region_id == 'nothing'):
            self._box_popup.hide()

        self._last_selected_cell = region_row, region_column

    @check_state
    def _on_release(self, event):
        self._held_column = None
        self._drag_drop.hide()
        self._drag_pos.hide()

        x = 0 if event.x < 0 else event.x
        region_id = self.identify_region(event.x, event.y)
        region_row = self.identify_row(event.y)
        region_column = self.column(self.identify_column(x))

        is_heading = (region_id in ['heading', 'separator'])
        is_cell = (region_id in ['cell', 'tree'])

        sel_count = len(self.selection())
        is_lclick = (event.state not in [1032, 1038])
        has_moved = (region_row not in self.selection())

        held_time = (time.time() - self._click_time)
        clicked = (held_time < 0.5)
        clicked_time = (0.1 < self._click_time_spacing < 1)

        if not is_heading and has_moved and sel_count > 0:
            self.drop_action(event)

        elif is_heading and clicked and is_lclick:
            self.sort(region_column)

        elif is_cell and clicked and clicked_time and sel_count == 1:
            if self._enter_edit_cell == self._last_selected_cell:
                self.edit_cell((region_row, region_column['id']))
            else:
                self._box_popup.hide()

        self._enter_edit_cell = self._last_selected_cell

    @check_state
    def _on_rclick(self, event):
        row = self.identify_row(event.y)
        col = self.identify_column(event.x)

        if row and row not in self.selection():
            self.selection_set(row)
            self._last_selected_cell = (row, col)
        elif not row:
            self.selection_remove(*self.get_children())

        self._rclick_menu.setup(event)

    def _columns_init(self, column_schema, root_width):
        self.column_schema = column_schema
        self.column_schema.append(
            {'id': 'fill', 'width': 5000, 'visible': True, 'heading': ''})
        self['columns'] = [c['id'] for c in self.column_schema]
        self.column('#0', width=root_width, minwidth=30,
                    stretch=False, anchor=tk.W)

        for c in self.column_schema:
            self.column(c['id'], width=c['width'], minwidth=30,
                        stretch=False, anchor=tk.W)
            self.heading(c['id'], text=c['heading'])

        self._columns_disp()

    def _columns_disp(self):
        self['displaycolumns'] = [
            c['id'] for c in self.column_schema if c['visible']]

    def columns_setvis(self, cids, vis):
        for col in self.column_schema:
            if col['id'] in cids and col['id'] != 'fill':
                col['visible'] = vis
        self._columns_disp()

    def get_schema(self):
        for c in self.column_schema:
            c['width'] = self.column(c['id'])['width']
        root_width = self.column('#0')['width']
        return root_width, self.column_schema

    def visible_width(self):
        w = self.column('#0')['width']
        for c in self['displaycolumns']:
            w += self.column(c)['width']
        return w

    def set_open(self, i_open, iid=None):
        for row in self.get_children(iid):
            if len(self.get_children(row)) > 0:
                self.opened.append(self.item(row)['tags'][0])
            self.item(row, open=i_open)
            self.set_open(i_open, row)

    def selected_pid(self):
        if len(self.selection()) == 1:
            return list(self.selected_pids())[0]
        return None

    def selected_pids(self):
        for row in self.selection():
            yield self.item(row)['tags'][0]

    def refresh(self):
        pass

    def select_action(self, event):
        pass

    def drag_action(self, event):
        pass

    def drop_action(self, event):
        pass

    def edit_cell(self, cell):
        pass

    def edit_cell_next(self, event):
        pass

    def sort(self, region_column):
        pass


class DragDrop(tk.Label):

    def __repr__(self):
        n, m = self.__class__.__name__, self.master
        return '<{} {}>'.format(n, m)

    def __init__(self, master):
        tk.Label.__init__(self, master)
        self.config(font=gui.font(9))
        self.config(state=tk.DISABLED)
        self.config(bg='#FFFFFF', bd=1)
        self.config(highlightthickness=1)
        self.config(highlightbackground='#000000')
        self.config(relief=tk.SOLID)
        self.config(anchor=tk.W)

    def set_text(self, text):
        self.config(text='  ' + text)

    def hide(self):
        self.place_forget()

    def move(self, xy):
        self.place(x=xy[0], y=xy[1], width=150, height=20, anchor=tk.W)


class DragPosition(tk.Frame):

    def __repr__(self):
        n, m = self.__class__.__name__, self.master
        return '<{} {}>'.format(n, m)

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(bg='#000000')

    def hide(self):
        self.place_forget()

    def drag_row(self, y):
        self.place(x=0, y=y, relwidth=1, height=2, anchor=tk.W)


class EditPopup(tk.Entry):

    def __repr__(self):
        n, m = self.__class__.__name__, self.master
        return '<{} {}>'.format(n, m)

    def __init__(self, master):
        tk.Entry.__init__(self, master)
        self.config(font=gui.font(9))
        self.config(relief=tk.FLAT)

        self.cell = None, None
        self.update_command = lambda *ignore: None

        self.bind('<Tab>', self._on_tab, add=True)
        self.bind('<Return>', self._on_enter)
        self.bind('<Control-a>', self._select_all)
        self.bind('<Escape>', lambda *ignore: self.hide())

    def popup(self, cell):
        if cell[1] == '': cell = cell[0], '#0'
        self.cell = cell
        row, col = cell

        x, y, w, h = self.master.bbox(row, col)
        self.place(x=x, y=(y+(h//2)), width=w, height=h, anchor=tk.W)

        cid = self.master.column(col)['id']

        if cid != '':
            values = self.master.item(row)['values']
            index = self.master['columns'].index(cid)
            text = values[index]
        else:
            text = self.master.item(row)['text']

        self.delete(0, tk.END)
        self.insert(0, text)
        self._select_all()
        self.focus_force()

    def _on_enter(self, event):
        self._update_cell()
        self.hide()

    def _on_tab(self, event):
        self._update_cell()

    def _update_cell(self):
        row, col = self.cell
        cid = self.master.column(col)['id']

        if cid != '':
            self.master.set(row, col, self.get())
        elif cid == '':
            self.master.item(row, text=self.get())

        self.update_command()

    def hide(self):
        self.delete(0, tk.END)
        self.place_forget()

    def _select_all(self, *ignore):
        self.selection_range(0, tk.END)
        return 'break'
