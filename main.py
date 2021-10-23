import pygame
from pygame.constants import KEYUP
import random
import math

pygame.init()

# Create the Display (x-axis=width=800 and y-axis=height=600)
screen = pygame.display.set_mode((800, 600))

#Title and Icon
pygame.display.set_caption("Space Invadors")
# icon = pygame.image.load('images/game-icon.png')
# pygame.display.set_icon(icon)

# Background image load
background = pygame.image.load('images/background.jpg')


# Background Music
pygame.mixer.music.load('music/background.wav')
pygame.mixer.music.play(-1)

# Player
spaceship = pygame.image.load('images/spaceship.png')
playerX = 370
playerY = 500
player_change = 0

# Enemy list
invader = []
enemyX = []
enemyY = []
enemyX_change = []
enemy_number = 6

# Draw enemny fubction
def enemy(invader, x, y):
    screen.blit(invader, (x, y))


# append objects in the list
for i in range(enemy_number):
    invader.append(pygame.image.load('images/space-invader-icon.png'))
    enemyX.append(random.randint(0, 370))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(0.5)


# bullet
bullet = pygame.image.load('images/bullet.png')
bulletX = playerX
bulletY = playerY
bulletY_change = 2
bullet_state = "ready"

# Find distance for collision between bullet and enemy


def iscollision(playerX, bulletY, enemyX, enemyY):
    distance = math.sqrt((math.pow((enemyX - playerX), 2)) +
                         (math.pow((enemyY - bulletY), 2)))
    if distance <= 25:
        return True
    else:
        return False


# Score Count
score_point = 0

font = pygame.font.Font('fonts/hound.ttf', 25)
scoreX = 10
scoreY = 10


# Game Over
game_over_font = pygame.font.Font('fonts/hound.ttf', 50)
game_overX = 250
game_overY = 250


def score(x, y):
    score_display = font.render(
        "Score : " + str(score_point), True, (255, 255, 255))
    screen.blit(score_display, (x, y))


def game_over(x, y):
    game_over_display = game_over_font.render(
        "GAME OVER", True, (255, 125, 125))
    screen.blit(game_over_display, (x, y))


def player(x, y):
    screen.blit(spaceship, (x, y))


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
                player_change = -2
            if event.key == pygame.K_RIGHT:
                player_change = 2
            if event.key == pygame.K_UP:
                if bullet_state == "ready":
                    # Sets the bullet position in X axis when the player move
                    bullet_release_sound = pygame.mixer.Sound(
                        'music/laser.wav')
                    bullet_release_sound.play()

                    bulletX = playerX
                    bullet_release(bulletX, bulletY)

        if event.type == KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_change = 0

    for i in range(enemy_number):
        enemyX[i] += enemyX_change[i]

        # Set the boundry for the Enemy
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += 20
        elif enemyX[i] >= 768:
            enemyX_change[i] = -0.5
            enemyY[i] += 20

        # Gane Over
        elif enemyY[i] >= 460:
            for j in range(enemy_number):
                enemyY[j] = 2000
            game_over(game_overX, game_overY)
            break

        enemy(invader[i], enemyX[i], enemyY[i])
        collision = iscollision(bulletX, bulletY, enemyX[i], enemyY[i])
        if collision == True:
            bullet_enemy_collision_sound = pygame.mixer.Sound(
                'music/explosion.wav')
            bullet_enemy_collision_sound.play()

            score_point += 1
            enemyX[i] = random.randint(0, 370)
            enemyY[i] = random.randint(0, 150)
    # Enable Player movement
    playerX += player_change

    # Set the Boundry for player in X-axis. Considered the size of the Image.
    if playerX <= 0:
        playerX = 0
    elif playerX >= 768:
        playerX = 768

    # Enable Enemy movement

    # Reset Bullet
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"

    # Fire Bullet
    if bullet_state == "fire":
        bullet_release(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    score(scoreX, scoreY)
    pygame.display.update()
