

__all__ = [
    'initiate', 'font', 'icon',
    'MPI3_FONTNAME',
    'MPI3_ENTRY',
    'MPI3_BUTTON',
    'MPI3_SIZEGRIP',
    'MPI3_CHECKBUTTON',
    'MPI3_CHECKBUTTON_TREE',
    'MPI3_TREEVIEW_MEDIA',
    'MPI3_TREEVIEW_ACTION',
    'MPI3_TREEVIEW_SIDEBAR',
    'MPI3_TREEVIEW_TOGGLE',
    'MPI3_TREEVIEW_DRIVES'
]


from tkinter import ttk


MPI3_FONTNAME = 'Helvetica'
MPI3_ENTRY = 'MPI3.TEntry'
MPI3_BUTTON = 'MPI3.TButton'
MPI3_SIZEGRIP = 'MPI3.TSizegrip'
MPI3_CHECKBUTTON = 'MPI3.OPT.TCheckbutton'
MPI3_TREEVIEW_MEDIA = 'MPI3.TREE.MEDIA.Treeview'
MPI3_TREEVIEW_ACTION = 'MPI3.TREE.ACTION.Treeview'
MPI3_TREEVIEW_SIDEBAR = 'MPI3.TREE.SIDEBAR.Treeview'
MPI3_TREEVIEW_TOGGLE = 'MPI3.TREE.TOGGLE.Treeview'
MPI3_TREEVIEW_DRIVES = 'MPI3.TREE.DRIVES.Treeview'
MPI3_CHECKBUTTON_TREE = 'MPI3.TREE.OPT.TCheckbutton'

def font(size, option='normal'):
    return MPI3_FONTNAME, size, option


def icon(icon_name, ext='.png'):
    return '{}{}{}'.format('rsrcpc/icons/', icon_name, ext)


