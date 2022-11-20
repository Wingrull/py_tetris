from copy import deepcopy
from random import choice, randrange

import pygame

from game_const import GAME_RES, TILE, W, H, FPS, RES
from game_function import get_record, set_record
from game_objects import figures, field, figure_rect, grid, anim_count, anim_speed, anim_limit

pygame.init()
screen = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)

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
score = 0
lines = 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
main_font = pygame.font.Font('font/font.ttf', 60)
font = pygame.font.Font('font/font2.otf', 35)

score_title = font.render('Current score:', True, pygame.Color('blue'))
tetris_title = main_font.render('TETRIS', True, pygame.Color('yellow'))
record_title = font.render('Record:', True, pygame.Color('blue'))


def get_color():
    return randrange(30, 256), randrange(30, 256), randrange(30, 256)


color, next_color = get_color(), get_color()

while True:
    record = get_record()

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
                for j in range(4):
                    field[figure_old[j].y][figure_old[j].x] = color
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
    score += scores[lines]

    # draw grid
    [pygame.draw.rect(screen, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # draw figure
    for i in range(4):
        if figure:
            figure_rect.x = figure[i].x * TILE
            figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(screen, color, figure_rect)

    # draw field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(screen, col, figure_rect)

    # draw tetris title
    screen.blit(tetris_title, (478, 50))

    # draw score
    screen.blit(record_title, (455, 655))
    screen.blit(font.render(str(record), True, pygame.Color('gold')), (455, 700))

    screen.blit(score_title, (455, 780))
    screen.blit(font.render(str(score), True, pygame.Color('white')), (455, 830))

    # draw next figure
    for i in range(4):
        if next_figure:
            figure_rect.x = next_figure[i].x * TILE + 395
            figure_rect.y = next_figure[i].y * TILE + 400
        pygame.draw.rect(screen, next_color, figure_rect)

    # game over
    for i in range(W):
        if field[0][i]:
            set_record(record, score)
            field = [[0 for j in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(screen, get_color(), i_rect)
                game_sc.blit(screen, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)
