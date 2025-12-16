import pygame

class YouSuck:
    def __init__(self):
        self.titlefont = pygame.font.Font("Silkscreen-Regular.ttf",100)
        self.otherfont = pygame.font.Font("Silkscreen-Regular.ttf",25)


    def draw(self, screen, scr):
        title = self.titlefont.render("You Died",True,("Red"))
        startbuttonrect = pygame.Rect(175, 200, 500,100)
        start_text = self.otherfont.render(f"Your Score Was {str(scr)}",True,("Red"))
        while True:
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if startbuttonrect.collidepoint(e.pos):
                        print("a")
                        return

            screen.fill(("Black"))
            screen.blit(title,(60,75))
            # pygame.draw.rect(screen,"white", startbuttonrect)
            screen.blit(start_text,startbuttonrect)
            pygame.display.update()
