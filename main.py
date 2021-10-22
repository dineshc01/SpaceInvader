import pygame
from pygame.constants import KEYUP
import random
import math

pygame.init()

# Create the Display (x-axis=width=800 and y-axis=height=600)
screen = pygame.display.set_mode((800, 600))

#Title and Icon
pygame.display.set_caption("Space Invadors")
# icon = pygame.image.load('game-icon.png')
# pygame.display.set_icon(icon)

# Background image load
background = pygame.image.load('images/background.jpg')

# Player
spaceship = pygame.image.load('images/spaceship.png')
playerX = 370
playerY = 500
player_change = 0

# Enemy
invader = pygame.image.load('images/space-invader-icon.png')
enemyX = random.randint(0, 370)
enemyY = random.randint(0, 150)
enemyX_change = 0.5

# bullet
bullet = pygame.image.load('images/bullet.png')
bulletX = playerX
bulletY = playerY
bulletY_change = 1
bullet_state = "ready"

# Find distance for collision between bullet and enemy


def iscollision(playerX, bulletY, enemyX, enemyY):
    distance = math.sqrt((math.pow((enemyX - playerX), 2)) +
                         (math.pow((enemyY - bulletY), 2)))
    if distance <= 25:
        return True
    else:
        return False

# Find distance for collision between player and enemy for Game Over.


def palyer_enemy_collision(bulletX, playerY, enemyX, enemyY):
    palyer_enemy_distance = math.sqrt((math.pow((enemyX - bulletX), 2)) +
                                      (math.pow((enemyY - playerY), 2)))
    if palyer_enemy_distance <= 31:
        return True
    else:
        return False


# Score Count
score_point = 0


def score(score_point):
    print(score_point)


def player(x, y):
    screen.blit(spaceship, (x, y))


def enemy(x, y):
    screen.blit(invader, (x, y))


def screen_background():
    screen.blit(background, (0, 0))


def bullet_release(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x, y))


# Game Loop
running = True
while running:
    # Screen Back Ground Black
    screen.fill((0, 0, 0))

    # Set the background
    screen_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # KEYDOWN is Press the key and KEYUP is release the hands from the key
        if event.type == pygame.KEYDOWN:
            # If KeyStroke is pressed, check whether its right or left or fire bullet.

            if event.key == pygame.K_LEFT:
                player_change = -1
            if event.key == pygame.K_RIGHT:
                player_change = 1
            if event.key == pygame.K_UP:
                if bullet_state == "ready":
                    # Sets the bullet position in X axis when the player move
                    bulletX = playerX
                    bullet_release(bulletX, bulletY)

        if event.type == KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_change = 0

    # Enable Player movement
    playerX += player_change

    # Set the Boundry for player in X-axis. Considered the size of the Image.
    if playerX <= 0:
        playerX = 0
    elif playerX >= 768:
        playerX = 768

    # Enable Enemy movement
    enemyX += enemyX_change

    # Set the boundry for the Enemy
    if enemyX <= 0:
        enemyX_change = 0.5
        enemyY += 20
    elif enemyX >= 768:
        enemyX_change = -0.5
        enemyY += 20

    # Reset Bullet
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"

    # Fire Bullet
    if bullet_state == "fire":
        bullet_release(bulletX, bulletY)
        bulletY -= bulletY_change

    # Detect Collision
    collision = iscollision(bulletX, bulletY, enemyX, enemyY)
    if collision == True:
        score_point += 1
        score(score_point)
        enemyX = random.randint(0, 370)
        enemyY = random.randint(0, 150)

    palyer_enemy_collide = palyer_enemy_collision(
        bulletX, playerY, enemyX, enemyY)
    if palyer_enemy_collide == True:
        print("Game Over")
        enemyX = random.randint(0, 370)
        enemyY = random.randint(0, 150)

    player(playerX, playerY)
    enemy(enemyX, enemyY)

    pygame.display.update()
