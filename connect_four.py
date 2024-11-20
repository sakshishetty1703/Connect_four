import pygame
import numpy as np
import sys

# Constants
ROWS = 6
COLUMNS = 7
SQUARESIZE = 100
RADIUS = SQUARESIZE // 2 - 5
WIDTH = COLUMNS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Initialize pygame
pygame.init()
FONT = pygame.font.SysFont("monospace", 50)

def create_board():
    return np.zeros((ROWS, COLUMNS))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROWS - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r, c + i] == piece for i in range(4)):
                return True

    # Check vertical locations
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r + i, c] == piece for i in range(4)):
                return True

    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i, c + i] == piece for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i, c + i] == piece for i in range(4)):
                return True

    return False

def draw_board(board):
    for r in range(ROWS):
        for c in range(COLUMNS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (c * SQUARESIZE + SQUARESIZE // 2, (r + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS)

            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (c * SQUARESIZE + SQUARESIZE // 2, HEIGHT - (r + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (c * SQUARESIZE + SQUARESIZE // 2, HEIGHT - (r + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS)

    pygame.display.update()

# Main Game Loop
board = create_board()
game_over = False
turn = 0

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Connect Four")
draw_board(board)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
            x_pos = event.pos[0]
            color = RED if turn == 0 else YELLOW
            pygame.draw.circle(screen, color, (x_pos, SQUARESIZE // 2), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
            x_pos = event.pos[0]
            col = x_pos // SQUARESIZE

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                piece = 1 if turn == 0 else 2
                drop_piece(board, row, col, piece)

                if winning_move(board, piece):
                    color = RED if turn == 0 else YELLOW
                    label = FONT.render(f"Player {turn + 1} wins!", True, color)
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    pygame.time.wait(3000)
                    game_over = True

                draw_board(board)
                turn = (turn + 1) % 2

    if game_over:
        pygame.quit()
