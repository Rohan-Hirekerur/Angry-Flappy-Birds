import pygame as pg
from random import randint

black = (0,0,0)
white = (255,255,255)

pg.init()

scale = 2
width = 1000*scale
height = 566*scale
size = width,height
screen = pg.display.set_mode(size)

pg.display.set_caption("Flappy Angry Bird")
bg = pg.image.load("./bg.jpg")
bg = pg.transform.scale(bg, size)
birdimg = pg.image.load("./bird.png")
birdimg = pg.transform.scale(birdimg,(80*scale,80*scale))
obs_img = pg.image.load("./wood.jpg")

done = False
clock = pg.time.Clock()

bird_x = width/4
bird_y = height/2

obs_x = width
obs_y = 0
separator = 500
obs_size_x = 80*scale

obs_size_y = randint(0,height-separator)
obs_speed = 30
score = 0

x_move = 0
flap = 0  

def set_bird_pos(x,y):
    screen.blit(birdimg,(x-(40*scale),y-(40*scale)))
    #pg.draw.circle(screen,white,(int(x),int(y)),40*scale)
    
def set_obs_pos(x,y,x_size,y_size):
    bot_size_y = int(height-y_size-separator)
    obs_mod_top = pg.transform.scale(obs_img,(int(x_size),int(y_size)))
    obs_mod_bot = pg.transform.scale(obs_img,(int(x_size),bot_size_y))
    screen.blit(obs_mod_top,(x-(40*scale),0))
    screen.blit(obs_mod_bot,(x-(40*scale),(height-bot_size_y)))
    
def gameover(score):
    font = pg.font.SysFont("./flappy.ttf",200)
    text = font.render("Game Over!",True,white)
    screen.blit(text,(width/2 - 500,height/2 - 100))
    text = font.render(str(score),True,white)
    screen.blit(text,(width/2 - 200,height/2+30))
    pg.display.flip()
    pg.time.delay(2000)
    
def set_score(score):
    font = pg.font.SysFont("./flappy.ttf",200)
    text = font.render(str(score),True,white)
    screen.blit(text,(width-250,50))
    pg.display.flip()
    

    
while not done:
        
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_UP:
            flap = -height/14
            
    if event.type == pg.KEYUP:
        if event.key == pg.K_UP:
            flap = height/28
            
    bird_y += flap
    obs_x -= obs_speed
    screen.blit(bg, (0, 0))
    set_obs_pos(obs_x,0,80*scale,obs_size_y)
    set_bird_pos(bird_x,bird_y)
    
    if int(bird_x) in range(obs_x,obs_x+obs_size_x):
        if int(bird_y) in range(obs_y,int((obs_y+obs_size_y))) or (int(bird_y) in range(int(obs_y+obs_size_y+separator),height)):
            gameover(score)
            break
    
    if bird_x == obs_x:
        score+=1;
    set_score(score)
    
    if bird_y >= height :
        gameover(score)
        break
    
    if obs_x <= 0:
        obs_x = width
        obs_size_y = randint(0,int(height-separator))
        
    
    pg.display.flip()
    clock.tick(30)
            
pg.quit()