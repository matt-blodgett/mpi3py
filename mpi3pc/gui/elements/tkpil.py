from PIL import ImageColor as ImageColour
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageTk
from PIL import Image
import tkinter as tk


def mix_rgb(rgb1, rgb2, strength, depth):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2

    ratio = lambda c2, c1: float(c2 - c1) / strength
    mix = lambda c1, r: int(c1 + (r * depth))
    bound = lambda c: max(0, min(c, 255))

    r = bound(mix(r1, ratio(r2, r1)))
    g = bound(mix(g1, ratio(g2, g1)))
    b = bound(mix(b1, ratio(b2, b1)))

    return r, g, b


def mix_hex(hex1, hex2, strength, depth):
    rgb1 = ImageColour.getrgb(hex1)
    rgb2 = ImageColour.getrgb(hex2)
    rgb_mixed = mix_rgb(rgb1, rgb2, strength, depth)
    return '#%02x%02x%02x' % rgb_mixed


def iter_pixels(img):
    for x, y in ([(x, y) for x in range(img.width) for y in range(img.height)]):
        yield x, y


def text_size(text, font_size):
    t_font = ImageFont.truetype('arial.ttf', font_size)
    return t_font.getsize(text)


def text_ellipsis(text, font_size, width):
    e_width = text_size('...', font_size)[0]
    t_width = text_size(text, font_size)[0] + 40

    if t_width < width: return text

    while t_width + e_width > width:
        text = text[:len(text)-1]
        t_width = text_size(text, font_size)[0]

    return '{}{}'.format(text, '...')


def slider_indicator(dimensions):
    indicator = Image.new('RGB', size=dimensions)
    return ImageTk.PhotoImage(indicator)


class PngIcon:

    def __init__(self, pngpath):
        self._path = pngpath
        self._raw_image = Image.open(self._path).convert('RGBA')
        self.image = ImageTk.PhotoImage(self._raw_image)

    def fade(self, alpha):
        icon = self._raw_image

        bound = lambda c: max(0, min(c, 255))
        put = lambda x, y, rbga: icon.putpixel((x, y), rgba)
        for x, y in (self._iter_xy(icon)):
            r, g, b, a = icon.getpixel((x, y))
            rgba = r, g, b, bound(a - alpha)
            put(x, y, rgba)

        self._raw_image = icon
        self.image = ImageTk.PhotoImage(self._raw_image)

    def is_transparent(self):
        icon = self._raw_image
        for x, y in (self._iter_xy(icon)):
            r, g, b, a = icon.getpixel((x, y))
            if a > 0: return False
        return True

    def reset(self):
        self._raw_image = Image.open(self._path).convert('RGBA')
        self.image = ImageTk.PhotoImage(self._raw_image)

    def colour_pixels(self, rgb):
        icon = self._raw_image
        r, g, b = rgb
        put = lambda x, y, a: icon.putpixel((x, y), (r, g, b, a))
        for x, y in (self._iter_xy(icon)):
            r1, g1, b1, a = icon.getpixel((x, y))
            if a != 0: put(x, y, a)

        self._raw_image = icon
        self.image = ImageTk.PhotoImage(self._raw_image)

    def _iter_xy(self, img):
        for x, y in ([(x, y) for x in range(img.width) for y in range(img.height)]):
            yield x, y


class ArrayLabel(tk.Canvas):

    def __init__(self, master, text):
        tk.Canvas.__init__(self, master, width=1, height=1, highlightthickness=0, bd=0)

        self._text = text
        self._font_type = ImageFont.truetype('consola.ttf', 17)
        self._font_fill = (0, 0, 0, 255)

        w, h = self._font_type.getsize(text)
        self.configure(width=w, height=h)

        self._base_label = Image.new('RGBA', (w, h), (255, 255, 255, 0))
        self._base_image = ImageTk.PhotoImage(self._base_label)
        self._draw = ImageDraw.Draw(self._base_label)

        self._char_list = []
        self._initial_char_list()

        self._text_draw_all()

        self.curr_char = 0

    def _initial_char_list(self):
        x = 0
        for char in self._text:
            font = self._font_type
            w, h = font.getsize(char)
            fill = self._font_fill

            sc = DrawChar(char, self._draw, self._base_label)
            sc.set(x=x, y=0)
            sc.set(font=font, fill=fill)

            self._char_list.append(sc)
            x += w

    def _update(self):
        self.delete('text')
        self._base_image = ImageTk.PhotoImage(self._base_label)
        self.create_image((0, 0), image=self._base_image, anchor='nw', tags='text')

    def _text_draw_all(self):
        for sc in self._char_list: sc.draw()
        self._update()

    def _clear_region(self, region):
        clear = (255, 255, 255, 0)
        x0, y0, x1, y1 = region

        for x in range(x0, x1):
            for y in range(y0, y1):
                self._base_label.putpixel((x, y), clear)

    def _slide(self):

        curr = self.curr_char + 1
        self.curr_char = 0 if (curr >= len(self._text) - 1) else curr

        sc = self._char_list[curr]
        sc.clear()

        if curr - 1 >= 0:
            a = self._char_list[(curr - 1)]
            a.draw()

        self._update()
        self.master.update()

        self.after(100, self._animate)

    def effect(self):
        self.curr_char = -1

        # for sc in self._char_list:
        #    print(sc.char, sc.x, sc.y, sc.width(), sc.height())

        self._animate()

    def _animate1(self):

        curr = self.curr_char + 1
        self.curr_char = 0 if (curr >= len(self._text) - 1) else curr

        sc = self._char_list[curr]
        sc.clear()

        if curr - 1 >= 0:
            a = self._char_list[(curr - 1)]
            a.draw()

        self._update()
        self.master.update()

        self.after(100, self._animate)

    def effect1(self):
        self.curr_char = -1

        # for sc in self._char_list:
        #    print(sc.char, sc.x, sc.y, sc.width(), sc.height())

        self._animate()


class DrawChar:

    def __init__(self, char, draw, image, x=0, y=0, width=0, height=0,
                 font=None, fill=None):
        self.x = x
        self.y = y

        self.char = char
        self.font = font
        self.fill = fill

        self.pil_draw = draw
        self.image = image

    def width(self):
        return self.font.getsize(self.char)[0]

    def height(self):
        return self.font.getsize(self.char)[1]

    def set(self, char=None, x=None, y=None, font=None, fill=None):

        if x: self.x = x
        if y: self.y = y
        if char: self.char = char
        if font: self.font = font
        if fill: self.fill = fill

    def draw(self):
        self.pil_draw.text((self.x, self.y), self.char,
                           font=self.font, fill=self.fill)

    def clear(self):
        clear = (255, 255, 255, 0)
        x0 = self.x
        y0 = self.y
        x1 = self.x + self.width()
        y1 = self.y + self.height()

        for x in range(x0, x1):
            for y in range(y0, y1):
                self.image.putpixel((x, y), clear)


class tkkk(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.configure(background='#A0B5D6')
        self.configure(height=400, width=800)
        self.grid_propagate(False)

        teststring = ('abc 123 def456 hij789')
        self.slabel = ArrayLabel(self, teststring)
        self.slabel.grid(row=0, column=0, sticky='NEWS')
        self.slabel.grid(padx=10, pady=10)

        self.button = tk.Button(self, text='splinter')
        self.button.bind('<ButtonRelease>', self._splinter)
        self.button.grid(row=0, column=1, sticky='NEWS')
        self.button.grid(padx=10, pady=10)

    def _splinter(self, event=None):
        self.slabel.effect()

# root = tkkk()
# root.mainloop()
