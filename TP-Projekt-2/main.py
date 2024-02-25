import pygame
from player import Player
from button import Button
from pygame import mixer

pygame.init()
mixer.init()

#Skapa spelfönster
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fighting Game")

#Ställ in frames per second
clock = pygame.time.Clock()
FPS = 60
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

#Definiera spelvariabler
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  #Spelarpoäng [spelare1, spelare2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
game_paused = False
menu_state = "main"

#load button images
resume_img = pygame.image.load("assets/images/buttons/button_resume.png").convert_alpha()
controls_img = pygame.image.load("assets/images/buttons/button_controls.png").convert_alpha()
quit_img = pygame.image.load("assets/images/buttons/button_quit.png").convert_alpha()
movement_img = pygame.image.load("assets/images/buttons/button_movement.png").convert_alpha()
attack_img = pygame.image.load("assets/images/buttons/button_attack.png").convert_alpha()
pause_img = pygame.image.load("assets/images/buttons/button_pause.png").convert_alpha()
back_img = pygame.image.load("assets/images/buttons/button_back.png").convert_alpha()

#create button
resume_button = Button(404, 125, resume_img, 1)
controls_button = Button(397, 250, controls_img, 1)
quit_button = Button(436, 375, quit_img, 1)
movement_button = Button(186, 75, movement_img, 1)
attack_button = Button(245, 200, attack_img, 1)
keys_button = Button(184, 325, pause_img, 1)
back_button = Button(432, 450, back_img, 1)


#Definiera spelkaraktärernas variabler
player1_size = 162#pixlar
player1_scale = 4
player1_offset = [72, 56]
PLAYER1_DATA = [player1_size, player1_scale, player1_offset]
player2_size = 250#pixlar
player2_scale = 3
player2_offset = [112, 107]
PLAYER2_DATA = [player2_size, player2_scale, player2_offset]

#Ladda ljudeffekter och musik
pygame.mixer.music.load("assets\\audio\\mk.mp3")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1, 0.0, 5000)
player1_fx = pygame.mixer.Sound("assets\\audio\\sword_sound_effect.wav")
player1_fx.set_volume(0.2)
player2_fx = pygame.mixer.Sound("assets\\audio\\explosion2.wav")
player2_fx.set_volume(0.8)

#Ladda bakgrundsbilden
background = pygame.image.load("assets\\images\\background\\background.png").convert_alpha()

#Ladda bilden som visas när en spelare vinner
victory_img = pygame.image.load("assets\\images\\icons\\win.png").convert_alpha()

#Ladda spritesheets och definiera antal steg för varje animation
warrior_sheet = pygame.image.load("assets\\images\\warrior\\sprites\\warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets\\images\\wizard\\sprites\\wizard.png").convert_alpha()
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#Definiera typsnitt
menu_font = pygame.font.SysFont("assets\\fonts\\Grand9K Pixel.ttf",40)
count_font = pygame.font.Font("assets\\fonts\\Grand9K Pixel.ttf", 60)
score_font = pygame.font.Font("assets\\fonts\\Grand9K Pixel.ttf", 30)

#Funktion för att skriva text på skärmen
def draw_text(text, font, text_color, x, y):
    """
    Draw text on the screen.

    Parameters:
        text (str): The text to be displayed.
        font (Font): The font object used for rendering the text.
        text_color ((int, int, int)): The RGB color of the text.
        x (int): The x-coordinate of the text.
        y (int): The y-coordinate of the text.F
    """
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

#Funktion för att skapa bakgrundsbilden
def draw_bg():
    """Draw the background image."""
    scaled_bg = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#Funktion för att skapa/måla hälsomätare
def draw_health_bar(health, x, y):
    """
    Draw a health bar on the screen.

    Parameters:
        health (float): The current health value.
        x (int): The x-coordinate of the health bar.
        y (int): The y-coordinate of the health bar.
    """
    ratio = health / 100
    pygame.draw.rect(screen, white, (x - 1, y - 1, 402.5, 32.5))
    pygame.draw.rect(screen, red, (x, y, 400, 30))
    pygame.draw.rect(screen, green, (x, y, 400 * ratio, 30))

#Skapa spelarkaraktärer
player_1 = Player(1, 150, 330, False, PLAYER1_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, player1_fx)
player_2 = Player(2, 750, 330, True, PLAYER2_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, player2_fx)

#Spelloop
run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = not game_paused  #Pausa spelet

    #Skapar en svart bakgrund för menyn
    screen.fill((0, 0, 0))  

    if game_paused:
        if menu_state == "main":
            if resume_button.draw(screen):
                game_paused = False  #Återuppta
            if controls_button.draw(screen):
                menu_state = "controls"  #Byt till sidan med lista på kontrollerna
            if quit_button.draw(screen):
                run = False  #Avsluta spelet
        elif menu_state == "controls":
            movement_button.draw(screen)
            attack_button.draw(screen)
            keys_button.draw(screen)
            if back_button.draw(screen):
                menu_state = "main"  #Byt tillbaka till huvudmenyn
    else:
        draw_bg()  #Målar bakgrundsbilden

        #Målar elementen för spelarnas status
        draw_health_bar(player_1.health, 20, 20)
        draw_health_bar(player_2.health, 580, 20)
        draw_text("P1: " + str(score[0]), score_font, blue, 25, 65)
        draw_text("P2: " + str(score[1]), score_font, blue, 585, 65)
        player_1.draw(screen)
        player_2.draw(screen)

        #Tillkalla update funktionen för karaktärernas animationer
        player_1.update()
        player_2.update()

        if intro_count > 0:
            draw_text(str(intro_count), count_font, red, SCREEN_WIDTH / 2.1, SCREEN_HEIGHT / 3)
            draw_text("Press 'SPACE' to pause", score_font, red, 320, SCREEN_HEIGHT / 5)
            if pygame.time.get_ticks() - last_count_update >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()
                if intro_count == 0:
                    round_over = False
        else:
            #Funktioner för spelarnas rörelse
            player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_2, round_over)
            player_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_1, round_over)

            #Kollar ifall rundan är över
            if not round_over:
                if not player_1.is_alive:
                    score[1] += 1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
                elif not player_2.is_alive:
                    score[0] += 1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
            else:
                screen.blit(victory_img, (175, 40))
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    round_over = False
                    intro_count = 4
                    player_1 = Player(1, 150, 350, False, PLAYER1_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, player1_fx)
                    player_2 = Player(2, 750, 350, True, PLAYER2_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, player2_fx)


    pygame.display.update()

pygame.quit()