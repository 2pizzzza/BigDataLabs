import collections
from tkinter import Tk, Canvas

grid = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0]
]


def bfs(start, target, grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    visited = set()
    queue = collections.deque([(start, 0)])
    while queue:
        (x, y), dist = queue.popleft()

        if (x, y) == target:
            return dist

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), dist + 1))

    return -1



class PathFindingUI:
    def __init__(self, master, grid):
        self.master = master
        self.grid = grid
        self.canvas = Canvas(master, width=500, height=500)
        self.canvas.pack()
        self.cell_size = 100
        self.draw_grid()

    def draw_grid(self):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                color = "white" if cell == 0 else "black"
                self.canvas.create_rectangle(
                    j * self.cell_size,
                    i * self.cell_size,
                    (j + 1) * self.cell_size,
                    (i + 1) * self.cell_size,
                    fill=color
                )

    def highlight_path(self, path):
        for (x, y) in path:
            self.canvas.create_rectangle(
                y * self.cell_size,
                x * self.cell_size,
                (y + 1) * self.cell_size,
                (x + 1) * self.cell_size,
                fill="green"
            )


def reconstruct_path(parent_map, end):
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent_map.get(current)
    return path[::-1]


def bfs_with_path(start, target, grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    visited = set()
    queue = collections.deque([start])
    parent_map = {start: None}

    while queue:
        x, y = queue.popleft()

        if (x, y) == target:
            return reconstruct_path(parent_map, target)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
                parent_map[(nx, ny)] = (x, y)

    return []


if __name__ == "__main__":
    start = (0, 0)
    target = (4, 4)
    root = Tk()
    ui = PathFindingUI(root, grid)

    path = bfs_with_path(start, target, grid)

    if path:
        ui.highlight_path(path)
    else:
        print("No path found")

    root.mainloop()
