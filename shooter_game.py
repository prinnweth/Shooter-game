#Create your own shooter
from random import*
from pygame import *
window = display.set_mode((700,500))
display.set_caption("Catch")
background=transform.scale(image.load("galaxy.jpg"),(700,500))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed,size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
bullets = sprite.Group()
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x>0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x<700-65:
            self.rect.x += self.speed
    
    def fire(self):
        b = Bullet("bullet.png",self.rect.centerx-20,self.rect.y,20,40,40)
        bullets.add(b)
plan = Player("rocket.png",200,450,10,150,150)

class Enemy (GameSprite):
    def update(self):
        global lost
        
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0,700-65)
            lost += 1

ufos = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    ufo = Enemy("ufo.png", randint(0,700-65), 0, randint(1,3),100,85)
    ufos.add(ufo)
    asteroid = Enemy("asteroid.png", randint(0,700-65), 0, randint(1,3),100,85)
    asteroids.add(asteroid)
class Bullet (GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0 :
            self.kill()
        


    
mixer.init()
mixer.music.load('Star Wars Main Theme (Full).ogg')
mixer.music.play()
game = True
lost = 0
score = 0
font.init()
font1 = font.SysFont("Arial",36)
font2 = font.SysFont("Arial",100)

finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                plan.fire()
    if not finish:
        window.blit(background,(0,0))
        
        
        sprites_list = sprite.groupcollide(ufos, bullets, True, True)
        asteroid_list=sprite.groupcollide(asteroids, bullets, True, True)
        for e in sprites_list:
            score  += 10
            ufo = Enemy("ufo.png", randint(0,700-65), 0, randint(1,3),100,100)
            ufos.add(ufo)
        for e in asteroid_list:
            score  -=20
            asteroid = Enemy("asteroid.png", randint(0,700-65), 0, randint(1,3),100,100)
            asteroids.add(asteroid)


        text_lose = font1.render("Missed:" + str(lost),1,(255,255,255))
        text_score = font1.render("Score:" + str(score),1,(255,255,255))
                    
        plan.update()
        plan.reset()
        ufos.update()
        ufos.draw(window)
        asteroids.update()
        asteroids.draw(window)
        window.blit(text_lose,(0,0))
        window.blit(text_score,(0,40))
        bullets.update()
        bullets.draw(window)

        if score >= 100:
            text_win = font2.render("Win" ,1,(255,255,255))
            window.blit(text_win,(280,200))
            finish = True 
        if score <= -40 :
            text_better= font2.render("Next time!" ,1,(255,255,255))
            window.blit(text_better,(175,200))
            finish = True
        #if lost >= 10 :
        #    text_better= font2.render("You lose!" ,1,(255,255,255))
         #   window.blit(text_better,(175,200))
          #  finish = True
    
        display.update()

    time.delay(50)