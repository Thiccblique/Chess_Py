import pygame
class Start:
    def __init__(self):
        self.titlefont = pygame.font.Font("Silkscreen-Regular.ttf",100)

    def draw(self, screen):
        title = self.titlefont.render("DinoGame",True,(24,150,19))
        startbuttonrect = pygame.Rect(175, 200, 500,100)
        start_text = self.titlefont.render("Start",True,("black"))
        while True:
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if startbuttonrect.collidepoint(e.pos):
                        print("a")
                        return

            screen.fill((14, 92, 161))
            screen.blit(title,(60,75))
            # pygame.draw.rect(screen,"white", startbuttonrect)
            screen.blit(start_text,startbuttonrect)
            pygame.display.update()
