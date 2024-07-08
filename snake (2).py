import pygame
from face import *
from random import randrange
from copy import deepcopy


class Square:
    def __init__(self, pos, face, food=False):
        self.surface = face
        self.food = food
        self.is_tail = False
        self.pos = pos
        self.dir = [-1, 0]
        if self.food:
            self.dir = [0, 0]

    def paint(self, color=SNAKE_CLR):
        a, b = self.pos[0], self.pos[1]
        s_size, g_size = SQUARE_SIZE, GAP_SIZE
        if self.dir == [-1, 0]:
            if self.is_tail:
                pygame.draw.rect(self.surface, color,
                                 (a * s_size + g_size, b * s_size + g_size, s_size - 2 * g_size, s_size - 2 * g_size))
            else:
                pygame.draw.rect(self.surface, color,
                                 (a * s_size + g_size, b * s_size + g_size, s_size, s_size - 2 * g_size))
        if self.dir == [1, 0]:
            if self.is_tail:
                pygame.draw.rect(self.surface, color,
                                 (a * s_size + g_size, b * s_size + g_size, s_size - 2 * g_size, s_size - 2 * g_size))
            else:
                pygame.draw.rect(self.surface, color,
                                 (a * s_size - g_size, b * s_size + g_size, s_size, s_size - 2 * g_size))
        if self.dir == [0, 1]:
            if self.is_tail:
                pygame.draw.rect(self.surface, color,
                                 (a * s_size + g_size, b * s_size + g_size, s_size - 2 * g_size, s_size - 2 * g_size))
            else:
                pygame.draw.rect(self.surface, color,
                                 (a * s_size + g_size, b * s_size - g_size, s_size - 2 * g_size, s_size))
        if self.dir == [0, -1]:
            if self.is_tail:
                pygame.draw.rect(self.surface, color,
                                 (a * s_size + g_size, b * s_size + g_size, s_size - 2 * g_size, s_size - 2 * g_size))
            else:
                pygame.draw.rect(self.surface, color,
                                 (a * s_size + g_size, b * s_size + g_size, s_size - 2 * g_size, s_size))
        if self.food:
            pygame.draw.rect(self.surface, color,
                             (a * s_size + g_size, b * s_size + g_size, s_size - 2 * g_size, s_size - 2 * g_size))

    def move(self, direction):
        self.dir = direction
        self.pos[0] += self.dir[0]
        self.pos[1] += self.dir[1]

    def hitting_wall(self):
        if (self.pos[0] <= -1) or (self.pos[0] >= ROWS) or (self.pos[1] <= -1) or (self.pos[1] >= ROWS):
            return True
        else:
            return False


