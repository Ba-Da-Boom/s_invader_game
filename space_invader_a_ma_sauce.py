#! /usr/bin/env python3


#Pygame space invaders

import pygame
import random
from os import path



background_dir = path.join(path.dirname(__file__), 'stuff','background')
spaceship_dir = path.join(path.dirname(__file__), 'stuff','spaceship')
img_dir = path.join(path.dirname(__file__),'stuff','img')



#Basics
#jeu en mode portrait
WIDTH = 480
HEIGHT = 600
FPS = 60


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW=(255,255,0)



# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # width = x et height = y
pygame.display.set_caption("Space invaders")
clock = pygame.time.Clock()


#score

font_name = pygame.font.match_font("PressStart2P")
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop=(x,y)
    surf.blit(text_surface,text_rect)


def newMob():  # pour éviter de répéter le code
    m=Mob()
    all_sprites.add(m)
    mobs.add(m)




#création de la barre du shield
def draw_shield_bar(surf,x,y,pct):
    if pct<0:
        pct=0
    BAR_LENGH = 100
    BAR_HEIGHT = 10
    fill = (pct/100)*BAR_LENGH
    outline_rect = pygame.Rect(x,y,BAR_LENGH,BAR_HEIGHT)  #ou bar_lengh est x et bar height est y
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)



def draw_life_counter(surf,x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img,img_rect)



#class
class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):

        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)



#image et rect sont très important pour le sprite
        # create a plain rectangle for the sprite image
        # self.image = pygame.Surface((50,40))

        self.image=pygame.transform.scale(player_img,(50,60))
        # self.image.set_colorkey(BLACK)



        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        self.radius = 20   # pour donner une circonférence dans l'image du player

        # center the sprite on the screen
        # self.rect.center = (WIDTH / 2, HEIGHT / 2) pas de y car le vaisseau est en bas

        self.rect.centerx = WIDTH/2 # que width car width est x
        self.rect.bottom=HEIGHT-10

        self.speedx=0

       #ajout du shield
        self.shield = 100



       #ajout du shoot
        self.shoot_delay=250
        self.last_shot = pygame.time.get_ticks()


        #ajout de la vie au joueur
        self.lives = 5
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()



    #la ou on effectue les changements
    def update(self):

        # any code here will happen every time the game loop updates



        #keys

        self.speedx=0

        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx=-8
        if keystate[pygame.K_RIGHT]:
            self.speedx=8
        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speedx


        #stay on the screen
        if self.rect.right> WIDTH:
            self.rect.right=WIDTH
        if self.rect.left<0:
            self.rect.left=0


        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000 :
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT -10


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot=now
            bullet = Bullet(self.rect.centerx,self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet) #pas oublie de rajouter bullets en sprite.group()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2,HEIGHT + 200)




# ennemi
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    #on a fait une copie de la version originale
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image=self.image_orig.copy()


        self.rect=self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2) #pour améliorer la présence du grava

        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        self.rect.x=random.randrange(WIDTH - self.rect.width)
        self.rect.y=random.randrange(-100,-40)   #start and stop



        self.speedy = random.randrange(2,10)

    #pour cette version on ajoute cette ligne :

        self.speedx=random.randrange(-3,3)





    # on rajoute la rotation ici
        self.rot=0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()


    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot=(self.rot + self.rot_speed )% 360
            new_image = pygame.transform.rotate(self.image_orig,self.rot)

            old_center = self.rect.center
            self.image= new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center





    def update(self):
        self.rect.y +=self.speedy
        #pour cette version on ajoute cette ligne:
        self.rect.x += self.speedx

        if self.rect.top> HEIGHT +10  or self.rect.left <25 or self.rect.right > WIDTH + 20:
            self.rect.x=random.randrange(WIDTH-self.rect.width)
            self.rect.y=random.randrange(-100,-40)
            self.speedy = random.randrange(1,8)





