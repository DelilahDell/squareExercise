import pygame

pygame.init()

gameDisplay = pygame.display.set_mode((500,500))

pygame.display.set_caption('SquareExcercise')

gold = (212, 175, 55)

silver = (192, 192, 192)


clock = pygame.time.Clock()

x = 220
y = 220


gameExit = False

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                x -= 10
            if event.key == pygame.K_d:
                x += 10
            if event.key == pygame.K_w:
                y -= 10
            if event.key == pygame.K_s:
                y += 10
            

            
    gameDisplay.fill(gold, rect=None, special_flags=0)

    pygame.draw.rect(gameDisplay, silver, [x, y, 70, 70])


    
    pygame.display.update()
    clock.tick(60)



pygame.quit()

quit()