class Snake:
    def __init__(self, surface):
        self.surface = surface
        self.is_dead = False
        self.squares_start_pos = [[ROWS // 2 + i, ROWS // 2] for i in range(INITIAL_SNAKE_LENGTH)]
        self.turns = {}
        self.dir = [-1, 0]
        self.score = 0
        self.moves_without_eating = 0
        self.apple = Square([randrange(ROWS), randrange(ROWS)], self.surface, food=True)
        self.squares = []
        for pos in self.squares_start_pos:
            self.squares.append(Square(pos, self.surface))
        self.head = self.squares[0]
        self.tail = self.squares[-1]
        self.tail.is_tail = True
        self.path = []
        self.is_virtual_snake = False
        self.total_moves = 0
        self.won_game = False

    def draw(self):
        self.apple.paint(APPLE_CLR)
        self.head.paint(HEAD_CLR)
        for sqr in self.squares[1:]:
            if self.is_virtual_snake:
                sqr.paint(VIRTUAL_SNAKE_CLR)
            else:
                sqr.paint()

    def set_direction(self, direction):
        if direction == 'left':
            if not self.dir == [1, 0]:
                self.dir = [-1, 0]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "right":
            if not self.dir == [-1, 0]:
                self.dir = [1, 0]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "up":
            if not self.dir == [0, 1]:
                self.dir = [0, -1]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "down":
            if not self.dir == [0, -1]:
                self.dir = [0, 1]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # using keyboard
            keys = pygame.key.get_pressed()
            for _ in keys:
                if keys[pygame.K_LEFT]:
                    self.set_direction('left')

                elif keys[pygame.K_RIGHT]:
                    self.set_direction('right')

                elif keys[pygame.K_UP]:
                    self.set_direction('up')

                elif keys[pygame.K_DOWN]:
                    self.set_direction('down')

    def move(self):
        for j, sqr in enumerate(self.squares):
            p = (sqr.pos[0], sqr.pos[1])
            if p in self.turns:
                turn = self.turns[p]
                sqr.move([turn[0], turn[1]])
                if j == len(self.squares) - 1:
                    self.turns.pop(p)
            else:
                sqr.move(sqr.dir)
        self.moves_without_eating += 1

    def reset(self):
        self.__init__(self.surface)

    def hitting_self(self):
        for sqr in self.squares[1:]:
            if sqr.pos == self.head.pos:
                return True

    def add_square(self):
        self.squares[-1].is_tail = False
        tail = self.squares[-1]  # Tail before adding new square

        direction = tail.dir
        if direction == [1, 0]:
            self.squares.append(Square([tail.pos[0] - 1, tail.pos[1]], self.surface))
        if direction == [-1, 0]:
            self.squares.append(Square([tail.pos[0] + 1, tail.pos[1]], self.surface))
        if direction == [0, 1]:
            self.squares.append(Square([tail.pos[0], tail.pos[1] - 1], self.surface))
        if direction == [0, -1]:
            self.squares.append(Square([tail.pos[0], tail.pos[1] + 1], self.surface))
        self.squares[-1].dir = direction
        self.squares[-1].is_tail = True  # The tail --> + square

    def generate_apple(self):
        self.apple = Square([randrange(ROWS), randrange(ROWS)], self.surface, food=True)
        if not self.is_position_free(self.apple.pos):
            self.generate_apple()

    def eating_apple(self):
        if self.head.pos == self.apple.pos and not self.is_virtual_snake and not self.won_game:
            self.generate_apple()
            self.moves_without_eating = 0
            self.score += 1
            return True

    def is_position_free(self, position):
        # checks if the position square free or not
        if position[0] >= ROWS or position[0] < 0 or position[1] >= ROWS or position[1] < 0:
            return False
        for sqr in self.squares:
            if sqr.pos == position:
                # the given square position could be occupied by another square
                return False
        return True

    def go_to(self, position):  # Set head direction to target position
        if self.head.pos[1] - 1 == position[1]:
            self.set_direction('up')
        if self.head.pos[1] + 1 == position[1]:
            self.set_direction('down')
        if self.head.pos[0] - 1 == position[0]:
            self.set_direction('left')
        if self.head.pos[0] + 1 == position[0]:
            self.set_direction('right')

    def bfs(self, start, end):  # the shortest path : start and end
        queue = [start]
        visited = {tuple(pos): False for pos in GRID}
        visited[start] = True
        # Previous --> parent node of each node
        prev = {tuple(pos): None for pos in GRID}
        while queue:  # not empty
            node = queue.pop(0)
            neighbors = ADJACENCY_DICT[node]
            for next_node in neighbors:
                if self.is_position_free(next_node) and not visited[tuple(next_node)]:
                    queue.append(tuple(next_node))
                    visited[tuple(next_node)] = True
                    prev[tuple(next_node)] = node
        path = list()
        parent_node = end  # end node -->  find the parent node
        start_node_found = False
        while not start_node_found:
            if prev[parent_node] is None:
                return []
            parent_node = prev[parent_node]
            if parent_node == start:
                path.append(end)
                return path
            path.insert(0, parent_node)
        return []  # the path is not available

    def dfs(self, end, start):
        stack = [end]
        visited = {tuple(pos): False for pos in GRID}
        visited[end] = True
        # Previous --> parent node of each node
        prev = {tuple(pos): None for pos in GRID}
        #dead = False
        while stack:  # not empty
            node = stack.pop(0)
            neighbors = ADJACENCY_DICT[node]
            for next_node in neighbors:
                if self.is_position_free(next_node) and not visited[tuple(next_node)]:
                    stack.append(tuple(next_node))
                    visited[tuple(next_node)] = True
                    prev[tuple(next_node)] = node
        path = list()
        parent_node = start  # start node -->  find the parent node
        end_node_found = False
        while not end_node_found:
            if prev[parent_node] is None:
                return []
            parent_node = prev[parent_node]
            if parent_node == end:
                path.append(start)
                return path
            path.insert(0, parent_node)
        return []  # the path is not available

    def get_path_to_tail(self):
        # return the path from the head of a list to its tail.
        tail_pos = deepcopy(self.squares[-1].pos)
        self.squares.pop(-1)
        path = self.dfs(tuple(self.head.pos), tuple(tail_pos))
        path = self.bfs(tuple(self.head.pos), tuple(tail_pos))
        self.add_square()
        # to make a complete path from the head to tail
        return path

    def create_v_snake(self):  # copy of snake
        v_snake = Snake(self.surface)
        for i in range(len(self.squares) - len(v_snake.squares)):
            v_snake.add_square()
        for i, sqr in enumerate(v_snake.squares):
            sqr.pos = deepcopy(self.squares[i].pos)
            sqr.dir = deepcopy(self.squares[i].dir)
        v_snake.dir = deepcopy(self.dir)
        v_snake.turns = deepcopy(self.turns)
        v_snake.apple.pos = deepcopy(self.apple.pos)
        v_snake.apple.food = True
        v_snake.is_virtual_snake = True
        return v_snake

    def available_neighbors(self, pos):
        valid_neighbors = []
        neighbors = get_neighbors(tuple(pos))
        for n in neighbors:
            if self.is_position_free(n) and self.apple.pos != n:
                valid_neighbors.append(tuple(n))
        return valid_neighbors

    def longest_tail(self):
        neighbors = self.available_neighbors(self.head.pos)
        path = []
        if neighbors:
            dis = -9999
            for n in neighbors:
                if distance(n, self.squares[-1].pos) > dis:
                    v_snake = self.create_v_snake()
                    v_snake.go_to(n)
                    v_snake.move()
                    if v_snake.eating_apple():
                        v_snake.add_square()
                    if v_snake.get_path_to_tail():
                        path.append(n)
                        dis = distance(n, self.squares[-1].pos)
            if path:
                return [path[-1]]

    def any_safe_move(self):
        neighbors = self.available_neighbors(self.head.pos)
        path = []
        if neighbors:
            path.append(neighbors[randrange(len(neighbors))])
            v_snake = self.create_v_snake()
            for move in path:
                v_snake.go_to(move)
                v_snake.move()
            if v_snake.get_path_to_tail():
                return path
            else:
                return self.get_path_to_tail()

    def set_path(self):
        # food -->  win , it's adjacent to head
        if self.score == SNAKE_MAX_LENGTH - 1 and self.apple.pos in get_neighbors(self.head.pos):
            winning_path = [tuple(self.apple.pos)]
            print('Your snake is about to win..')
            return winning_path
        v_snake = self.create_v_snake()
        # V_snake --> path : food is available
        path_1 = v_snake.dfs(tuple(v_snake.head.pos), tuple(v_snake.apple.pos))
        path_1 = v_snake.bfs(tuple(v_snake.head.pos), tuple(v_snake.apple.pos))
        # path to v_snake tail --> following path_1
        path_2 = []
        if path_1:
            for pos in path_1:
                v_snake.go_to(pos)
                v_snake.move()
            v_snake.add_square()  # Because it will eat an apple
            path_2 = v_snake.get_path_to_tail()
        # v_snake.draw()
        if path_2:  # path : v_snake, tail
            return path_1  # BFS --> fast , short
        # path_1 , path_2  are not available : the longest path to tail is available
            # score is even --> longest_path_to_tail() and if odd --> any_safe_move()
            # tail method --> snake gets stuck
        if self.longest_tail() and\
                self.score % 2 == 0 and\
                self.moves_without_eating < MAX_MOVES_WITHOUT_EATING / 2:
            return self.longest_tail()  # the longest path to tail
        # possible safe move
        # path to tail is available
        if self.any_safe_move():
            return self.any_safe_move()
        # is available?
        if self.get_path_to_tail():
            # The shortest path
            return self.get_path_to_tail()    # Cannot find a path ,die
        print('There is no available path, your snake is in danger!')

    def update(self):
        self.handle_events()
        self.path = self.set_path()
        if self.path:
            self.go_to(self.path[0])
        self.draw()
        self.move()
        if self.score == ROWS * ROWS - INITIAL_SNAKE_LENGTH:  # win the game
            self.won_game = True
            print("The snake won the game"
                  .format(self.total_moves))
            pygame.time.wait(1000 * WAIT_SECONDS_AFTER_WIN)
            return 1
        self.total_moves += 1
        if self.hitting_self() or self.head.hitting_wall():
            print("The snake is dead")
            self.is_dead = True
            self.reset()
        if self.moves_without_eating == MAX_MOVES_WITHOUT_EATING:
            self.is_dead = True
            print("The snake got stuck")
            self.reset()
        if self.eating_apple():
            self.add_square()