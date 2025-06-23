import tkinter as tk
import random

# グリッドサイズ
ROWS = 20
COLS = 10
CELL_SIZE = 30

# 色とテトロミノの形
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]]
}

COLORS = {
    'I': 'cyan',
    'O': 'yellow',
    'T': 'purple',
    'S': 'green',
    'Z': 'red',
    'J': 'blue',
    'L': 'orange'
}

class Tetris:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg='black')
        self.canvas.pack()
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.current = None
        self.running = True
        self.spawn_new_piece()
        self.bind_events()
        self.game_loop()

    def spawn_new_piece(self):
        shape_name = random.choice(list(SHAPES.keys()))
        self.current_shape = SHAPES[shape_name]
        self.current_color = COLORS[shape_name]
        self.current_x = COLS // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0
        if self.check_collision(self.current_shape, self.current_x, self.current_y):
            self.running = False
            self.canvas.create_text(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2, text="Game Over", fill="white", font=("Helvetica", 24))

    def bind_events(self):
        self.root.bind("<Left>", lambda e: self.move(-1, 0))
        self.root.bind("<Right>", lambda e: self.move(1, 0))
        self.root.bind("<Down>", lambda e: self.move(0, 1))
        self.root.bind("<Up>", lambda e: self.rotate())

    def game_loop(self):
        if self.running:
            self.move(0, 1)
            self.draw()
            self.root.after(500, self.game_loop)

    def move(self, dx, dy):
        if not self.running:
            return
        new_x = self.current_x + dx
        new_y = self.current_y + dy
        if not self.check_collision(self.current_shape, new_x, new_y):
            self.current_x = new_x
            self.current_y = new_y
        elif dy == 1:  # 落下できない＝固定
            self.lock_piece()
            self.clear_lines()
            self.spawn_new_piece()

    def rotate(self):
        rotated = list(zip(*self.current_shape[::-1]))
        if not self.check_collision(rotated, self.current_x, self.current_y):
            self.current_shape = [list(row) for row in rotated]

    def check_collision(self, shape, x, y):
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    nx, ny = x + j, y + i
                    if nx < 0 or nx >= COLS or ny >= ROWS:
                        return True
                    if ny >= 0 and self.board[ny][nx]:
                        return True
        return False

    def lock_piece(self):
        for i, row in enumerate(self.current_shape):
            for j, cell in enumerate(row):
                if cell:
                    ny = self.current_y + i
                    nx = self.current_x + j
                    if 0 <= ny < ROWS and 0 <= nx < COLS:
                        self.board[ny][nx] = self.current_color

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell is None for cell in row)]
        lines_cleared = ROWS - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [None for _ in range(COLS)])
        self.board = new_board

    def draw(self):
        self.canvas.delete("all")
        # 既存の固定ブロックを描画
        for y in range(ROWS):
            for x in range(COLS):
                color = self.board[y][x]
                if color:
                    self.draw_cell(x, y, color)

        # 現在のピースを描画
        for i, row in enumerate(self.current_shape):
            for j, cell in enumerate(row):
                if cell:
                    x = self.current_x + j
                    y = self.current_y + i
                    if y >= 0:
                        self.draw_cell(x, y, self.current_color)

    def draw_cell(self, x, y, color):
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')


if __name__ == "__main__":
    root = tk.Tk()
    root.title("テトリス")
    game = Tetris(root)
    root.mainloop()
