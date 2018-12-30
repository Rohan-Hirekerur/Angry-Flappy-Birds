import pygame as pg
import pyglet
from random import randint

black = (0,0,0)
white = (255,255,255)

pg.init()

page_width = 2560
page_height = 1132

size = page_width,page_height
screen = pg.display.set_mode(size)

pg.display.set_caption("Flappy Angry Bird")
bg = pg.image.load("./img/bg.jpg")
bg = pg.transform.scale(bg, size)
birdimg = pg.image.load("./img/bird.png")
birdimg = pg.transform.scale(birdimg,(160,160))
obs_img = pg.image.load("./img/wood.jpg")

class bird:
    width = 160
    height = 160
    x = 560
    y = 486
    score = 0
        
    def get_pos(self):
        return [self.x,self.y]
        
    def show(self):
        #pg.draw.rect(screen,white,[self.x+25,self.y+25,114,114])
        screen.blit(birdimg,(self.x,self.y))
        pg.display.update()
        
    def flap(self):
        self.y -= page_height/14
        screen.blit(birdimg,(self.x,self.y))
        
    def fall(self):
        self.y += page_height/28
        screen.blit(birdimg,(self.x,self.y))
        
    def gameover(self):
        font = pg.font.SysFont("./flappy.ttf",200)
        text = font.render("Game Over!",True,white)
        screen.blit(text,(page_width/2 - 500,page_height/2 - 100))
        text = font.render(str(self.score),True,white)
        screen.blit(text,(page_width/2 - 200,page_height/2+30))
        screen.blit(birdimg,(self.x,self.y))
        pg.display.update()
        pg.time.delay(2000)
        
    def show_score(self):
        font = pg.font.SysFont("./flappy.ttf",200)
        text = font.render(str(self.score),True,white)
        screen.blit(text,(page_width-250,50))
        
    def inc_score(self):
        print(self.score)
        self.score += 1
        
def set_obs_pos(x,y,x_size,y_size,separator):
    bot_size_y = int(page_height-y_size-separator)
    obs_mod_top = pg.transform.scale(obs_img,(int(x_size),int(y_size)))
    obs_mod_bot = pg.transform.scale(obs_img,(int(x_size),bot_size_y))
    screen.blit(obs_mod_top,(x,0))
    screen.blit(obs_mod_bot,(x,(page_height-bot_size_y)))
    pg.display.update()

def collision(l1,r1,l2,r2):
    return  (l1[0] < r2[0]) and (l2[0] < r1[0]) and \
            (l1[1] < r2[1]) and (l2[1] < r1[1])
        
def play():
    b1 = bird()
    b1.show()
    
    obs_x = page_width
    obs_y = 0
    separator = 500
    obs_size_x = 160
    obs_size_y = randint(0,page_height-separator)
    obs_speed = 40
    clock = pyglet.clock.Clock()
    clock.set_fps_limit(60)
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                b1.flap()
            else:
                b1.fall()
        else:
            b1.fall()
            
        obs_x -= obs_speed
        screen.blit(bg,(0,0))
        set_obs_pos(obs_x,0,160,obs_size_y,separator)
        bird_pos = b1.get_pos()
        b1.show_score()
        
        
        bird_pos[0] += 25
        bird_pos[1] += 25
        bird_pos[1] = int(bird_pos[1])
        bird_diag = [int(bird_pos[0]+114),int(bird_pos[1]+114)]
        b1.show()
        upper_obs_pos = [int(obs_x),int(obs_y)]
        upper_obs_diag = [int(obs_x+obs_size_x),int(obs_size_y)]
        bot_obs_pos = [int(obs_x),int(obs_size_y+separator)]
        bot_obs_diag = [int(obs_x+obs_size_x),int(page_height)]
        
        if collision(bird_pos,bird_diag,upper_obs_pos,upper_obs_diag):
            b1.gameover()
            break
        
        if collision(bird_pos,bird_diag,bot_obs_pos,bot_obs_diag):
            b1.gameover()
            break
                
        if int(bird_pos[0]) == int(obs_x+25):
            b1.inc_score()
            
        if bird_pos[1] >= page_height :
            b1.gameover()
            break
    
        if obs_x <= -80:
            obs_x = page_width
            obs_size_y = randint(0,int(page_height-separator))
        
        clock.tick()

#while True:
play()  
pg.quit()
    