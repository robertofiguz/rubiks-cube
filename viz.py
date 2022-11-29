import pygame

pygame.init()
pygame.display.set_caption("Rubik's Cube")
screen = pygame.display.set_mode((600,200))
screen.fill((255,255,255))
def draw_rubiks_cube():
    pygame.draw.rect(screen, (0,0,0),(50,100,100,100))
    pygame.draw.rect(screen, (255,0,0),(150,100,100,100))
    pygame.draw.rect(screen, (0,255,0),(250,100,100,100))
    pygame.draw.rect(screen, (0,0,255),(350,100,100,100))

draw_rubiks_cube()
pygame.display.update()

while True:
    
    pygame.display.flip()
