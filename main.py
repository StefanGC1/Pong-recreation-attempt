import pygame, sys, random, os
from scorefont import Score


def resource_path(relative_path):  # ??? Something to fix executable compiling issues
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def ball_anim():  # Ball logic
    global player_score, enemy_score, countdown_timer

    if ball.left <= 0:  # Border Collision check
        enemy_score += 1
        countdown_timer = pygame.time.get_ticks()
        score_sound.play()
    if ball.left >= screen_width:
        player_score += 1
        countdown_timer = pygame.time.get_ticks()
        score_sound.play()


    if ball.colliderect(player) and speed[0] < 0:  # Collision check
        #speed[0] = -speed[0]
        if abs(player.right - ball.left) < 8:
            speed[0] = -speed[0]
            bounce_sound.play()
        if (abs(player.top - ball.bottom) < 10 and speed[1] > 0) or (abs(player.bottom - ball.top) < 10 and speed[1] < 0):
            speed[1] = -speed[1]
            bounce_sound.play()

    if ball.colliderect(enemy) and speed[0] > 0:  # Collision check
        # speed[0] = -speed[0]
        if abs(enemy.left - ball.right) < 8:
            speed[0] = -speed[0]
            bounce_sound.play()
        if (abs(enemy.top - ball.bottom) < 10 and speed[1] > 0) or (abs(enemy.bottom - ball.top) < 10 and speed[1] < 0):
            speed[1] = -speed[1]
            bounce_sound.play()

    if ball.top <= 0 or ball.bottom >= screen_height:
        speed[1] = -speed[1]

    ball.centerx += speed[0]
    ball.centery += speed[1]


def player_anim():  # A bit of player object logic
    global player_speed
    player.centery += player_speed
    if player.bottom > screen_height:  # Collision check
        #player_speed = 0
        player.y = screen_height - 180
    if player.top < 0:
        #player_speed = 0
        player.y = 0


def enemy_ai():  # Enemy object logic
    global enemy_speed
    counter = 0
    rand_number = 0
    counter += 1
    if counter == 0:
        # This gets a random delay for the enemy AI with a 1/4 it gets a bad delay
        rand_number = random.choice([random.randrange(100, 200),random.randrange(150, 250),random.randrange(150, 300),random.randrange(320, 450)])
    # enemy.centery += enemy_speed


    if ball.centerx > screen_width / 2 + rand_number:  # Enemy AI
        if enemy.centery + 25 <= ball.centery:
            enemy.centery += enemy_speed
        if enemy.centery - 25 >= ball.centery:
            enemy.centery -= enemy_speed

    if ball.centerx < screen_width:  # This is to make sure the random number is fixed once it crosses into enemy territory
        counter = 0
    if enemy.bottom > screen_height:
        # player_speed = 0
        enemy.y = screen_height - 180
    if enemy.top < 0:
        # player_speed = 0
        enemy.y = 0


def game_start():  # Restart function
    global speed, countdown_timer
    ball.center = (screen_width/2, screen_height/2)
    current_time = pygame.time.get_ticks()

    if current_time - countdown_timer < 700:
        number_three = countdown_font.render("3", False, (218, 218, 218))
        screen.blit(number_three, (screen_width / 2 - 7.5, screen_height / 2 + 20))
    if 700 < current_time - countdown_timer < 1400:
        number_two = countdown_font.render("2", False, (218, 218, 218))
        screen.blit(number_two, (screen_width / 2 - 7.5, screen_height / 2 + 20))
    if 1400 < current_time - countdown_timer < 2100:
        number_one = countdown_font.render("1", False, (218, 218, 218))
        screen.blit(number_one, (screen_width / 2 - 7.5, screen_height / 2 + 20))

    if current_time - countdown_timer < 2100:
        speed = [0, 0]
    else:
        speed[0] = random.choice([-1, 1]) * 8
        speed[1] = random.choice([-1, 1]) * 8
        countdown_timer = None  # This gets set to None so the if statement in the game loop is false and the game can start


# Initialisation
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
pygame.mixer.init()

# Screen info
screen_width = 1280
screen_height = 960
bg_color = pygame.Color("gray10")
light_grey = pygame.Color("gray70")

# Screen creation
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Object / Rect. Variables
ball = pygame.Rect(screen_width/2 - 12.5, screen_height/2 - 12.5, 25, 25)
player = pygame.Rect(10, screen_height/2 - 90, 15, 180)
enemy = pygame.Rect(screen_width - 25, screen_height/2 - 90, 15, 180)

# Speed Variables
speed = [random.choice([-1, 1]) * 8, random.choice([-1, 1]) * 8]
player_speed = 0
enemy_speed = 6

# Score / Text Variables
countdown_font = pygame.font.SysFont('freesansbold.ttf', 30)
player_score = 0
player_score_render = Score(player_score, (screen_width / 2 - 20, screen_height / 2 - 150))
enemy_score = 0
enemy_score_render = Score(player_score, (screen_width / 2 + 20, screen_height / 2 - 150))

# Sound Variables
scs_url = resource_path("score.ogg")
score_sound = pygame.mixer.Sound(scs_url)
score_sound.set_volume(0.7)
bnc_url = resource_path("bounce.ogg")
bounce_sound = pygame.mixer.Sound(bnc_url)
bounce_sound.set_volume(0.7)

# Start Timer
countdown_timer = True

while True:  # Game Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYUP:  # Checking for key release
            player_speed = 0
        if event.type == pygame.KEYDOWN:  # Checking for key press
            if event.key == pygame.K_DOWN:
                player_speed += 6
            if event.key == pygame.K_UP:
                player_speed -= 6


    # Calling the object logic functions
    player_anim()
    enemy_ai()
    ball_anim()


    # Drawing on the screen
    screen.fill(bg_color)
    player_score_render.update(player_score, screen)
    enemy_score_render.update(enemy_score, screen)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, enemy)
    pygame.draw.rect(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))


    if countdown_timer:
        game_start()

    pygame.display.flip()
    clock.tick(60)