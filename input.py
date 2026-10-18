import argparse
from quadtree import generate_plan
from desktop_view import launch_grid

def main():
    p = argparse.ArgumentParser(description="Interactive quad-tree building grid")
    p.add_argument("--width", type=float, default=12)
    p.add_argument("--depth", type=float, default=10)
    p.add_argument("--rooms", type=int, default=7)
    p.add_argument("--min-size", type=float, default=2)
    p.add_argument("--seed", type=int, default=7)
    a = p.parse_args()
    if min(a.width, a.depth, a.min_size) <= 0 or a.rooms < 1:
        p.error("Dimensions and min-size must be positive; rooms must be >= 1.")
    plan = generate_plan(a.width, a.depth, a.rooms, a.min_size, a.seed)
    launch_grid(plan)
if __name__ == "__main__":
    main()
