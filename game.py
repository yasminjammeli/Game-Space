import pygame
import sys
import random
from math import *
from pygame import mixer
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((800,600))
pygame.display.set_caption("Menu")


BG = pygame.image.load("assets/Background.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("KnightWarrior-w16n8.otf", size)


def play():
    

    # init pygame
    pygame.init()

    # create screen
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))

    # background
    background = pygame.image.load("background.png")

    # background sound
    mixer.music.load("bg-music.mp3")
    mixer.music.play(-1)

    # Function to increase volume
    def increase_volume(step=0.1):
        current_volume = pygame.mixer.music.get_volume()
        new_volume = min(1.0, current_volume + step)
        pygame.mixer.music.set_volume(new_volume)

    # Function to decrease volume
    def decrease_volume(step=0.1):
        current_volume = pygame.mixer.music.get_volume()
        new_volume = max(0.0, current_volume - step)
        pygame.mixer.music.set_volume(new_volume)

    # title and icon
    pygame.display.set_caption("Space Invaders")
    icon = pygame.image.load("logo.png")
    pygame.display.set_icon(icon)

    # player
    playerImg = pygame.image.load("player.png")
    playerX = 370
    playerY = 480
    playerX_change = 0

    def player(x, y):
        screen.blit(playerImg, (x, y))

    # enemy
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 3

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load("enemy.png"))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(3)
        enemyY_change.append(40)

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    # bullet
    bulletImg = pygame.image.load("bullet.png")
    bulletX = 0
    bulletY = 480
    bulletX_change = 4
    bulletY_change = 8
    bullet_state = "ready"  # we can't see bullet in screen

    def handle_bullets(bullets, playerX, playerY, num_of_enemies):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_sound = mixer.Sound("bull-sound.wav")
                    bullet_sound.play()
                    if len(bullets) < 4:  # Limit the number of active bullets
                        new_bullet = {'x': playerX, 'y': playerY, 'state': 'fire'}
                        bullets.append(new_bullet)
                        if score_value >= 5:  # Allow more bullets when score_value is 6 or greater
                            new_bullet = {'x': playerX - 10, 'y': playerY, 'state': 'fire'}
                            bullets.append(new_bullet)
                            new_bullet = {'x': playerX + 10, 'y': playerY, 'state': 'fire'}
                            bullets.append(new_bullet)

        for bullet in bullets:
            if bullet['state'] == 'fire':
                bullet['y'] -= 8
                bullet_rect = bullet_img.get_rect(topleft=(bullet['x'] + 16, bullet['y'] + 10))
                screen.blit(bullet_img, bullet_rect)

        for bullet in bullets:
            for i in range(num_of_enemies):
                if bullet['state'] == 'fire':
                    enemy_rect = enemyImg[i].get_rect(topleft=(enemyX[i], enemyY[i]))
                    bullet_rect = bullet_img.get_rect(topleft=(bullet['x'] + 16, bullet['y'] + 10))
                    if bullet_rect.colliderect(enemy_rect):
                        bullet['state'] = 'ready'
                        score_value += 1
                        # Additional logic for handling enemy hit by bullet

        bullets[:] = [bullet for bullet in bullets if bullet['y'] > 0]

    def fire_bullet(x, y):
        nonlocal bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))

    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = sqrt((bulletX - enemyX) ** 2 + (bulletY - enemyY) ** 2)
        if distance < 27:
            return True
        else:
            return False

    # score
    score_value = 0
    font = pygame.font.Font("RebellionSquad-ZpprZ.ttf", 28)
    textX = 10
    textY = 10

    def show_score(x, y):
        score = font.render("Score :  " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

    # Load all player images
    player_images = {
        'normal': pygame.image.load("player.png"),  # Original player image
        'updated': pygame.image.load("player_updated.png")  # Updated player image
    }

    # Set the current player image
    current_player_image = 'normal'

    # health
    health_value = 100
    health_font = pygame.font.Font("RebellionSquad-ZpprZ.ttf", 28)

    def show_health():
        health = health_font.render("health  :  " + str(health_value), True, (255, 255, 255))
        screen.blit(health, (10, 50))

    # game over text
    over_font = pygame.font.Font("BruceForeverRegular-X3jd2.ttf", 64)

    def game_over_text():
        over_text = over_font.render("GAME OVER !! ", True, (255, 0, 0))
        screen.blit(over_text, (110, 250))

    def respawn(i):
        enemyX[i] = random.randint(0, 736)
        enemyY[i] = random.randint(50, 150)

    # game loop
    collision = False
    running = True
    game_over = False
    player_updated = False  # Flag to track if player image has been updated

    while running:
        # screen.fill((red,green,blue))
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    bullet_sound = mixer.Sound("bull-sound.wav")
                    bullet_sound.play()
                    if bullet_state == "ready":
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                if event.key == pygame.K_KP_PLUS:
                    increase_volume()
                if event.key == pygame.K_KP_MINUS:
                    decrease_volume()
                if event.key == pygame.K_r and game_over:
                    score_value = 0
                    health_value = 100
                    num_of_enemies = 3
                    playerY = 480
                    for i in range(num_of_enemies):
                        respawn(i)
                    game_over = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # Check if score reaches 5 to update player image
        if score_value == 5 and not player_updated:
            player_updated = True
            # Update player image
            playerImg = pygame.image.load("player_updated.png")
            # You may also need to update the player function if necessary
            player_images['normal'] = playerImg

        # Player movement
        playerX += playerX_change
        if playerX <= -64:  # playerX = 0
            playerX = width - 64  # playerX = 0
        elif playerX >= width:  # playerX = width -64
            playerX = 0
        # enemy movement

        for i in range(num_of_enemies):

            if playerY + 64 > enemyY[i] >= 430 and playerX <= enemyX[i] <= playerX + 55:
                # for j in range(num_of_enemies):
                # enemyY[j] = 2000
                # game_over_text()
                enemyY[i] = 2000
                health_value -= 10
                respawn(i)
                # break

            if 2000 > enemyY[i] > 600:
                respawn(i)

            if health_value == 0:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                game_over = True
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0 or enemyX[i] >= width - 64:
                enemyX_change[i] = -enemyX_change[i]
                enemyY[i] += enemyY_change[i]

            # collision
            if enemyY[i] < playerY - 55:
                collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bullet_sound = mixer.Sound("explosion.wav")
                bullet_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1

                if score_value % 3 == 0:
                    # add new enemy
                    enemyImg.append(pygame.image.load("enemy.png"))
                    enemyX.append(random.randint(0, 736))
                    enemyY.append(random.randint(50, 150))
                    enemyX_change.append(3)
                    enemyY_change.append(40)
                    num_of_enemies += 1
                respawn(i)

            enemy(enemyX[i], enemyY[i], i)

        # bullet movement
        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)
        show_health()
        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(110).render("MAIN   MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 120))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(370, 280),
            text_input="PLAY", font=get_font(80), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(370, 450),
            text_input="QUIT", font=get_font(80), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()