import tkinter as tk
import random
import time

CELL = 70
SIZE = 10

snakes = {99: 54, 95: 72, 70: 55, 52: 42, 25: 2}
ladders = {6: 25, 11: 40, 17: 69, 46: 90, 60: 83}

root = tk.Tk()
root.title("🐍 Snake & Ladder Pro")
root.geometry("750x850")
root.config(bg="#1e1e2f")

canvas = tk.Canvas(root, width=700, height=700, bg="#2b2d42", highlightthickness=0)
canvas.pack(pady=10)

info = tk.Label(root, text="نوبت بازیکن 1", fg="white", bg="#1e1e2f",
                font=("Arial", 16, "bold"))
info.pack()

# ---------- صفحه ----------
colors = ["#ffbe0b", "#fb5607", "#ff006e", "#8338ec", "#3a86ff"]

num = 1
for row in range(SIZE):
    for col in range(SIZE):

        r = row
        c = col if row % 2 == 0 else 9 - col

        x1 = c * CELL
        y1 = (9 - r) * CELL
        x2 = x1 + CELL
        y2 = y1 + CELL

        canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=random.choice(colors),
            outline="white",
            width=2
        )

        canvas.create_text(
            x1 + 10, y1 + 10,
            text=str(num),
            fill="white",
            font=("Arial", 10, "bold")
        )

        num += 1

# ---------- موقعیت ----------
def get_xy(pos):
    pos -= 1
    row = pos // 10
    col = pos % 10

    if row % 2 == 1:
        col = 9 - col

    x = col * CELL + CELL // 2
    y = (9 - row) * CELL + CELL // 2

    return x, y

# ---------- نردبان ----------
def draw_ladder(s, e):
    x1, y1 = get_xy(s)
    x2, y2 = get_xy(e)

    canvas.create_line(x1-10, y1, x2-10, y2, width=6, fill="#8d5524")
    canvas.create_line(x1+10, y1, x2+10, y2, width=6, fill="#8d5524")

    for i in range(6):
        t = i/5
        lx = (x1-10)+(x2-x1)*t
        ly = y1+(y2-y1)*t
        rx = (x1+10)+(x2-x1)*t
        ry = y1+(y2-y1)*t

        canvas.create_line(lx, ly, rx, ry, width=4, fill="#c68642")

# ---------- مار ----------
def draw_snake(s, e):
    x1, y1 = get_xy(s)
    x2, y2 = get_xy(e)

    canvas.create_line(
        x1, y1, x2, y2,
        width=12,
        fill="#06d6a0",
        smooth=True
    )

    canvas.create_oval(
        x1-12, y1-12,
        x1+12, y1+12,
        fill="#06d6a0"
    )

# رسم
for s, e in ladders.items():
    draw_ladder(s, e)

for s, e in snakes.items():
    draw_snake(s, e)

# ---------- بازیکن ----------
p1_pos = 1
p2_pos = 1
turn = 1

x, y = get_xy(1)

p1 = canvas.create_oval(x-18, y-18, x+18, y+18,
                        fill="#ff006e", outline="white", width=3)

p2 = canvas.create_oval(x-18, y-18, x+18, y+18,
                        fill="#00f5d4", outline="white", width=3)

# ---------- حرکت انیمیشنی ----------
def animate(piece, start, end):
    for step in range(start, end+1):
        x, y = get_xy(step)
        canvas.coords(piece, x-18, y-18, x+18, y+18)
        root.update()
        time.sleep(0.08)

# ---------- تاس ----------
dice_label = tk.Label(root, text="🎲", font=("Arial", 40),
                      bg="#1e1e2f", fg="white")
dice_label.pack()

# ---------- بازی ----------
def roll():
    global p1_pos, p2_pos, turn

    dice = random.randint(1, 6)
    dice_label.config(text=f"🎲 {dice}")

    if turn == 1:
        old = p1_pos
        p1_pos = min(100, p1_pos + dice)

        animate(p1, old, p1_pos)

        if p1_pos in ladders:
            animate(p1, p1_pos, ladders[p1_pos])
            p1_pos = ladders[p1_pos]

        elif p1_pos in snakes:
            animate(p1, p1_pos, snakes[p1_pos])
            p1_pos = snakes[p1_pos]

        if p1_pos == 100:
            info.config(text="🏆 بازیکن 1 برنده شد!")
            return

        turn = 2

    else:
        old = p2_pos
        p2_pos = min(100, p2_pos + dice)

        animate(p2, old, p2_pos)

        if p2_pos in ladders:
            animate(p2, p2_pos, ladders[p2_pos])
            p2_pos = ladders[p2_pos]

        elif p2_pos in snakes:
            animate(p2, p2_pos, snakes[p2_pos])
            p2_pos = snakes[p2_pos]

        if p2_pos == 100:
            info.config(text="🏆 بازیکن 2 برنده شد!")
            return

        turn = 1

    info.config(text=f"نوبت بازیکن {turn}")

# ---------- دکمه ----------
btn = tk.Button(
    root,
    text="🎲 تاس بنداز",
    font=("Arial", 16, "bold"),
    bg="#ffbe0b",
    fg="black",
    command=roll
)
btn.pack(pady=10)

root.mainloop()
