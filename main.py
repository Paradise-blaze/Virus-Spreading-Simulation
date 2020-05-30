import pygame

pygame.init()

height = 576
width  = 1024

screen = pygame.display.set_mode((width, height) )


pygame.display.set_caption("NanoWar")

clock = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    #gameplay.play(screen)

    clock.tick(60)
    pygame.display.flip()




if __name__ == '__main__':
    main()