def initiate():
    style = ttk.Style()
    style.theme_use('xpnative')

    ################################################################################
    # MPI3_BUTTON
    style.configure(
        MPI3_BUTTON,
        font=font(9)
    )

    ################################################################################
    # MPI3_CHECKBUTTON
    style.configure(
        MPI3_CHECKBUTTON,
        font=font(9),
        borderwidth=0,
        relief='flat'
    )

    ################################################################################
    # MPI3_CHECKBUTTON_TREE
    style.configure(
        MPI3_CHECKBUTTON_TREE,
        background='#FFFFFF',
        font=font(9),
        borderwidth=0,
        relief='flat'
    )

    ################################################################################
    # MPI3_SIZEGRIP
    style.configure(
        MPI3_SIZEGRIP,
        background='#000000',
        relief='flat',
        borderwidth=0
    )

    ################################################################################
    # MPI3_ENTRY
    style.configure(
        MPI3_ENTRY,
        background='#FFFFFF',
        font=font(9),
        relief='flat',
        borderwidth=10
    )

    ################################################################################
    # MPI3_TREEVIEW_MEDIA
    style.configure(
        MPI3_TREEVIEW_MEDIA,
        background='#FFFFFF',
        font=font(9),
        relief='flat',
        borderwidth=0
    )

    style.configure(
        MPI3_TREEVIEW_MEDIA + '.Item',
        padding=(5, 0)
    )

    style.layout(
        MPI3_TREEVIEW_MEDIA, [
            ('Treeview.treearea', {
                'sticky': 'nswe'
            })
        ]
    )

    ################################################################################
    # MPI3_TREEVIEW_ACTION
    style.configure(
        MPI3_TREEVIEW_ACTION,
        background='#FFFFFF',
        font=font(8),
        relief='flat',
        borderwidth=0,
    )

    style.layout(
        MPI3_TREEVIEW_ACTION, [
            ('Treeview.treearea', {
                'sticky': 'nswe'
            })
        ]
    )

    ################################################################################
    # MPI3_TREEVIEW_SIDEBAR
    style.configure(
        MPI3_TREEVIEW_SIDEBAR,
        background='#FFFFFF',
        font=font(8),
        relief='flat',
        borderwidth=0,
        indent=6
    )

    style.configure(
        MPI3_TREEVIEW_SIDEBAR + '.Item',
        padding=(5, 0)
    )

    style.layout(
        MPI3_TREEVIEW_SIDEBAR, [
            ('Treeview.treearea', {
                'sticky': 'nswe'
            })
        ]
    )

    ################################################################################
    # MPI3_TREEVIEW_DRIVES
    style.configure(
        MPI3_TREEVIEW_DRIVES,
        background='#FFFFFF',
        font=font(9),
        relief='flat',
        borderwidth=0,
        indent=10
    )

    style.configure(
        MPI3_TREEVIEW_DRIVES + '.Item',
        padding=(5, 0)
    )

    style.configure(
        MPI3_TREEVIEW_DRIVES + '.Heading',
        font=font(10)
    )

    style.layout(
        MPI3_TREEVIEW_DRIVES, [
            ('Treeview.treearea', {
                'sticky': 'nswe'
            })
        ]
    )

    style.layout(
        MPI3_TREEVIEW_DRIVES + '.Item', [
            ('Treeitem.padding', {
                'sticky': 'nswe',
                'children': [
                    ('Treeitem.indicator', {'side': 'left', 'sticky': 'w'}),
                    ('Treeitem.image', {'side': 'left', 'sticky': 'w'}),
                    # ('Treeitem.focus', {'side': 'left', 'sticky': 'e'}),
                    ('Treeitem.text', {'side': 'left', 'sticky': 'e'}),
                ]
            })
        ]
    )

    ################################################################################
    # MPI3_TREEVIEW_TOGGLE
    style.configure(
        MPI3_TREEVIEW_TOGGLE,
        background='#FFFFFF',
        font=font(8),
        relief='flat',
        borderwidth=0,
        indent=6,
    )

    style.configure(
        MPI3_TREEVIEW_TOGGLE + '.Item',
        padding=(20, 0),
    )

    style.map(
        MPI3_TREEVIEW_TOGGLE,
        background=[('selected', '#FFFFFF')],
        foreground=[('selected', '#000000')]
    )

    style.configure(
        MPI3_TREEVIEW_TOGGLE + '.Heading',
        background='#FFFFFF',
        foreground='#000000'
    )

    style.map(
        MPI3_TREEVIEW_TOGGLE + '.Heading',
        background=[('active', '#FFFFFF')],
        foreground=[('active', '#000000')]
    )

    # style.map(
    #     MPI3_TREEVIEW_TOGGLE + '.Heading',
    #     background=[('focus', '#FFFFFF')],
    #     foreground=[('focus', '#000000')],
    # )

    style.layout(
        MPI3_TREEVIEW_TOGGLE, [
            ('Treeview.treearea', {
                'sticky': 'nswe'
            })
        ]
    )

    style.layout(
        MPI3_TREEVIEW_TOGGLE + '.Item', [
            ('Treeitem.padding', {
                'sticky': 'nswe',
                'children': [
                    ('Treeitem.indicator', {'side': 'left', 'sticky': 'w'}),
                    ('Treeitem.image', {'side': 'left', 'sticky': 'w'}),
                    # ('Treeitem.focus', {'side': 'left', 'sticky': 'e'}),
                    ('Treeitem.text', {'side': 'left', 'sticky': 'e'}),
                ]
            })
        ]
    )

    ################################################################################
    # MPI3_CHECKBUTTON_TREE
    style.layout(
        MPI3_CHECKBUTTON_TREE, [
            ('Checkbutton.padding',
             {'sticky': 'nswe', 'children': [
                 ('Checkbutton.indicator', {'side': 'right', 'sticky': 'e'})
                 # ('Checkbutton.focus', {'side': 'left', 'sticky': 'w', 'children': [
                 #     ('Checkbutton.label', {'sticky': 'nswe'})
                 # ]})
             ]})
        ]
    )

    # 'Treeheading.border': (),
    # 'Treeitem.indicator': (),
    # 'Treeview.field': (),
    #
    # "Treeview"
    # "Treeview.Heading"
    # "Treeview.Row"
    # "Treeview.Cell"
    # "Treeview.Item"

    # print(style.layout('Treeview.Item'))
    # style.configure('Treeview', indent=7)
