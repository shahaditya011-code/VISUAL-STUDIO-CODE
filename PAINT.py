
import pygame
from pygame.locals import QUIT

pygame.init()

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
TOOLBAR_HEIGHT = 70

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (200,200,200)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,180,0)
YELLOW = (255,255,0)
PURPLE = (160,32,240)
ORANGE = (255,165,0)
CYAN = (0,200,200)

WINDOW = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Paint")

drawing = False
brush_size = 2
min_brush_size = 1
max_brush_size = 10
brush_color = BLACK
eraser_mode = False
last_pos = None

canvas = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT-TOOLBAR_HEIGHT))
canvas.fill(WHITE)

toolbar = pygame.Surface((WINDOW_WIDTH,TOOLBAR_HEIGHT))
toolbar.fill(GRAY)

running = True

while running:

    toolbar.fill(GRAY)

    font = pygame.font.Font(None,24)

    pen_text = font.render("P",True,BLACK)
    eraser_text = font.render("E",True,BLACK)
    decrease_text = font.render("-",True,BLACK)
    increase_text = font.render("+",True,BLACK)

    size_text = font.render("Size: " + str(brush_size),True,BLACK)

    toolbar.blit(pen_text,(10,10))
    toolbar.blit(eraser_text,(45,10))
    toolbar.blit(decrease_text,(85,10))
    toolbar.blit(increase_text,(115,10))
    toolbar.blit(size_text,(155,15))

    pen_rect = pen_text.get_rect(topleft=(10,10))
    eraser_rect = eraser_text.get_rect(topleft=(45,10))
    decrease_rect = decrease_text.get_rect(topleft=(85,10))
    increase_rect = increase_text.get_rect(topleft=(115,10))

    # Colour palette
    colors = [BLACK,RED,BLUE,GREEN,YELLOW,PURPLE,ORANGE,CYAN]

    color_buttons = []

    for i,color in enumerate(colors):
        button = pygame.draw.circle(toolbar,color,(15+i*35,52),10)
        color_buttons.append(button)

    # Clear canvas button
    clear_rect = pygame.draw.rect(toolbar,(255,255,255),(305,40,85,25))
    clear_text = font.render("Clear",True,BLACK)
    toolbar.blit(clear_text,(325,44))

    # Display everything
    WINDOW.fill(WHITE)
    WINDOW.blit(canvas,(0,TOOLBAR_HEIGHT))
    WINDOW.blit(toolbar,(0,0))

    for event in pygame.event.get():

        if event.type == QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.pos[1] <= TOOLBAR_HEIGHT:

                if pen_rect.collidepoint(event.pos):
                    eraser_mode = False

                elif eraser_rect.collidepoint(event.pos):
                    eraser_mode = True

                elif decrease_rect.collidepoint(event.pos):
                    brush_size = max(min_brush_size,brush_size-1)

                elif increase_rect.collidepoint(event.pos):
                    brush_size = min(max_brush_size,brush_size+1)

                # Select colour
                for i,button in enumerate(color_buttons):
                    if button.collidepoint(event.pos):
                        brush_color = colors[i]
                        eraser_mode = False

                # Clear canvas
                if clear_rect.collidepoint(event.pos):
                    canvas.fill(WHITE)

            else:
                drawing = True
                last_pos = (event.pos[0],event.pos[1]-TOOLBAR_HEIGHT)

                color = brush_color if not eraser_mode else WHITE

                pygame.draw.circle(canvas,color,last_pos,brush_size//2)

        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None

        elif event.type == pygame.MOUSEMOTION and drawing:

            if event.pos[1] > TOOLBAR_HEIGHT:

                color = brush_color if not eraser_mode else WHITE

                current_pos = (event.pos[0],event.pos[1]-TOOLBAR_HEIGHT)

                pygame.draw.line(canvas,color,last_pos,current_pos,brush_size)

                last_pos = current_pos

            else:
                last_pos = None

    pygame.display.flip()

pygame.quit()


