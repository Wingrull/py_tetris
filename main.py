from copy import deepcopy
from random import choice

import pygame
from pygame.color import Color

from game_const import GAME_RES, TILE, W, H, FPS
from game_objects import figures, field, figure_rect, grid, anim_count, anim_speed, anim_limit

pygame.init()
screen = pygame.display.set_mode(GAME_RES)
clock = pygame.time.Clock()

pygame.display.set_caption("py_tetris")
speed = 1


def check_borders() -> bool:
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))


def get_color() -> Color:
    return pygame.Color("white")


color, next_color = get_color(), get_color()

while True:
    dx = 0
    rotate = False
    dy = 1 * speed
    screen.fill(pygame.Color("black"))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            if event.key == pygame.K_RIGHT:
                dx = 1
            if event.key == pygame.K_DOWN:
                anim_limit = 100
            if event.key == pygame.K_UP:
                rotate = True

    # move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break

    # move y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_limit = 2000
                break

    # rotate
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break

    # check lines
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

    # draw grid
    [pygame.draw.rect(screen, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # draw figure
    for i in range(4):
        if figure:
            figure_rect.x = figure[i].x * TILE
            figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(screen, pygame.Color("white"), figure_rect)

    # draw field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(screen, col, figure_rect)

    # game over
    for i in range(W):
        if field[0][i]:
            field = [[0 for j in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(screen, get_color(), i_rect)
                screen.blit(screen, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)
