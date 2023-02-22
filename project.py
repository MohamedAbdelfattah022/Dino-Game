import pygame
from sys import exit
from random import randint


# display the player's score
def player_score():
    score = (pygame.time.get_ticks() - initial_score)//100
    user_score_font = pygame.font.Font(None, 30)
    user_score_surface = user_score_font.render(
        f"Score: {score} ", True, "dark grey")
    if score == 100:
        point_sound = pygame.mixer.Sound("sounds\point.wav")
        point_sound.play()
    user_score_surface_box = user_score_surface.get_rect(topleft=(4, 2))
    screen.blit(user_score_surface, user_score_surface_box)
    return score


# display player's score function
def score_message():
    message = pygame.font.Font(None, 30)
    message_surface = message.render(
        f"Your Score: {your_score}", True, "black")
    message_surface_box = message_surface.get_rect(center=(425, 300))
    screen.blit(message_surface, message_surface_box)


# Clouds movement
def clouds_movement():
    Clouds_box.x -= 1.5
    if Clouds_box.right < 0:
        Clouds_box.left = 1000
    screen.blit(Clouds, Clouds_box)


# enemies movement
def enemies_movement(list_of_enemies):
    if list_of_enemies:
        for enemy in list_of_enemies:

            if enemy.bottom == 331:
                enemy.x -= 10
                screen.blit(Cactus_surface, enemy)
            else:
                enemy.x -= 8
                screen.blit(bird_surface, enemy)

        list_of_enemies = [
            enemy for enemy in list_of_enemies if enemy.x > -100]

        return list_of_enemies
    else:
        return []


# Collisions with enemies
def collisions(user, enemies):
    if enemies:
        for enemies_box in enemies:
            if user.colliderect(enemies_box):
                lose_sound = pygame.mixer.Sound('sounds\die.wav')
                lose_sound.play()
                return False
    return True


# Game Over Screen
def GAME_OVER():
    game_over = pygame.image.load("Other/GameOver.png")
    game_over_box = game_over.get_rect(center=(425, 170))
    reset_img = pygame.image.load("Other/Reset.png")
    reset_img_box = reset_img.get_rect(midtop=(425, 200))
    screen.blit(game_over, game_over_box)
    screen.blit(reset_img, reset_img_box)


# dino animation
def dino_animation():
    global player, player_index
    if player_box.bottom < 331:
        player = player_jumping
    else:
        player_index += 0.1
        if player_index >= 2:
            player_index = 0
        player = player_Running[int(player_index)]


# Birds animation
def bird_animation():
    global birds_index, bird_surface
    if event.type == birds_animation_timer:
        if birds_index == 0:
            birds_index = 1
        else:
            birds_index = 0
        bird_surface = birds[birds_index]


pygame.init()
screen = pygame.display.set_mode((800, 400))

# giving a name to our lovely game ^_^
pygame.display.set_caption("Dino runner")

# setting frame rate
clock = pygame.time.Clock()
initial_score = 0
your_score = 0
is_game_active = True
BackGround = pygame.image.load('Other/Track.png')

# clouds initialization and it's rectangle
Clouds = pygame.image.load('Other/Cloud.png')
Clouds_box = Clouds.get_rect(topleft=(800, 100))

# ENEMIES
# el sappar attributes
Cactus = pygame.image.load('Cactus/LargeCactus1.png')
Cactus2 = pygame.image.load('Cactus/LargeCactus2.png')
Cactus3 = pygame.image.load('Cactus/LargeCactus3.png')
Cactus4 = pygame.image.load('Cactus/SmallCactus1.png')
Cactus5 = pygame.image.load('Cactus/SmallCactus2.png')
Cactus6 = pygame.image.load('Cactus/SmallCactus3.png')
Cactus_list = [Cactus, Cactus2, Cactus3, Cactus4, Cactus5, Cactus6]
Cactus_list_index = randint(0, len(Cactus_list))
Cactus_surface = Cactus_list[Cactus_list_index]

# bird attributes
The_bird1 = pygame.image.load('Bird/Bird1.png')
The_bird2 = pygame.image.load('Bird/Bird2.png')
birds = [The_bird1, The_bird2]
birds_index = 0
bird_surface = birds[birds_index]

enemies_boxes_list = []


# player attributes
player_R1 = pygame.image.load("Dino/DinoRun1.png")
player_R2 = pygame.image.load("Dino/DinoRun2.png")
player_Running = [player_R1, player_R2]
player_index = 0
player_jumping = pygame.image.load("Dino/DinoJump.png")
player = player_Running[player_index]
player_box = player.get_rect(midbottom=(100, 331))
player_GRAVITY = 0
jump_sound = pygame.mixer.Sound("sounds/jump.wav")

# ENEMIES RESPAWN
enemies_time = pygame.USEREVENT
pygame.time.set_timer(enemies_time, 1200)

# birds animation speed
birds_animation_timer = pygame.USEREVENT + 1
pygame.time.set_timer(birds_animation_timer, 200)


# the real game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # checking for user's inputs
        if is_game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jump_sound.play()
                if player_box.bottom >= 331:
                    player_GRAVITY = -22
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_game_active = True
                initial_score = pygame.time.get_ticks()

        if is_game_active:
            if event.type == enemies_time:
                if randint(0, 1):
                    enemies_boxes_list.append(Cactus_surface.get_rect(
                        bottomleft=(randint(800, 850), 331)))
                else:
                    enemies_boxes_list.append(The_bird1.get_rect(
                        midleft=(randint(780, 850), 140)))
            # bird Animation
            bird_animation()

    # putting our surfaces to the main screen
    if is_game_active:
        screen.fill("white")
        player_score()
        your_score = player_score()
        screen.blit(BackGround, (0, 300))

        # clouds movement
        clouds_movement()

        # enemies movement
        enemies_boxes_list = enemies_movement(enemies_boxes_list)

        # player
        player_GRAVITY += 1
        player_box.y += player_GRAVITY
        if player_box.bottom >= 331:
            player_box.bottom = 331
        dino_animation()
        screen.blit(player, player_box)

        # collisions
        is_game_active = collisions(player_box, enemies_boxes_list)

    else:
        screen.fill("grey")
        GAME_OVER()
        enemies_boxes_list.clear()
        player_box.midbottom = (100, 331)
        player_GRAVITY = 0
        # display player's score
        score_message()

    pygame.display.update()
    clock.tick(60)
