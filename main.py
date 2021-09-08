import pygame
import sys
import time
import random

screen = pygame.display.set_mode((405, 720))
bg = pygame.image.load("images/bg.png") 
floor = pygame.image.load("images/base.png")
floor_rect = floor.get_rect(center = (0,730))
magikarp = pygame.transform.scale(pygame.image.load("images/magikarp.png"), (80, 80)) 
magikarp_rect = magikarp.get_rect(center = (60, 360))
straw_surface = pygame.image.load("images/straw.png")
straw_list = []
strawspawn = pygame.USEREVENT
clock = pygame.time.Clock()
run = False
it = 0
ft = 0
t = 0
g = 0.5
scorenumber = 0
gameover = False

pygame.mixer.init(48000, -16, 1, 1024)
pygame.init()
pygame.display.set_caption("Magikarp Jump")
pygame.time.set_timer(strawspawn, 1500) 

font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 40)
font2 = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 25)
font3 = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 15)
bgmusic = pygame.mixer.Sound("sounds/game.mp3")

def move_floor(floor_rect):
    floor_rect.right -= 3
    if floor_rect.right <= 405:
        floor_rect.left = 0

def create_straw():
    straw_pos = random.randint(270, 680)
    bottom_straw = straw_surface.get_rect(midtop = (500, straw_pos))
    top_straw = straw_surface.get_rect(midbottom = (500, straw_pos - 250))
    return bottom_straw, top_straw    

def move_straws(straws):
	for straw in straws:
		straw.centerx -= 3
	return straws

def draw_straws(straws):
	for straw in straws:
            if straw.bottom >= 720:
                screen.blit(straw_surface, straw)
            else:  
                flip_straw_surface =  pygame.transform.flip(straw_surface, False, True)
                screen.blit(flip_straw_surface, straw)

def remove_straws(straws):
	for straw in straws:
		if straw.right == 0:
			straws.remove(straw)
	return straws

def collision(): 
    global run
    global gameover
    for straw in straw_list:
        if magikarp_rect.colliderect(straw):
            run = None
            gameover = True
    if magikarp_rect.bottom >= 700:
        run = None
        gameover = True
    if magikarp_rect.top <= -200:
        run = None
        gameover = True

def score():
    global scorenumber
    score = font.render(str(int(scorenumber)), True, (255, 255, 255))
    score_rect = score.get_rect(center = (202, 100))
    screen.blit(score, score_rect)

while True:
    bgmusic.play()

    #game state
    if run: 
        magikarp = pygame.transform.scale(pygame.image.load("images/magikarp.png"), (100, 100)) 
        screen.blit(bg, (0,0))

        clock.tick(90)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #handling quit state
                pygame.quit()
                sys.exit()

            if event.type == strawspawn: 
                straw_list.extend(create_straw())
                if straw_list[0].right <= 60:
                    scorenumber += 1

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            t = 2
            magikarp_rect.bottom -= 10 
            magikarp = pygame.transform.scale(pygame.image.load("images/magikarp-1.png"), (112, 112)) 

        #gravity
        t += 0.166
        s = 0.5*g*(t**2)
        magikarp_rect.bottom += s
        screen.blit(magikarp, magikarp_rect)

        #ran into this issue where the first pipe was not counted, this is a hacky fix that updates score of first pipe after a certain amount of time
        ft = round(time.time())
        if scorenumber == 0:
            if ft - it == 3:
                scorenumber += 1

        straw_list = move_straws(straw_list)
        straw_list = remove_straws(straw_list)
        draw_straws(straw_list)
        remove_straws(straw_list)
        collision()
        score()
        move_floor(floor_rect)
        screen.blit(floor, floor_rect)
        
        pygame.display.update()

    #title screen on first startup
    if run == False:
        bgmusic.play()
        clock.tick(90)
        for event in pygame.event.get(): #handling quit state
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = True
                    it = round(time.time())
        screen.blit(bg, (0,0))
        move_floor(floor_rect)
        screen.blit(floor, floor_rect)

        header = font2.render(("Magikarp Jump!"), True, (255, 255, 255))
        header_rect = header.get_rect(center = (202, 150))
        screen.blit(header, header_rect)

        magikarp_2 = pygame.transform.scale(pygame.image.load("images/magikarp.png"), (200, 200)) 
        magikarp_2_rect = magikarp_2.get_rect(center = (202, 300))
        screen.blit(magikarp_2, magikarp_2_rect)

        space = font3.render(("Press SPACE to jump"), True, (255, 255, 255))
        space_rect = space.get_rect(center = (202, 520))
        screen.blit(space, space_rect)

        enter = font3.render(("Press ENTER to start"), True, (255, 255, 255))
        enter_rect = enter.get_rect(center = (202, 570))
        screen.blit(enter, enter_rect)

        credits = font3.render(("Made by Ashwin V"), True, (255, 255, 255))
        credits_rect = credits.get_rect(center = (202, 620))
        screen.blit(credits, credits_rect)

        pygame.display.update()

    #game over state
    if gameover == True:
        clock.tick(90)
        bgmusic.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    #resetting all the values
                    t = 0
                    magikarp_rect = magikarp.get_rect(center = (60, 360))
                    it = round(time.time())
                    straw_list = []
                    scorenumber = 0
                    run = True
                    gameover = False

        screen.blit(bg, (0,0))
        move_floor(floor_rect)
        screen.blit(floor, floor_rect)

        header = font2.render(("Game Over!"), True, (255, 255, 255))
        header_rect = header.get_rect(center = (202, 150))
        screen.blit(header, header_rect)

        magikarp_3 = pygame.transform.scale(pygame.image.load("images/magikarp-dead.png"), (200, 200)) 
        magikarp_3_rect = magikarp_3.get_rect(center = (202, 300))
        screen.blit(magikarp_3, magikarp_3_rect)
        
        final_score = font2.render(("Score : " + str(scorenumber)), True, (255, 255, 255))
        final_score_rect = final_score.get_rect(center = (202, 450))
        screen.blit(final_score, final_score_rect)

        enter = font3.render(("Press ENTER to try again"), True, (255, 255, 255))
        enter_rect = enter.get_rect(center = (202, 570))
        screen.blit(enter, enter_rect)

        pygame.display.update()