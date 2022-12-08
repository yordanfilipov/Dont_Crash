import sys
import time

import pygame
import random
from pygame import mixer

clock = pygame.time.Clock()

pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Sound on button
soundImg = pygame.image.load('volume_on.png')

# Mute button
muteImg = pygame.image.load('mute.png')

# New Game button
new_game_img = pygame.image.load('new_game.png')

# Title and icon
pygame.display.set_caption("Don't Crash")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Score
font = pygame.font.Font('freesansbold.ttf', 32)

playerImg = pygame.image.load('car.png')


# Creating Trees
def creating_trees():
    num_of_trees = 11
    tree_img = []
    tree_x = []
    tree_y = []
    possible_x_places = [10, 74, 138, 202, 266, 330, 394, 458, 522, 586, 650, 714]
    for i in range(num_of_trees):
        tree_img.append(pygame.image.load('tree.png'))
        tree_x.append(random.choice(possible_x_places))
        tree_y.append(0)
    return tree_img, tree_x, tree_y, num_of_trees


def show_score(x, y, score_value):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def sound(img):
    screen.blit(img, (760, 10))


def new_game(img):
    screen.blit(img, (620, 10))


def player(x, y):
    screen.blit(playerImg, (x, y))


def tree(x, y):
    screen.blit(pygame.image.load('tree.png'), (x, y))



def main_loop():
    sound_rect = pygame.Rect(760, 10, 24, 24)
    new_game_rect = pygame.Rect(620, 10, 124, 24)

    music_paused = False

    # Player
    player_x = 370
    player_y = 510
    player_x_change = 0

    # Trees
    tree_y_change = 1.3

    score_text_x = 10
    score_text_y = 10

    score_value = 0

    is_game_over = False

    tree_img, tree_x, tree_y, num_of_trees = creating_trees()

    running = True
    while running:
        # RGB background
        screen.fill((127, 85, 57))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                pygame.quit()
                sys.exit()

            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -1.7
                if event.key == pygame.K_RIGHT:
                    player_x_change = 1.7

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_rect.collidepoint(event.pos):
                    music_paused = not music_paused
                    if music_paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                if new_game_rect.collidepoint(event.pos):
                    main_loop()

        player_x += player_x_change
        if player_x <= 0:
            player_x = 0
        elif player_x >= 736:
            player_x = 736

        # Check if trees went out of border

        if tree_y[0] >= 600:
            score_value += 1
            tree_img, tree_x, tree_y, num_of_trees = creating_trees()

        # Move trees
        for i in range(num_of_trees):
            tree_y[i] += tree_y_change

            # Collision
            tree_rect = tree_img[i].get_rect(x=tree_x[i], y=tree_y[i])
            player_rect = playerImg.get_rect(x=player_x, y=player_y)
            if tree_rect.colliderect(player_rect):
                if not music_paused:
                    crash_sound = mixer.Sound("crash.wav")
                    crash_sound.set_volume(0.7)
                    crash_sound.play()
                is_game_over = True
                break

            tree(tree_x[i], tree_y[i])
        if is_game_over:
            game_over_text()
            tree_y_change = 0
            num_of_trees = 0

        player(player_x, player_y)
        if music_paused:
            sound(muteImg)
        else:
            sound(soundImg)
        new_game(new_game_img)
        show_score(score_text_x, score_text_y, score_value)
        pygame.display.update()


main_loop()
