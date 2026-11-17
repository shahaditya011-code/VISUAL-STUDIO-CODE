
import pygame
import random
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


pygame.init()

screen_width,screen_height=400,300
window=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Space Collider Game")

background1=pygame.image.load("SPACESHIP BACKGROUND.jpeg").convert()
background1 = pygame.transform.scale(background1, (screen_width, screen_height))
background2=pygame.transform.scale(background1,(screen_width,screen_height))

spaceship_img=pygame.image.load("SPACESHIP.png").convert_alpha()
spaceship_width,spaceship_height=spaceship_img.get_size()
spaceship_scale=0.15
spaceship_img=pygame.transform.scale(spaceship_img,(int(spaceship_width*spaceship_scale),int(spaceship_height*spaceship_scale)))

spaceship_x=screen_width//2-spaceship_img.get_width()//2
spaceship_y=screen_height-50
spaceship_speed=3

class Asteroid:
    def __init__(self,x,y,image,scale):
        self.x=x
        self.y=y
        self.image=image
        self.scale=scale

        self.image=pygame.transform.scale(image,(int(image.get_width()*scale),int(image.get_height()*scale)))

    def move(self,speed):
        self.y+=speed

    def draw(self,window):
        window.blit(self.image,(self.x,self.y))


asteroid_img=pygame.image.load("Asteroids.png").convert_alpha()
asteroid_width,asteroid_height=asteroid_img.get_size()
max_asteroid_scale=0.15
min_asteroid_scale=0.05

asteroids=[]
clock=pygame.time.Clock()
game_running=True

def close_game():
    pygame.quit()
    sys.exit()

def update_background():
    global background1_y,background2_y
    background1_y=(background1_y+1)%screen_height
    background2_y=background1_y-screen_height
    window.blit(background1,(0,background1_y))
    window.blit(background2,(0,background2_y))

background1_y=0
background2_y=-screen_height

def create_asteroid():
    x = random.randint(0, screen_width - 50)
    y = -50
    scale = random.uniform(min_asteroid_scale, max_asteroid_scale)
    asteroids.append(Asteroid(x, y, asteroid_img, scale))

create_asteroid_timer = 0


while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    keys = pygame.key.get_pressed()

    create_asteroid_timer += 1

    if create_asteroid_timer >= 60:
        create_asteroid()
        create_asteroid_timer = 0

    if keys[pygame.K_LEFT]:
        spaceship_x -= spaceship_speed

    if spaceship_x < 0:
        spaceship_x = 0

    if keys[pygame.K_RIGHT]:
        spaceship_x += spaceship_speed

    if spaceship_x > screen_width - spaceship_img.get_width():
        spaceship_x = screen_width - spaceship_img.get_width()

    window.fill((0, 0, 0))
    update_background()

    window.blit(spaceship_img, (spaceship_x, spaceship_y))

    spaceship_mask = pygame.mask.from_surface(spaceship_img)

    for asteroid in asteroids:
        asteroid.move(2)

        asteroid.draw(window)

        asteroid_mask = pygame.mask.from_surface(asteroid.image)

        offset = (
            asteroid.x - spaceship_x,
            asteroid.y - spaceship_y
        )

        if spaceship_mask.overlap(asteroid_mask, offset):
            close_game()
    asteroids = [
        asteroid for asteroid in asteroids
        if asteroid.y < screen_height
    ]

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
