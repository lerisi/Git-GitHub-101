# -*- coding: utf-8 -*-
"""
Hello World แบบ Animation ด้วย Tkinter (single file, ใช้แค่ standard library)
by lerisi

ฟีเจอร์:
  - พื้นหลังไล่สีเคลื่อนไหวตลอดเวลา
  - ดาวระยิบระยับลอยขึ้น
  - ตัวอักษร "Hello, World!" ร่วงลงมาทีละตัว แล้วเต้นเป็นคลื่น พร้อมสีรุ้งเปลี่ยนไปเรื่อยๆ
  - ข้อความย่อยพิมพ์ทีละตัวอักษร
  - จุดแสงโคจรรอบข้อความ
  - คลิกเมาส์เพื่อสร้างพลุ  |  กด Esc เพื่อออก

วิธีรัน:  python hello_animation.py
"""

import colorsys
import math
import random
import tkinter as tk
from tkinter import font as tkfont

WIDTH, HEIGHT = 960, 560
FPS_DELAY = 16  # ms (~60 fps)

TITLE = "Hello, World!"
SUBTITLE = "ยินดีต้อนรับสู่โลกของ Python + Tkinter ✨"
HINT = "คลิกเพื่อสร้างพลุ  •  กด Esc เพื่อออก"


def hsv(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, max(0, min(1, s)), max(0, min(1, v)))
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"


def ease_out_bounce(t):
    t = max(0.0, min(1.0, t))
    if t < 1 / 2.75:
        return 7.5625 * t * t
    if t < 2 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    if t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    t -= 2.625 / 2.75
    return 7.5625 * t * t + 0.984375


