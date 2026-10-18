import tkinter as tk
from tkinter import ttk

class DesktopGrid:
    def __init__(self, plan):
        self.plan = plan
        self.w = plan["building"]["width"]
        self.d = plan["building"]["depth"]
        self.rooms = plan["rooms"]
        self.scale = 48
        self.root = tk.Tk()
        self.root.title("Quad-tree Building Grid")
        self.root.geometry("1100x760")
        self.root.minsize(700, 500)

        header = ttk.Frame(self.root, padding=10)
        header.pack(fill="x")
        ttk.Label(header, text="Quad-tree Building Grid", font=("Arial",16,"bold")).pack(side="left")
        ttk.Label(header, text=f"{self.w:g} m × {self.d:g} m | {len(self.rooms)} regions").pack(side="right")

        controls = ttk.Frame(self.root, padding=(10,0,10,8))
        controls.pack(fill="x")
        ttk.Label(controls, text="Zoom").pack(side="left")
        zoom = ttk.Scale(controls, from_=20, to=75, command=self.zoom)
        zoom.set(self.scale)
        zoom.pack(side="left", fill="x", expand=True, padx=10)

        body = ttk.Frame(self.root, padding=10)
        body.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(body, bg="white", highlightthickness=1, highlightbackground="#aaa")
        self.canvas.pack(side="left", fill="both", expand=True)
        panel = ttk.Frame(body, padding=10)
        panel.pack(side="right", fill="y")
        ttk.Label(panel, text="Selected region", font=("Arial",12,"bold")).pack(anchor="w")
        self.info = tk.Text(panel, width=27, height=14, wrap="word", state="disabled")
        self.info.pack(pady=8)
        self.canvas.bind("<Configure>", lambda e: self.draw())
        self.canvas.bind("<Button-1>", self.click)
        self.draw()
        self.root.mainloop()

    def zoom(self, value):
        self.scale = int(float(value))
        self.draw()

    def draw(self):
        if not hasattr(self, "canvas"): return
        c = self.canvas
        c.delete("all")
        margin = 38
        grid_w, grid_h = self.w*self.scale, self.d*self.scale
        cw, ch = max(c.winfo_width(), 300), max(c.winfo_height(), 250)
        ox = max(margin, (cw-grid_w)/2)
        oy = max(margin, (ch-grid_h)/2)
        self.origin = (ox, oy, margin)
        # metre grid
        for x in range(int(self.w)+1):
            px = ox+x*self.scale
            c.create_line(px, oy, px, oy+grid_h, fill="#e5e7eb")
            c.create_text(px, oy+grid_h+14, text=str(x), fill="#555", font=("Arial",8))
        for y in range(int(self.d)+1):
            py = oy+(self.d-y)*self.scale
            c.create_line(ox, py, ox+grid_w, py, fill="#e5e7eb")
            c.create_text(ox-14, py, text=str(y), fill="#555", font=("Arial",8))
        colors = ["#dbeafe","#dcfce7","#fef3c7","#fce7f3","#ede9fe",
                  "#ffedd5","#cffafe","#f3f4f6","#e0e7ff","#fae8ff"]
        for r in self.rooms:
            x0, y0 = ox+r["x"]*self.scale, oy+(self.d-r["y"]-r["depth"])*self.scale
            x1, y1 = x0+r["width"]*self.scale, y0+r["depth"]*self.scale
            tag = f"room{r['id']}"
            c.create_rectangle(x0,y0,x1,y1, fill=colors[(r["id"]-1)%len(colors)],
                               outline="#111827", width=2, tags=(tag,))
            if x1-x0 > 65 and y1-y0 > 40:
                c.create_text((x0+x1)/2,(y0+y1)/2,
                    text=f"{r['name']}\n{r['width']:g} × {r['depth']:g} m",
                    justify="center", font=("Arial",9), tags=(tag,))
        c.create_rectangle(ox,oy,ox+grid_w,oy+grid_h, outline="#111827", width=3)

    def click(self, event):
        item = self.canvas.find_closest(event.x,event.y)
        tags = self.canvas.gettags(item)
        tag = next((t for t in tags if t.startswith("room")), None)
        if not tag: return
        room = next((r for r in self.rooms if f"room{r['id']}" == tag), None)
        if not room: return
        text = (f"{room['name']}\nID: {room['id']}\n"
                f"Position: ({room['x']:g}, {room['y']:g}) m\n"
                f"Width: {room['width']:g} m\nDepth: {room['depth']:g} m\n"
                f"Area: {room['area_m2']:g} m²\nAspect ratio: {room['aspect_ratio']:g}:1")
        self.info.configure(state="normal")
        self.info.delete("1.0","end")
        self.info.insert("1.0",text)
        self.info.configure(state="disabled")

def launch_grid(plan):
    DesktopGrid(plan)
