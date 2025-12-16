import pygame
import os  #NEW

class Piece():


    def __init__(self,piece,color,file,rank):
        self.file = file
        self.rank = rank
        self.image = self.get_image(piece, color)
        self.piece = piece
        self.color = color

    def get_image(self,piece,color):
        # Get the absolute path to the CSGO directory  #NEW
        current_dir = os.path.dirname(os.path.abspath(__file__))  #NEW
        csgo_dir = os.path.join(os.path.dirname(current_dir), "CSGO")  #NEW
        
        images = {
            ("white","pawn"):pygame.image.load(os.path.join(csgo_dir, "whitepawn.png")),  #NEW
            ("white","queen"):pygame.image.load(os.path.join(csgo_dir, "wq.png")),  #NEW
            ("white","king"):pygame.image.load(os.path.join(csgo_dir, "whiteking.png")),  #NEW
            ("white","knight"):pygame.image.load(os.path.join(csgo_dir, "whitehorse.png")),  #NEW
            ("white","bishop"):pygame.image.load(os.path.join(csgo_dir, "whitebishop.png")),  #NEW
            ("white","rook"):pygame.image.load(os.path.join(csgo_dir, "whiterook.png")),  #NEW
            ("black","queen"):pygame.image.load(os.path.join(csgo_dir, "black queen.png")),  #NEW
            ("black","king"):pygame.image.load(os.path.join(csgo_dir, "blackking.png")),  #NEW
            ("black","pawn"):pygame.image.load(os.path.join(csgo_dir, "blackpawn.png")),  #NEW
            ("black","rook"):pygame.image.load(os.path.join(csgo_dir, "BLACKROOK.png")),  #NEW
            ("black","bishop"):pygame.image.load(os.path.join(csgo_dir, "black bishop.png")),  #NEW
            ("black","knight"):pygame.image.load(os.path.join(csgo_dir, "blackhorse.png"))  #NEW
            
        }
        return pygame.transform.scale(images[(color,piece)],(90,90))  # Scale to new square size  #NEW
    
    def draw(self,screen):
        square_size = 90  # Match the new square size
        board_start_y = 80  # Match the board start position
        screen.blit(self.image, ((self.file-1)*square_size,(8-self.rank)*square_size + board_start_y))
        
    def get_rect(self):
        square_size = 90  # Match the new square size
        board_start_y = 80  # Match the board start position
        return pygame.Rect((self.file-1)*square_size,(8-self.rank)*square_size + board_start_y, square_size, square_size)
    
    def set_position(self, x, y):
        self.file = x
        self.rank = y   

    def rook_movement(self, x, y):
        return self.file == x or self.rank == y
    
       
                
    
    
    
    # def checklegalmove(self,x,y):
    #     if piece[1] == rook