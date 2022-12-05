import pygame
import random
import math
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

sound_rect = pygame.Rect(760, 10, 24, 24)
music_paused = False

# Title and icon
pygame.display.set_caption("Don't Crash")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('car.png')
playerX = 370
playerY = 510
playerX_change = 0

# Trees
num_of_trees = 11
# treeImg = [pygame.image.load('tree.png')] * num_of_trees
treeImg = []
treeX = []
treeY = []
treeY_change = 0.5
possible_x_places = [10, 74, 138, 202, 266, 330, 394, 458, 522, 586, 650, 714]

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

score_textX = 10
score_textY = 10

is_game_over = False


# Creating Trees
def creating_trees():
    for i in range(num_of_trees):
        treeImg.append(pygame.image.load('tree.png'))
        treeX.append(random.choice(possible_x_places))
        treeY.append(0)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def sound(img):
    screen.blit(img, (760, 10))


def player(x, y):
    screen.blit(playerImg, (x, y))


def tree(x, y, i):
    screen.blit(treeImg[i], (x, y))


def is_collision(treeX, treeY, playerX, playerY):
    distance = math.sqrt(math.pow(treeX - playerX, 2) + (math.pow(treeY - playerY, 2)))
    if distance < 64:
        return True
    return False


creating_trees()

running = True
while running:
    # RGB background
    screen.fill((127, 85, 57))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.6
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.6

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if sound_rect.collidepoint(event.pos):
                music_paused = not music_paused
                if music_paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Check if trees went out of border

    if treeY[0] >= 600:
        score_value += 1
        treeImg = []
        treeX = []
        treeY = []
        creating_trees()

    # Move trees
    for i in range(num_of_trees):
        treeY[i] += treeY_change

        # Collision
        tree_rect = treeImg[i].get_rect(x=treeX[i], y=treeY[i])
        player_rect = playerImg.get_rect(x=playerX, y=playerY)
        if tree_rect.colliderect(player_rect):
            crash_sound = mixer.Sound("crash.wav")
            crash_sound.set_volume(0.7)
            crash_sound.play()
            is_game_over = True
            break

        tree(treeX[i], treeY[i], i)
    if is_game_over:
        game_over_text()
        treeY_change = 0
        num_of_trees = 0

    player(playerX, playerY)
    if music_paused:
        sound(muteImg)
    else:
        sound(soundImg)
    show_score(score_textX, score_textY)
    pygame.display.update()
