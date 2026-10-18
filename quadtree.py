import random

LABELS = ["Living room", "Kitchen", "Bedroom", "Bedroom", "Bathroom",
          "Office", "Dining", "Storage", "Utility", "Guest room"]

class Region:
    def __init__(self, x, y, w, d):
        self.x, self.y, self.width, self.depth = x, y, w, d
        self.children = []

def leaves(node):
    if not node.children:
        return [node]
    return [r for child in node.children for r in leaves(child)]

def split(r):
    w, d = r.width / 2, r.depth / 2
    x, y = r.x, r.y
    r.children = [Region(x,y,w,d), Region(x+w,y,w,d),
                  Region(x,y+d,w,d), Region(x+w,y+d,w,d)]

def generate_plan(width=12, depth=10, target_rooms=7, min_size=2, seed=7):
    if width < 2*min_size or depth < 2*min_size:
        raise ValueError("Building width and depth must each be at least twice min-size.")
    rng = random.Random(seed)
    root = Region(0, 0, width, depth)
    rooms = [root]
    while len(rooms) + 3 <= target_rooms:
        possible = [r for r in rooms if r.width >= 2*min_size and r.depth >= 2*min_size]
        if not possible:
            break
        possible.sort(key=lambda r: r.width*r.depth, reverse=True)
        max_area = possible[0].width*possible[0].depth
        possible = [r for r in possible if r.width*r.depth >= .75*max_area]
        split(rng.choice(possible))
        rooms = leaves(root)
    labels = LABELS.copy()
    while len(labels) < len(rooms):
        labels.append(f"Room {len(labels)+1}")
    rng.shuffle(labels)
    result = []
    for i, r in enumerate(rooms, 1):
        result.append({"id":i, "name":labels[i-1], "x":r.x, "y":r.y,
                       "width":r.width, "depth":r.depth,
                       "area_m2":round(r.width*r.depth, 2),
                       "aspect_ratio":round(max(r.width,r.depth)/min(r.width,r.depth), 2)})
    return {"building":{"width":width, "depth":depth}, "rooms":result}
