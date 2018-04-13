import pygame
import random
import os



WIDTH = 500
HEIGHT = 800
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
Yellow =(255,255,0)



# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

clock = pygame.time.Clock()



#class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("/Users/mecmantor67/Desktop/projet.py/GAME/3 : GAME A CONTINUER : PERSO/space invader a ma sauce/stuff/spaceship/razafree.png")


        self.rect=self.image.get_rect()

        self.rect.centerx = WIDTH/2   # le rectangle est centré
        self.rect.bottom = HEIGHT - 10 # le bas pas tout en bas ( à 10 du bas)


        self.speedx=0   # au début de la partie la vitesse est nulle



    def update(self):


        #keys

        self.speedx=0   #pour dire que la vitesse est 0 au début 


        keys= pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.speedx = 8
        if keys[pygame.K_LEFT]:
            self.speedx =-8

        self.rect.x += self.speedx    # pour réactualiser la position du rectangle après l'appui des touches  qui lui confère une vitesse à droite et gauche  ra!!!!!!!!!
    


        #stay on screen

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <0:
            self.rect.left =0

    def shooter(self):
        ball = Ball(self.rect.centerx,self.rect.top)
        all_sprites.add(ball)
        balls.add(ball) 




#ennemi
class Ennemi(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        

        # self.image=pygame.Surface((30,40))
        # self.image.fill(RED)
        self.image=pygame.image.load("/Users/mecmantor67/Desktop/projet.py/GAME/3 : GAME A CONTINUER : PERSO/space invader a ma sauce/stuff/Runes/Rune_Fire.png")
        self.rect = self.image.get_rect() 

        self.rect.x = random.randrange(WIDTH - self.rect.width)   # le nombre d'ennemies aléatoirement
        self.rect.y = random.randrange(-105,-60)                   #le nombre d'ennemies aléatoirement


        self.speedy = random.randrange(1,20)        #leur vitesse vers le vaisseau aléatoirement
        self.speedx= random.randrange(-3,3)        # leur vitesse en lateral aléatoirement

    def update(self):
        self.rect.y+=self.speedy
        self.rect.x +=self.speedx

        if self.rect.top > HEIGHT +10 or self.rect.right > WIDTH +20 or self.rect.left < 25:      # si l'ennemei va vers le vaisseau 
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-105,-60)
            self.speedy= random.randrange(1,20)


    
class Ball(pygame.sprite.Sprite):
    def __init__ (self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((10,20))
        self.image.fill(Yellow)
        self.rect=self.image.get_rect()

        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy     
        if self.rect.bottom<0:
            self.kill()


#load background graphics

background = pygame.image.load("/Users/mecmantor67/Desktop/projet.py/GAME/3 : GAME A CONTINUER : PERSO/space invader a ma sauce/stuff/background/moon_overlay.png")
background_rect = background.get_rect()



all_sprites = pygame.sprite.Group()

ennemies = pygame.sprite.Group()

balls=pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range (8):
    
    e = Ennemi()
    all_sprites.add(e)
    ennemies.add(e)


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

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shooter()
            


    # Update
    all_sprites.update()

    #check if ennemi hit the player
    hits= pygame.sprite.spritecollide(player,ennemies,False) # en premier le target et en deuxieme celui qui vise 
    if hits : 
        running = False


    #check if player hit ennemi
    hits = pygame.sprite.groupcollide(ennemies,balls,True, True)
    for hit in hits:
        
        e = Ennemi()
        all_sprites.add(e)
        ennemies.add(e)
            


    # Draw / render
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)





    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()