import pygame
import os
import math
import numpy as np
from board import *

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.set_caption('Dots and Boxes AI')
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# top, bottom, left, right
board = np.zeros((n - 1, m - 1, 5), dtype=object)
# -1 human, 1 ai
turn = -1


def draw_dots():
    for i in range(m):
        for j in range(n):
            pygame.draw.circle(screen, BLACK, (i * WIDTH // m + OFFSET, j * HEIGHT // n + OFFSET), 7)


def draw_line(i, j, direction, colour):
    x1 = i * WIDTH // m + OFFSET
    x2 = x1 + WIDTH // m
    y1 = j * HEIGHT // n + OFFSET
    y2 = y1 + HEIGHT // n

    if direction == DIRECTION['top']:
        pygame.draw.line(screen, colour, (x1, y1), (x2, y1), THICC)
    elif direction == DIRECTION['bottom']:
        pygame.draw.line(screen, colour, (x1, y2), (x2, y2), THICC)
    elif direction == DIRECTION['left']:
        pygame.draw.line(screen, colour, (x1, y1), (x1, y2), THICC)
    if direction == DIRECTION['right']:
        pygame.draw.line(screen, colour, (x2, y1), (x2, y2), THICC)


def draw_board():
    global board
    for i in range(m - 1):
        for j in range(n - 1):
            for index, line in enumerate(board[j, i, :4]):
                try:
                    # Check if the lines are drawn
                    if line[0] != 0:
                        draw_line(i, j, index, line[1])
                except TypeError:
                    # line = [drawn, colour]
                    board[j, i, index] = (0, 0)


def colour_box():
    for i in range(m - 1):
        for j in range(n - 1):
            # Check if the box is full
            full = board[j, i][4]
            if full:
                pygame.draw.rect(screen, COLOURS[full * 2],
                                 (i * WIDTH // m + OFFSET + THICC - 1, j * HEIGHT // n + OFFSET + THICC - 1,
                                  WIDTH // m - THICC,
                                  HEIGHT // n - THICC))


def draw_text(size, text, colour, x, y):
    font = pygame.font.SysFont('Comic Sans MS', size)
    text_surface = font.render(text, 1, colour)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def reset():
    global board, turn, playing, winner
    winner = WHITE
    board = np.zeros((n - 1, m - 1, 5), dtype=object)
    draw_board()
    playing = True
    SCORES[1] = 0
    SCORES[-1] = 0
    turn = -1


# Convert board
draw_board()
playing = True
winner = WHITE

while True:
    screen.fill(winner)
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            assert math.fabs(turn) == 1
            if event.button == pygame.BUTTON_LEFT:
                if place_line(board, mouse_pos, turn) and not check_full(board, turn):
                    turn *= -1
            if event.button == pygame.BUTTON_RIGHT:
                reset()

    if playing:
        place_line(board, mouse_pos, turn * 2, True)
        draw_board()
        colour_box()
        draw_dots()
        draw_text(45, f'RED    {SCORES[1]}', RED, WIDTH // 2, HEIGHT - 40)
        draw_text(45, f'BLUE   {SCORES[-1]}', BLUE, WIDTH // 2, HEIGHT - 10)
    if check_board_full(board):
        playing = False
        if SCORES[-1] > SCORES[1]:
            winner = COLOURS[-1]
        elif SCORES[-1] == SCORES[1]:
            winner = WHITE
        else:
            winner = COLOURS[1]

    pygame.display.flip()
