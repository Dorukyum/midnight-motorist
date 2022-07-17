from os import environ
from random import randint

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

from utils import load_image, render_text

Position = list[float]

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1440, 810))
pygame.display.set_caption("Midnight Motorist")

pygame.mixer.music.load("assets/soundtrack.mp3")  # by NASisawesome10 on SoundCloud
pygame.mixer.music.play(-1)

font = pygame.font.SysFont("timesnewroman", 40)


BG_POS: list[list[float]] = [[0, 0], [1440, 0]]
background = load_image("background.png")


def blit_background(speed: float) -> None:
    if BG_POS[0][0] <= 0:
        BG_POS[0], BG_POS[1] = BG_POS[1], BG_POS[0]
        BG_POS[0][0] = 1440
    BG_POS[0][0] -= speed
    BG_POS[1][0] -= speed
    screen.blit(background, BG_POS[0])
    screen.blit(background, BG_POS[1])


purple_car = load_image("purple_car.png")
pink_car = load_image("pink_car.png")
pygame.display.set_icon(pink_car)
x, y = 60, 375

GAME_SPEED = 1
MAX_GAME_SPEED = 30
X_SPEED = 10
Y_SPEED = 15


purple_cars = []
time = 0.0
highest_time = 0.0


def blit_purple_car(pos: Position) -> None:
    if pos[1] > 362:  # going left
        pos[0] -= 3
        screen.blit(pygame.transform.flip(purple_car, True, False), pos)
    else:  # going right
        pos[0] += 3
        screen.blit(purple_car, pos)


def blit_purple_cars(cars: list[Position], speed: float, pink_pos: Position):
    new_cars = []
    if randint(1, 10) == 1:  # 10% chance to create new car
        pos = [1440 - speed, randint(10, 737)]
        blit_purple_car(pos)
        new_cars.append(pos)

    crash = False
    for pos in cars:
        pos[0] -= speed

        if not crash:
            x, r, y, b = pos[0], pos[0] + 85, pos[1], pos[1] + 63
            if crash := (x < pink_pos[0] < r or x < pink_pos[0] + 85 < r) and (
                y < pink_pos[1] < b or y < pink_pos[1] + 63 < b
            ):
                continue

        if pos[0] >= -85:
            blit_purple_car(pos)
            new_cars.append(pos)

    return crash, new_cars


while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and y >= 0:
        y -= Y_SPEED
    elif keys[pygame.K_DOWN] and not y >= 740:
        y += Y_SPEED
    if keys[pygame.K_RIGHT] and x <= 1355:
        x += X_SPEED
    elif keys[pygame.K_LEFT] and x >= X_SPEED:
        x -= X_SPEED

    if GAME_SPEED < MAX_GAME_SPEED:
        GAME_SPEED += 0.25

    blit_background(GAME_SPEED)
    crash, purple_cars = blit_purple_cars(purple_cars, GAME_SPEED, [x, y])
    if crash:
        time = 0.0
        GAME_SPEED = 1
    screen.blit(pink_car, (x, y))

    time += 0.03
    if time > highest_time:
        highest_time = max(time, highest_time)
    screen.blit(
        render_text(f"Current: {time:.2f}s | Highest: {highest_time:.2f}s"),
        (20, 20),
    )

    pygame.display.update()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
