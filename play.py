from snake import *
from os import environ


def screen(surface):
    surface.fill(SURFACE_CLR)


def grid(surface):
    a = 0
    b = 0
    for r in range(ROWS):
        a = a + SQUARE_SIZE
        b = b + SQUARE_SIZE
        pygame.draw.line(surface, GRID_CLR, (a, 0), (a, HEIGHT))
        pygame.draw.line(surface, GRID_CLR, (0, b), (WIDTH, b))


def game():
    pygame.init()
    environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption("Our team game")
    game_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    snake = Snake(game_surface)
    loop = True
    while loop:
        screen(game_surface)
        grid(game_surface)
        snake.update()
        clock.tick(FRAMES)
        pygame.display.update()


if __name__ == '__main__':
    game()
