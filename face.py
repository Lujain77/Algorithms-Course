# The dimensions
WIDTH = 500
HEIGHT = 500
ROWS = 12
SQUARE_SIZE = WIDTH // ROWS
GAP_SIZE = 2  # the gap --> adjacent squares

# The Colors
SURFACE_CLR = (240, 255, 255)
SNAKE_CLR = (205, 96, 144)
APPLE_CLR = (139, 35, 35)
HEAD_CLR = (139, 58, 98)
GRID_CLR = (8, 8, 8)
VIRTUAL_SNAKE_CLR = (255, 0, 0)

# Some more things
FRAMES = 35  # The frames _ second
INITIAL_SNAKE_LENGTH = 3
AFTER_WIN = 10
MAX_MOVES_WITHOUT_EATING = ROWS * ROWS * ROWS * 2
SNAKE_MAX_LENGTH = ROWS * ROWS - INITIAL_SNAKE_LENGTH

GRID = [[i, j] for i in range(ROWS) for j in range(ROWS)]


def distance(pos1, pos2):
    a1, a2 = pos1[0], pos2[0]
    b1, b2 = pos1[1], pos2[1]
    return abs(a2 - a1) + abs(b2 - b1)


def get_neighbors(position):
    neighbors = [[position[0] + 1, position[1]], [position[0] - 1, position[1]], [position[0], position[1] + 1],
                 [position[0], position[1] - 1]]
    in_grid_neighbors = []
    for pos in neighbors:
        if pos in GRID:
            in_grid_neighbors.append(pos)
    return in_grid_neighbors


ADJACENCY_DICT = {tuple(pos): get_neighbors(pos) for pos in GRID}