class HelloApp:
    BANDS = 72

    def __init__(self, root):
        self.root = root
        root.title("Hello World ✨")
        root.geometry(f"{WIDTH}x{HEIGHT}")
        root.minsize(640, 420)
        root.bind("<Escape>", lambda e: root.destroy())

        self.canvas = tk.Canvas(root, highlightthickness=0, bg="#0b1030")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Configure>", self.on_resize)

        self.w, self.h = WIDTH, HEIGHT
        self.frame = 0

        self.title_font = tkfont.Font(family="Helvetica", size=68, weight="bold")
        self.sub_font = tkfont.Font(family="TkDefaultFont", size=17)
        self.hint_font = tkfont.Font(family="TkDefaultFont", size=10)

        self.bands = []
        self.stars = []
        self.sparks = []
        self.letters = []   # (shadow_id, main_id, char_x_offset)
        self.orbs = []

        self.build_scene()
        self.tick()

    # ------------------------------------------------------------------
    def build_scene(self):
        c = self.canvas
        c.delete("all")
        self.bands.clear()
        self.stars.clear()
        self.letters.clear()
        self.orbs.clear()

        # gradient bands
        band_h = self.h / self.BANDS + 1
        for k in range(self.BANDS):
            self.bands.append(c.create_rectangle(0, k * self.h / self.BANDS, self.w,
                                                  k * self.h / self.BANDS + band_h,
                                                  fill="#000", outline=""))

        # stars
        for _ in range(70):
            x = random.uniform(0, self.w)
            y = random.uniform(0, self.h)
            r = random.uniform(1.0, 3.2)
            item = c.create_oval(x - r, y - r, x + r, y + r, fill="#fff", outline="")
            self.stars.append({
                "id": item, "x": x, "y": y, "r": r,
                "speed": random.uniform(0.2, 0.9),
                "phase": random.uniform(0, math.tau),
                "hue": random.uniform(0.5, 0.95),
            })

        # title letters
        widths = [self.title_font.measure(ch) for ch in TITLE]
        total = sum(widths)
        x = (self.w - total) / 2
        self.title_y = self.h * 0.42
        for ch, wd in zip(TITLE, widths):
            shadow = c.create_text(x + 4, self.title_y + 5, text=ch, anchor="w",
                                    font=self.title_font, fill="#000", state="hidden")
            main = c.create_text(x, self.title_y, text=ch, anchor="w",
                                  font=self.title_font, fill="#fff", state="hidden")
            self.letters.append({"shadow": shadow, "main": main, "x": x, "w": wd})
            x += wd
        self.title_left = (self.w - total) / 2
        self.title_total = total

        # underline
        self.underline = c.create_line(0, 0, 0, 0, width=4, capstyle="round", fill="#fff")

        # subtitle (typing)
        sub_w = self.sub_font.measure(SUBTITLE)
        self.sub_x = (self.w - sub_w) / 2
        self.sub_y = self.h * 0.66
        self.subtitle = c.create_text(self.sub_x, self.sub_y, text="", anchor="w",
                                       font=self.sub_font, fill="#e8ecff")

        # orbiting orbs
        for i in range(4):
            self.orbs.append(c.create_oval(0, 0, 0, 0, fill="#fff", outline=""))

        # hint
        self.hint = c.create_text(self.w / 2, self.h - 22, text=HINT,
                                   font=self.hint_font, fill="#8d97c9")

    def on_resize(self, event):
        if abs(event.width - self.w) > 2 or abs(event.height - self.h) > 2:
            self.w, self.h = event.width, event.height
            self.sparks.clear()
            self.build_scene()

    # ------------------------------------------------------------------
    def on_click(self, event):
        base_hue = random.random()
        for _ in range(46):
            ang = random.uniform(0, math.tau)
            speed = random.uniform(2.0, 7.5)
            r = random.uniform(2, 4.5)
            item = self.canvas.create_oval(event.x - r, event.y - r, event.x + r, event.y + r,
                                            fill=hsv(base_hue + random.uniform(-0.08, 0.08), 0.85, 1),
                                            outline="")
            self.sparks.append({
                "id": item, "x": event.x, "y": event.y,
                "vx": math.cos(ang) * speed, "vy": math.sin(ang) * speed,
                "life": random.randint(30, 55), "age": 0, "r": r, "hue": base_hue,
            })

    # ------------------------------------------------------------------
    def tick(self):
        if not self.root.winfo_exists():
            return
        self.frame += 1
        f = self.frame
        c = self.canvas

        self.animate_background(f)
        self.animate_stars(f)
        self.animate_title(f)
        self.animate_subtitle(f)
        self.animate_orbs(f)
        self.animate_sparks()

        # keep text above decorations
        c.tag_raise(self.hint)

        self.root.after(FPS_DELAY, self.tick)

    def animate_background(self, f):
        for k, band in enumerate(self.bands):
            t = k / self.BANDS
            hue = 0.62 + 0.10 * math.sin(f * 0.008 + t * 2.4) + 0.05 * t
            val = 0.20 + 0.30 * t
            self.canvas.itemconfig(band, fill=hsv(hue, 0.78, val))

    def animate_stars(self, f):
        for s in self.stars:
            s["y"] -= s["speed"]
            if s["y"] < -5:
                s["y"] = self.h + 5
                s["x"] = random.uniform(0, self.w)
            tw = 0.55 + 0.45 * math.sin(f * 0.07 + s["phase"])
            r = s["r"] * (0.6 + 0.6 * tw)
            self.canvas.coords(s["id"], s["x"] - r, s["y"] - r, s["x"] + r, s["y"] + r)
            self.canvas.itemconfig(s["id"], fill=hsv(s["hue"], 0.25, 0.6 + 0.4 * tw))

    def animate_title(self, f):
        c = self.canvas
        n = len(self.letters)
        all_landed = True
        for i, L in enumerate(self.letters):
            start = 10 + i * 5
            p = (f - start) / 38.0
            if p <= 0:
                all_landed = False
                continue
            c.itemconfigure(L["main"], state="normal")
            c.itemconfigure(L["shadow"], state="normal")

            if p < 1:
                all_landed = False
                y = self.title_y - (1 - ease_out_bounce(p)) * 280
            else:
                y = self.title_y - 11 * math.sin(f * 0.07 + i * 0.55)

            hue = f * 0.0035 + i * 0.045
            c.coords(L["main"], L["x"], y)
            c.coords(L["shadow"], L["x"] + 4, y + 6)
            c.itemconfig(L["main"], fill=hsv(hue, 0.55, 1.0))
            c.itemconfig(L["shadow"], fill=hsv(hue, 0.9, 0.22))

        # underline pulses once letters have landed
        if all_landed:
            pulse = 0.5 + 0.5 * math.sin(f * 0.06)
            half = self.title_total / 2 * (0.55 + 0.45 * pulse)
            cx = self.w / 2
            y = self.title_y + 58
            c.coords(self.underline, cx - half, y, cx + half, y)
            c.itemconfig(self.underline, fill=hsv(f * 0.004 + 0.1, 0.6, 1.0), width=3 + 2 * pulse)
        self.letters_done = all_landed

    def animate_subtitle(self, f):
        start = 10 + len(TITLE) * 5 + 40
        if f < start:
            return
        n = min(len(SUBTITLE), (f - start) // 3)
        cursor = "▌" if (f // 18) % 2 == 0 else " "
        self.canvas.itemconfig(self.subtitle, text=SUBTITLE[:n] + cursor)

    def animate_orbs(self, f):
        if not getattr(self, "letters_done", False):
            return
        cx, cy = self.w / 2, self.title_y + 4
        rx = self.title_total / 2 + 70
        ry = 82
        for i, orb in enumerate(self.orbs):
            ang = f * 0.03 + i * math.tau / len(self.orbs)
            x = cx + math.cos(ang) * rx
            y = cy + math.sin(ang) * ry
            depth = 0.5 + 0.5 * math.sin(ang)
            r = 4 + 4 * depth
            self.canvas.coords(orb, x - r, y - r, x + r, y + r)
            self.canvas.itemconfig(orb, fill=hsv(f * 0.004 + i * 0.25, 0.5, 0.7 + 0.3 * depth))

    def animate_sparks(self):
        alive = []
        for p in self.sparks:
            p["age"] += 1
            if p["age"] >= p["life"]:
                self.canvas.delete(p["id"])
                continue
            p["vy"] += 0.12  # gravity
            p["vx"] *= 0.985
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            k = 1 - p["age"] / p["life"]
            r = p["r"] * (0.4 + 0.6 * k)
            self.canvas.coords(p["id"], p["x"] - r, p["y"] - r, p["x"] + r, p["y"] + r)
            self.canvas.itemconfig(p["id"], fill=hsv(p["hue"] + (1 - k) * 0.1, 0.8 * k + 0.1, 0.4 + 0.6 * k))
            alive.append(p)
        self.sparks = alive


def main():
    root = tk.Tk()
    HelloApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()