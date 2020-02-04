
import pygame
import random
from time import sleep
pygame.mixer.init()


WHITE = (255, 255, 255)
BLACK= (0,0,0)
RED = (255,0,0)
pad_width = 1280
pad_height = 720
background_width = 1280
aircraft_width = 90
aircraft_height = 55
mushroom_width = 110
mushroom_height = 100


fireball1_width = 140
fireball1_height = 60
fireball2_width = 82
fireball2_height = 80

def drawScore(count):
    global gamepad

    font = pygame.font.SysFont(None,75)
    text = font.render('Mushroom Passed: '+ str(count),True,BLACK)
    gamepad.blit(text,(0,0))

def gameOver():
    global gamepad
    dispMessage('GAME OVER')


def textObj(text, font):
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()

def dispMessage(text):
    global gamepad

    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = textObj(text, largeText)
    TextRect.center = ((pad_width/2),(pad_height/2))
    gamepad.blit(TextSurf, TextRect)
    pygame.display.update()
    sleep(2)
    runGame()

def crash():
    global gamepad, explosion_sound
    pygame.mixer.Sound.play(explosion_sound)
    dispMessage('GameOver!')


def drawObject(obj,x,y):
    global gamepad
    gamepad.blit(obj,(x,y))

def runGame():
    global gamepad, aircraft, clock, background1, background2
    global mushroom,fires,bullet,boom, shot_sound

    isShotMushroom = False
    boom_count = 0

    mushroom_passed = 0

    bullet_xy = []

    x = pad_width * 0.05
    y = pad_height * 0.8
    y_change = 0

    background1_x = 0
    background2_x = background_width

    mushroom_x = pad_width
    mushroom_y = random.randrange(0, pad_height)

    fire_x = pad_width
    fire_y = random.randrange(0, pad_height)
    random.shuffle(fires)
    fire = fires[0]

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -7
                elif event.key == pygame.K_DOWN:
                    y_change = 7

                elif event.key == pygame.K_LCTRL:
                    pygame.mixer.Sound.play(shot_sound)
                    bullet_x = x + aircraft_width
                    bullet_y = y + aircraft_height/2
                    bullet_xy.append([bullet_x, bullet_y])

                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        
        gamepad.fill(WHITE)

        background1_x -= 2
        background2_x -= 2

        if background1_x == -background_width:
            background1_x = background_width

        if background2_x == -background_width:
            background2_x = background_width
            
        drawObject(background1, background1_x, 0)
        drawObject(background2, background2_x, 0)

#----->add
        drawScore(mushroom_passed)

        if mushroom_passed > 2:
            gameOver()
        

        y += y_change
        if y<0:
            y = 0
        elif y>pad_height - aircraft_height:
                y = pad_height - aircraft_height

        mushroom_x -=10
        if mushroom_x <= 0:
            mushroom_passed += 1
            mushroom_x = pad_width
            mushroom_y = random.randrange(0, pad_height)

        if fire[1] == None:
            fire_x -= 12
        else:
            fire_x-= 9

        if fire_x <= 0:
            fire_x = pad_width
            fire_y = random.randrange(0, pad_height)
            random.shuffle(fires)
            fire = fires[0]

        if len(bullet_xy)!= 0:
            for i,bxy in enumerate(bullet_xy):
                bxy[0] += 15
                bullet_xy[i][0] = bxy[0]

                if bxy[0] > mushroom_x:
                    if bxy[1] > mushroom_y and bxy[1]<mushroom_y+mushroom_height:
                        bullet_xy.remove(bxy)
                        isShotMushroom = True
                
                if bxy[0] >= pad_width:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass





        if x + aircraft_width > mushroom_x:
            if(y > mushroom_y and y < mushroom_y+mushroom_height)or\
            (y+aircraft_height > mushroom_y and y+aircraft_height < mushroom_y + mushroom_height):
                crash()

        if fire[1]!= None:
            if fire[0] == 0:
                fireball_width = fireball1_width
                fireball_height = fireball1_height
            elif fire[0] == 1:
                fireball_width = fireball2_width
                fireball_height = fireball2_height

            if x + aircraft_width > fire_x:
                if(y > fire_y and y <fire_y+fireball_height)or\
                (y+aircraft_height > fire_y and y + aircraft_height < fire_y+fireball_height):
                    crash()
                    

                    
                    
        drawObject(aircraft,x,y)

        if len(bullet_xy) != 0:
            for bx,by in bullet_xy:
                drawObject(bullet,bx,by)

        if not isShotMushroom:        
            drawObject(mushroom,mushroom_x,mushroom_y)
        else:
            drawObject(boom,mushroom_x,mushroom_y)
            boom_count += 1
            if boom_count>5:
                boom_count = 0
                mushroom_x = pad_width
                mushroom_y = random.randrange(0,pad_height-mushroom_height)
                isShotMushroom = False
        
        if fire[1]!= None:
            drawObject(fire[1],fire_x,fire_y)
        
        pygame.display.update()
        clock.tick(60)
        
    pygame.quit()
    quit()

def initGame():
    global gamepad, aircraft, clock, background1, background2
    global mushroom,fires,bullet,boom
    global shot_sound, explosion_sound

    #pygame.mixer.music.load('')
    shot_sound = pygame.mixer.Sound('C:\python\pr/bgm/shot.wav')
    explosion_sound = pygame.mixer.Sound('C:\python\pr/bgm/explosion.wav')
    pygame.mixer.music.load('C:\python\pr/bgm/bgm.wav')
    pygame.mixer.music.play(-1)

    fires = []

    pygame.init()
    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('PyFlying')
    aircraft = pygame.image.load('C:\python\pr/img/ca.png')
    background1 = pygame.image.load('C:\python\pr/img/backg.png')
    background2 = background1.copy()
    mushroom = pygame.image.load('C:\python\pr/img/mushroom.png')
    
    fires.append((0, pygame.image.load('C:\python\pr/img/sl.png')))
    fires.append((1, pygame.image.load('C:\python\pr/img/dal.png')))

    boom = pygame.image.load('C:\python\pr/img/boom.png')


    for i in range(3):
        fires.append((i+2, None))

    bullet = pygame.image.load('C:\python\pr/img/bullet.png')
    
    clock = pygame.time.Clock()
    runGame()

initGame()
    
