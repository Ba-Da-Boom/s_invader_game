import pygame
import random
import os

WIDTH =500
HEIGHT = 700
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)




#class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("/Users/mecmantor67/Desktop/projet.py/GAME/3 : GAME A CONTINUER : PERSO/space invader a ma sauce/stuff/spaceship/razafree.png")
        self.rect=self.image.get_rect()


        self.rect.centerx=(WIDTH/2)
        self.rect.bottom = HEIGHT - 10


        
        
        self.speedx = 0



    def update(self):
        self.speedx=0
        self.rect.x += self.speedx
        


        #keys
        keys= pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.speedx = 10

        if keys[pygame.K_LEFT]:
            self.speedx =-10

        self.rect.x +=self.speedx


        #stay on screen

        if self.rect.right > WIDTH:
            self.rect.right=WIDTH
        if self.rect.left <0:
            self.rect.left = 0 



class Grava(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("/Users/mecmantor67/Desktop/projet.py/GAME/3 : GAME A CONTINUER : PERSO/space invader a ma sauce/stuff/Runes/Rune_Fire.png")
        self.rect= self.image.get_rect()

        self.rect.x=random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-60)

        self.speedx=random.randrange(-3,3)
        self.speedy=random.randrange(1,20)


    def update(self):
        self.rect.y +=self.speedy
        self.rect.x +=self.speedx


        if self.rect.top > HEIGHT + 10 or self.rect.right > WIDTH +20 or self.rect.left < 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-60)
            self.speedy = random.randrange(1,20)






# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space_X")

clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()

grava = pygame.sprite.Group()


player = Player()

all_sprites.add(player)

for i in range(8):
    g = Grava()
    all_sprites.add(g)
    grava.add(g)

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

    # Update
    all_sprites.update()


    #if player get hit by grava :
    hits = pygame.sprite.spritecollide(player,grava,False)
    if hits : 
        running = False

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)


    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()