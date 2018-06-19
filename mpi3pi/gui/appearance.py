

__all__ = [
    'initiate', 'font', 'icon',
]


from tkinter import ttk


def font(size, option='normal'):
    return MPI3_FONTNAME, size, option


def icon(icon_name, ext='.png'):
    return '{}{}{}'.format('rsrc/gui/', icon_name, ext)


def initiate():
    style = ttk.Style()
    style.theme_use('xpnative')
