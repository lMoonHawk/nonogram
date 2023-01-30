from tkinter import *

root = Tk()


canvas = Canvas(root, width=500, height=500)
canvas.pack()


x1, y1 = 100, 150
x2, y2 = 400, 350
# rad = 20
fill_color = "red"
outline_color = "blue"

# canvas.create_rectangle(x1, y1, x2, y2, fill="blue")


def create_rounded_rectangle(canvas, x1, y1, x2, y2, rad=None, fill=None, outline="black", width=1):

    if rad is None:
        rad = min(x2 - x1, y2 - y1) // 10
    rad = max(min(min(x2 - x1, y2 - y1) // 2, rad), 0)
    out = []
    if fill:
        out.append(canvas.create_arc(x2 - 2 * rad, y1, x2, y1 + 2 * rad, start=0 * 90, fill=fill, outline=fill))
        out.append(canvas.create_arc(x2 - 2 * rad, y2 - 2 * rad, x2, y2, start=3 * 90, fill=fill, outline=fill))
        out.append(canvas.create_arc(x1, y2 - 2 * rad, x1 + 2 * rad, y2, start=2 * 90, fill=fill, outline=fill))
        out.append(canvas.create_arc(x1, y1, x1 + 2 * rad, y1 + 2 * rad, start=1 * 90, fill=fill, outline=fill))
        out.append(canvas.create_rectangle(x1 + rad, y1, x2 - rad, y2, fill=fill, width=0))
        out.append(canvas.create_rectangle(x1, y1 + rad, x2, y2 - rad, fill=fill, width=0))

    if width:
        canvas.create_line(x1 + rad, y1, x2 - rad, y1, fill=outline, width=width)
        canvas.create_line(x1 + rad, y2, x2 - rad, y2, fill=outline, width=width)
        canvas.create_line(x1, y1 + rad, x1, y2 - rad, fill=outline, width=width)
        canvas.create_line(x2, y1 + rad, x2, y2 - rad, fill=outline, width=width)
        canvas.create_arc(x2 - 2 * rad, y1, x2, y1 + 2 * rad, start=0 * 90, style="arc", outline=outline, width=width)
        canvas.create_arc(x2 - 2 * rad, y2 - 2 * rad, x2, y2, start=3 * 90, style="arc", outline=outline, width=width)
        canvas.create_arc(x1, y2 - 2 * rad, x1 + 2 * rad, y2, start=2 * 90, style="arc", outline=outline, width=width)
        canvas.create_arc(x1, y1, x1 + 2 * rad, y1 + 2 * rad, start=1 * 90, style="arc", outline=outline, width=width)
    return out


# canvas.create_rectangle(x1, y1, x2, y2, fill="black", width=1, outline="blue")
tags = create_rounded_rectangle(canvas, x1, y1, x2, y2, fill="blue", width=1, outline="red", rad=35)
for shape in tags:
    canvas.itemconfig(shape, fill="white", outline="white")

root.mainloop()