#bullet for the player
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((10,20))
        self.image.fill(YELLOW)

        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx = x
        self.speedy = -10


    def update(self):
        self.rect.y +=self.speedy  # speedy = -10 car va du bas vers le haut et le haut est négatif

        if self.rect.bottom < 0:
            self.kill()   # remove de l'écran

class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size= size
        self.image=explosion_anim[self.size][0]
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.frame=0
        self.last_update=pygame.time.get_ticks()
        self.frame_rate = 50


    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update=now
            self.frame +=1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()


            else:
                center = self.rect.center
                self.image=explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Pow (pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield","gun"])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


#load the game graphics
background = pygame.image.load(path.join(background_dir,'moon_overlay.png')).convert()
background_rect = background.get_rect()


player_img = pygame.image.load(
    path.join(spaceship_dir,'razafree.png')).convert()
player_mini_img = pygame.transform.scale(player_img,(25,25))
player_mini_img.set_colorkey(BLACK)

# meteor_img = pygame.image.load(path.join(img_dir,"/Users/mecmantor67/Desktop/projet.py/GAME/TUTO GAME +/stuff/img/meteorBrown_med1.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png',
               'meteorBrown_big2.png', 'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir,img)).convert())


explosion_anim = {}
explosion_anim["lg"]=[]
explosion_anim["sm"]=[]
explosion_anim["player"]=[]
for i in range(9):
    filename = 'sonicExplosion0{}.png'.format(
        i)
    img1 = pygame.image.load(path.join(img_dir,filename)).convert()
    img1.set_colorkey(BLACK)
    img_lg=pygame.transform.scale(img1,(75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img1,(32,32))
    explosion_anim["sm"].append(img_sm)
    filename2 = 'regularExplosion0{}.png'.format(
        i)
    img2=pygame.image.load(path.join(img_dir,filename2)).convert()
    explosion_anim["player"].append(img2)


powerup_images = {}
powerup_images["shield"] = pygame.image.load(path.join(
    img_dir, 'shield_gold.png')).convert()
powerup_images["gun"] = pygame.image.load(path.join(
    img_dir, 'laserRed16.png')).convert()


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets=pygame.sprite.Group()
powerups = pygame.sprite.Group()



player = Player()        # instance de la classe player
all_sprites.add(player)


for i in range(8):
  newMob()
score = 0





# Game loop
running = True
while running:

    # keep loop running at the right speed
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():

        # check for closing window
        if event.type == pygame.QUIT:
            running = False


        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         player.shoot()



    # Update
    all_sprites.update()

    #check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs,bullets, True ,True) #le premier True est pour le groupe et le deuxième True est pour le groupe bullets
    for hit in hits :
        score += 50 - hit.radius
        expl = Explosion(hit.rect.center,"lg")
        all_sprites.add(expl)
        if random.random()>0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newMob()



    #check to see if a mob it the player
    hits = pygame.sprite.spritecollide( player, mobs,True,pygame.sprite.collide_circle)   #mettre comme paramètre dans les parenthèses en premier la target après le Group et puis False ou True )
    for hit in hits:
        player.shield -= hit.radius *2
        expl = Explosion(hit.rect.center,"sm")
        all_sprites.add(expl)
        newMob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center,"player")
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -=1
            player.shield = 100

    if player.lives == 0 and not death_explosion.alive():
        running=False



    #check to see if player hit a powerup
    hits = pygame.sprite.spritecollide(player,powerups,True)
    for hit in hits:
        if hit.type =="shield":
            player.shield +=random.randrange(10,30)
            if player.shield >=100:
                player.shield = 100
        if hit.type =="gun":
            pass



    # Draw / render
    screen.fill(BLACK)
    screen.blit(background,background_rect)   # check dans load graphics
    all_sprites.draw(screen)
    draw_text(screen,str(score),18, WIDTH/2, 10)
    draw_shield_bar(screen,5,5,player.shield)

    draw_life_counter (screen,WIDTH - 100,5,player.lives,player_mini_img)

    # *after* drawing everything, flip the display
    pygame.display.flip()



pygame.quit()
