import pygame
import random
import sys

pygame.init()

BLOCK_SIZE = 30
COLUMNS = 10
ROWS = 20
WIDTH = COLUMNS * BLOCK_SIZE
HEIGHT = ROWS * BLOCK_SIZE
FPS = 10

COLORS = [
    (0, 0, 0),
    (0, 255, 255),
    (0, 0, 255),
    (255, 165, 0),
    (255, 255, 0),
    (0, 255, 0),
    (128, 0, 128),
    (255, 0, 0),
]

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 0], [1, 1, 1]],
]

class Piece:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.rotation = 0


def create_grid(locked_positions=None):
    grid = [[(0, 0, 0) for _ in range(COLUMNS)] for _ in range(ROWS)]
    if locked_positions:
        for (x, y), color in locked_positions.items():
            if y >= 0:
                grid[y][x] = color
    return grid


def convert_shape_format(piece):
    positions = []
    form = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(form):
        for j, column in enumerate(line):
            if column == 1:
                positions.append((piece.x + j, piece.y + i))
    return positions


def valid_space(piece, grid):
    accepted_positions = [(j, i) for i in range(ROWS) for j in range(COLUMNS) if grid[i][j] == (0, 0, 0)]
    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] >= 0:
                return False
    return True


def check_lost(positions):
    for x, y in positions:
        if y < 1:
            return True
    return False


def get_shape():
    shape_index = random.randrange(len(SHAPES))
    shape = SHAPES[shape_index]
    rotations = [shape]
    for _ in range(3):
        shape = rotate_shape(shape)
        rotations.append(shape)
    return Piece(COLUMNS // 2 - 2, -1, rotations, COLORS[shape_index + 1])


def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]


def clear_rows(grid, locked):
    inc = 0
    for i in range(ROWS - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            for j in range(COLUMNS):
                try:
                    del locked[(j, i)]
                except KeyError:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            color = locked.pop(key)
            locked[(x, y + inc)] = color
    return inc


def draw_grid(surface, grid):
    for i in range(ROWS):
        for j in range(COLUMNS):
            pygame.draw.rect(surface, grid[i][j], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    for i in range(ROWS):
        pygame.draw.line(surface, (128, 128, 128), (0, i * BLOCK_SIZE), (WIDTH, i * BLOCK_SIZE))
    for j in range(COLUMNS):
        pygame.draw.line(surface, (128, 128, 128), (j * BLOCK_SIZE, 0), (j * BLOCK_SIZE, HEIGHT))


def draw_window(surface, grid):
    surface.fill((0, 0, 0))
    draw_grid(surface, grid)
    pygame.display.update()


def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick(FPS)

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                elif event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True

        shape_positions = convert_shape_format(current_piece)

        for x, y in shape_positions:
            if y >= 0:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_positions:
                x, y = pos
                if y >= 0:
                    locked_positions[(x, y)] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            lines_cleared = clear_rows(grid, locked_positions)

            if check_lost(list(locked_positions)):
                run = False

        draw_window(screen, grid)

    pygame.quit()


if __name__ == '__main__':
    main()
