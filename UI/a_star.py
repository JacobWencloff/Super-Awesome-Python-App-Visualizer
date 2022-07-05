from ast import Lambda
import pygame
import math
from queue import PriorityQueue
import imgui

# WIDTH = 800
# WIN = pygame.display.set_mode((WIDTH,WIDTH))
# pygame.display.set_caption('A* Path Finding')

RED =       (1,0,0,1)
GREEN =     (0,1,0,1)
BLUE =      (0,0,1,1)
YELLOW =    (1,1,0,1)
WHITE =     (1,1,1,1)
BLACK =     (0,0,0,1)
PURPLE =    ( 0.5, 0, 0.5, 1)
ORANGE =    (1,0.6,0,1)
GREY =      (0.5,0.5,0.5,1)
TURQUOISE = (0.25,0.86,0.78,1)


class Spot():
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK
        
    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win, rows, width, pos):
        gap = width // rows

        x = (self.x * gap) + pos[0]
        y = (self.y * gap) + pos[1]

        end_x = x + gap
        end_y = y + gap
        # pygame.draw.rect(WIN, self.color, (self.x, self.y, self.width, self.width))

        col_t = self.color
        color = imgui.get_color_u32_rgba(col_t[0], col_t[1], col_t[2], col_t[3])
        imgui.get_window_draw_list().add_rect_filled(x, y, end_x, end_y, color)

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

  


class a_star_build():
    def __init__(self, window_width = 50) -> None:
        self.ROWS = 50
        self.width = window_width
        self.grid = self.make_grid(self.ROWS, self.width)

        self.start = None
        self.end = None

        self.run = True
        self.started = False

    def h(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1-x2) + abs(y1-y2)

    def reconstruct_path(self, came_from, current, win, grid, rows, width, pos):
        while current in came_from:
            current = came_from[current]
            current.make_path()
            self.draw(win, grid, rows, width ,pos)
# self.algorithm( self.grid, self.start, self.end, win, self.ROWS, width, pos)
    def algorithm(self, grid, start, end, win, rows, width, pos):
        

        # while not open_set.empty():

        self.current = self.open_set.get()[2]
        self.open_set_hash.remove(self.current)

        if self.current == end:
            self.reconstruct_path(self.came_from, end, win, grid, rows, width ,pos)
            self.started = False
            return True

        for neighbor in self.current.neighbors:
            temp_g_score = self.g_score[self.current] + 1

            if temp_g_score < self.g_score[neighbor]:
                self.came_from[neighbor] = self.current
                self.g_score[neighbor] = temp_g_score
                self.f_score[neighbor] = temp_g_score + self.h(neighbor.get_pos(), end.get_pos())
                if neighbor not in self.open_set_hash:
                    self.count += 1
                    self.open_set.put((self.f_score[neighbor], self.count, neighbor))
                    self.open_set_hash.add(neighbor)
                    neighbor.make_open()
        self.draw(win, grid, rows, width ,pos)

        if self.current != start:
            self.current.make_closed()


    def make_grid(self ,rows, width):
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Spot(i, j, gap, rows)
                grid[i].append(spot)
        
        return grid

    def draw_grid(self, win, rows,width, pos):
        x_off, y_off = pos[0], pos[1]
        gap = width // rows
        for i in range(rows):
            # pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
            imgui.get_window_draw_list().add_line(x_off, y_off + i * gap, x_off + width, y_off + i * gap, imgui.get_color_u32_rgba(0,0,0,1))
            for j in range(rows):
                # pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
                imgui.get_window_draw_list().add_line(x_off + j * gap, y_off, x_off + j * gap, y_off + width,imgui.get_color_u32_rgba(0,0,0,1))

    def draw(self, win, grid, rows, width, pos):
        # win.fill(WHITE)
        for row in grid:
            for spot in row:
                spot.draw(win, rows, width, pos)

        self.draw_grid(win, rows, width, pos)
        # pygame.display.update()

    def get_clicked_pos(self, pos, rows, width):
        gap = width // rows
        y, x = pos

        row = y // gap
        col = x // gap

        return row, col

    def main(self, win, width, pos):
        # self.ROWS = 50
        # self.grid = self.make_grid(self.ROWS, width)

        # self.start = None
        # self.end = None

        # self.run = True
        # self.started = False
        if self.run:
            if self.started:
                self.algorithm( self.grid, self.start, self.end, win, self.ROWS, width, pos)
                
            else:
                self.draw(win, self.grid, self.ROWS, width, pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


                if pygame.mouse.get_pressed()[0]:
                    m_pos = pygame.mouse.get_pos() 
                    adj_m_pos = (int(m_pos[0]-pos[0]), int(m_pos[1]-pos[1]))
                    row, col = self.get_clicked_pos(adj_m_pos, self.ROWS, width)
                    if (row < 0 or col < 0) or (row > self.ROWS or col > self.ROWS):
                        break
                    spot = self.grid[row][col]
                    if not self.start and spot != self.end:
                        self.start = spot
                        self.start.make_start()
                    elif not self.end and spot != self.start:
                        self.end = spot
                        self.end.make_end()
                    elif spot != self.end and spot != self.start:
                        spot.make_barrier()

                elif pygame.mouse.get_pressed()[2]:
                    m_pos = pygame.mouse.get_pos() 
                    adj_m_pos = (int(m_pos[0]-pos[0]), int(m_pos[1]-pos[1]))
                    row, col = self.get_clicked_pos(adj_m_pos, self.ROWS, width)
                    if (row < 0 or col < 0) or (row > self.ROWS or col > self.ROWS):
                        break
                    spot = self.grid[row][col]
                    spot.reset()
                    if spot == self.start:
                       self.start = None
                    elif spot == self.end:
                        self.end == None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.started:
                        for row in self.grid:
                            for spot in row:
                                spot.update_neighbors(self.grid)
                            self.started = True
                        
                        self.count = 0
                        self.open_set = PriorityQueue()
                        self.open_set.put((0, self.count, self.start))
                        self.came_from = {}
                        self.g_score = {spot: float("inf") for row in self.grid for spot in row}
                        self.g_score[self.start] = 0
                        self.f_score = {spot: float("inf") for row in self.grid for spot in row}
                        self.f_score[self.start] = self.h(self.start.get_pos(), self.end.get_pos())

                        self.open_set_hash = {self.start}
                        # self.algorithm( self.grid, self.start, self.end, win, self.ROWS, width, pos)
                
                    if event.key == pygame.K_c:
                        self.__init__()

# x = a_star_build()

# x.main()