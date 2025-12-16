# IMPORT SECTION - This is where we import all necessary modules
import pygame
from Pieces import Piece

# NEW IMPORTS - These are the new modules we created for enhanced functionality  #NEW
from MainMenu import MainMenu      # Handles main menu screen and game initialization  #NEW
from UI import GameUI              # Handles player turn indicators and UI elements  #NEW
from Animations import GameAnimations  # Handles animations and visual polish  #NEW

# PYGAME INITIALIZATION - This initializes pygame and must come after imports
pygame.init()

# SCREEN SETUP - Variables that define the game window
screen_width = 800
screen_height = screen_width + 80  # Add space for UI at top  #NEW
screen = pygame.display.set_mode((screen_width, screen_height))

# BOARD SETTINGS - Define board size and position  #NEW
board_size = 720  # Slightly smaller than screen width  #NEW
board_start_y = 80  # Start board below the UI  #NEW
square_size = board_size // 8  # Each square size (90x90 instead of 100x100)  #NEW 

# INITIALIZE NEW SYSTEMS - Create instances of our new classes  #NEW
# MainMenu handles the start screen and game initialization  #NEW
main_menu = MainMenu(screen_width, screen_height)  #NEW

# GameUI handles player turn display and game status  #NEW
game_ui = GameUI(screen_width, screen_height)  #NEW

# GameAnimations handles visual effects and smooth transitions  #NEW
game_animations = GameAnimations(screen_width, screen_height)  #NEW

# GAME STATE VARIABLES - Track what state the game is in  #NEW
game_state = "menu"  # Can be "menu" or "playing"  #NEW
show_main_menu = True  #NEW

# CHESS PIECE INITIALIZATION - This creates all the chess pieces at their starting positions
pieces = [
    # White pieces - These are placed at the bottom of the board (ranks 1-2)
    Piece("rook","white",1,1),
    Piece("knight","white",2,1),
    Piece("bishop","white",3,1),
    Piece("queen","white",4,1),
    Piece("king","white",5,1),
    Piece("bishop","white",6,1),
    Piece("knight","white",7,1),
    Piece("rook","white",8,1),
    Piece("pawn","white",1,2),
    Piece("pawn","white",2,2),
    Piece("pawn","white",3,2),
    Piece("pawn","white",4,2),
    Piece("pawn","white",5,2),
    Piece("pawn","white",6,2),
    Piece("pawn","white",7,2),
    Piece("pawn","white",8,2),

    # Black pieces - These are placed at the top of the board (ranks 7-8)
    Piece("rook","black",1,8),
    Piece("knight","black",2,8),
    Piece("bishop","black",3,8),
    Piece("queen","black",4,8),
    Piece("king","black",5,8),
    Piece("bishop","black",6,8),
    Piece("knight","black",7,8),
    Piece("rook","black",8,8),
    Piece("pawn","black",1,7),
    Piece("pawn","black",2,7),
    Piece("pawn","black",3,7),
    Piece("pawn","black",4,7),
    Piece("pawn","black",5,7),
    Piece("pawn","black",6,7),
    Piece("pawn","black",7,7),
    Piece("pawn","black",8,7),
]

# GAME LOGIC SETUP - Variables for tracking game state during play
pygame.display.set_caption("Chess")  # Set the window title
running = True  # Main game loop control
selected_piece = None  # Currently selected piece (None if no piece selected)
available_moves = []  # List of valid moves for selected piece
current_turn = "white"  # Which player's turn it is (white always starts)

# TRACKING VARIABLES - For UI display purposes
captured_pieces_white = 0  # Number of pieces white has captured
captured_pieces_black = 0  # Number of pieces black has captured
game_status_message = ""  # Current game status (check, checkmate, etc.)
def checkclearpath(file,rank, capture, color):
    for I, piece in enumerate(pieces):
        P_File = piece.file - 1
        P_Rank = 8 - piece.rank
        colory = piece.color
        if P_File == file and P_Rank == rank:
            if capture and (color != colory):
                pieces.pop(I)
                #return True
            return False

    return True

def checkclearpath2(start_file, start_rank, end_file, end_rank, piece_type):  #NEW
    """
    Check if the path between start and end positions is clear of pieces  #NEW
    
    Args:  #NEW
        start_file (int): Starting file (1-8)  #NEW
        start_rank (int): Starting rank (1-8)   #NEW
        end_file (int): Ending file (1-8)  #NEW
        end_rank (int): Ending rank (1-8)  #NEW
        piece_type (str): Type of piece moving  #NEW
    
    Returns:  #NEW
        bool: True if path is clear, False if blocked  #NEW
    """
    # Convert to 0-based coordinates for easier math  #NEW
    start_x = start_file - 1  #NEW
    start_y = 8 - start_rank  #NEW
    end_x = end_file - 1    #NEW
    end_y = 8 - end_rank  #NEW
    
    # Calculate direction of movement  #NEW
    dx = 0 if end_x == start_x else (1 if end_x > start_x else -1)  #NEW
    dy = 0 if end_y == start_y else (1 if end_y > start_y else -1)  #NEW
    
    # Start checking from the square after the starting position  #NEW
    check_x = start_x + dx  #NEW
    check_y = start_y + dy  #NEW
    
    # Check each square along the path (excluding the destination)  #NEW
    while (check_x != end_x or check_y != end_y):  #NEW
        # Convert back to game coordinates  #NEW
        check_file = check_x + 1  #NEW
        check_rank = 8 - check_y  #NEW
        
        # Check if there's a piece at this position  #NEW
        for piece in pieces:  #NEW
            if piece.file == check_file and piece.rank == check_rank:  #NEW
                return False  # Path is blocked  #NEW
        
        # Move to next square in the path  #NEW
        check_x += dx  #NEW
        check_y += dy  #NEW
        
        # Safety check to prevent infinite loop  #NEW
        if abs(check_x - start_x) > 7 or abs(check_y - start_y) > 7:  #NEW
            break  #NEW
    
    return True  # Path is clear  #NEW



#rank = y file = x
def checklegalmove(color,piece,file,rank):
    #Pawn Logic 
    if piece == "pawn":
        if color == "black" and 9 - rank == new_y and (new_x == file-2 or new_x == file) and checkclearpath(new_x,new_y,True,color) == False and checkclearpath2(file, rank, new_x+1, 8-new_y, piece):
            return True
        elif color == "white" and  7  - rank == new_y and (new_x == file - 2 or new_x == file) and checkclearpath(new_x,new_y,True,color)== False and checkclearpath2(file, rank, new_x+1, 8-new_y, piece):
            return True
        elif color == "black" and rank == 7:
            if new_y <4 and new_y >1 and new_x == file-1 and checkclearpath(new_x,new_y,False,color) and checkclearpath2(file, rank, new_x+1, 8-new_y, piece):
                return True
            else:
                return False
        elif color == "white" and rank == 2:
            if new_y >= 4 and new_y <7 and new_x == file-1 and checkclearpath(new_x,new_y,False,color) and checkclearpath2(file, rank, new_x+1, 8-new_y, piece):
                return True
        else:
            if ((color == "black" and 9 - rank == new_y and new_x == file-1) or (color == "white" and  7  - rank == new_y and new_x == file - 1 )) and checkclearpath(new_x,new_y,False,color):
                return True
   #knight logic    
    if piece == "knight":
        for i in range(2):
            if  (((new_x == file - 2 or new_x == file) and (new_y == 10 - rank  or new_y == 6 - rank)) or ((new_x == file - 3 or new_x == file + 1 ) and (new_y== 9 - rank or new_y ==7- rank  ))) and (checkclearpath(new_x,new_y,True,color)!= False):
                return True
    #rook logic    
    if piece == "rook":
        if (new_x == file-1 or new_y == 8-rank) and checkclearpath(new_x,new_y,True,color) and checkclearpath2(file, rank, new_x+1, 8-new_y, "rook"):
            return True
    #king logic    
    if piece == "king":
        for i in range(2):
            if (((new_x == file-2 or new_x == file) and new_y == 8-rank) or ((new_y == 9-rank or new_y == 7-rank) and new_x == file-1 ) or (new_x == file-2 and new_y == 9-rank ) or ( new_x == file and new_y == 7-rank) or (new_x == file-2 and new_y == 7-rank) or (new_x == file and new_y == 9-rank )) and checkclearpath(new_x,new_y,True,color):
                return True
    #bishop logic    
    if piece =="bishop":
        x = file - 1 - new_x
        y = 8 - rank - new_y
        # Check if it's a valid diagonal move
        if abs(x) == abs(y) and checkclearpath(new_x,new_y,True,color) and checkclearpath2(file, rank, new_x+1, 8-new_y, "bishop"):
            return True
    #queen logic - combines rook and bishop movement
    if piece == "queen":
        x = file - 1 - new_x
        y = 8 - rank - new_y
        
        # Check if it's a valid rook-like move (straight line)
        is_rook_move = (new_x == file-1 or new_y == 8-rank)
        # Check if it's a valid bishop-like move (diagonal)
        is_bishop_move = abs(x) == abs(y)
        
        if (is_rook_move or is_bishop_move) and checkclearpath(new_x,new_y,True,color) and checkclearpath2(file, rank, new_x+1, 8-new_y, "queen"):
            return True


def get_available_moves(p):
    """
    Return a list of (tx, ty) grid positions (0..7) that `p` can move to.
    This temporarily sets the global `new_x`/`new_y` used by `checklegalmove`.
    """
    moves = []
    # save prior values if present
    prev_new_x = globals().get('new_x', None)
    prev_new_y = globals().get('new_y', None)
    # create a shallow copy of pieces so checks that remove captures
    # won't mutate the real game state while probing moves
    prev_pieces = globals().get('pieces', None)
    globals()['pieces'] = list(prev_pieces) if prev_pieces is not None else []

    for tx in range(0, 8):
        for ty in range(0, 8):
            globals()['new_x'] = tx
            globals()['new_y'] = ty
            try:
                if checklegalmove(p.color, p.piece, p.file, p.rank):
                    moves.append((tx, ty))
            except Exception:
                # if checklegalmove raises due to incomplete logic, ignore that square
                pass

    # restore previous globals
    if prev_new_x is None:
        if 'new_x' in globals():
            del globals()['new_x']
    else:
        globals()['new_x'] = prev_new_x
    if prev_new_y is None:
        if 'new_y' in globals():
            del globals()['new_y']
    else:
        globals()['new_y'] = prev_new_y

    # restore real pieces list
    globals()['pieces'] = prev_pieces

    return moves


    

 

# MAIN GAME LOOP - This runs continuously until the game is closed
while running:
    # EVENT HANDLING - Process all pygame events (mouse clicks, key presses, etc.)
    for event in pygame.event.get():
        # QUIT EVENT - When player clicks the X button
        if event.type == pygame.QUIT:
            running = False
            
        # MENU STATE EVENT HANDLING - When we're in the main menu
        elif game_state == "menu":
            menu_action = main_menu.handle_event(event)
            if menu_action == 'start':
                # GAME START - Transition from menu to playing state
                print("Starting new chess game...")
                game_state = "playing"
                show_main_menu = False
                current_turn = "white"  # White always starts first
                print(f"Game started! {current_turn.capitalize()} player goes first.")
            elif menu_action == 'quit':
                # QUIT FROM MENU
                running = False
                
        # PLAYING STATE EVENT HANDLING - When we're actually playing chess
        elif game_state == "playing" and event.type == pygame.MOUSEBUTTONDOWN:
            
            # PIECE SELECTION PHASE - If no piece is currently selected
            if selected_piece == None:
                 for p in pieces:
                    # CHECK FOR PIECE CLICK - See if clicked piece matches current turn
                    if p.get_rect().collidepoint(event.pos) and p.color == current_turn:
                        selected_piece = p
                        print(f"Selected {p.color} {p.piece} at position ({p.file}, {p.rank})")
                        
                        # CALCULATE AVAILABLE MOVES - Get valid moves for selected piece
                        available_moves = get_available_moves(selected_piece)
                        print(f"Available moves: {available_moves}")
                        
                        # START SELECTION ANIMATION - Visual feedback for piece selection
                        game_animations.animate_selection_pulse(selected_piece.get_rect())
                        game_animations.animate_valid_move_highlight(available_moves)
                        break  # Stop after selecting one piece
                        
            # PIECE MOVEMENT PHASE - A piece is already selected, now move it
            else: 
                print(f"Attempting to move to: {event.pos}")
                
                # CALCULATE BOARD POSITION - Convert mouse position to board coordinates
                new_x = event.pos[0]//square_size  # Convert pixel position to board column
                new_y = (event.pos[1] - board_start_y)//square_size  # Convert pixel position to board row (adjusted for UI)
                print(f"Board position: ({new_x}, {new_y})") 
                
                # VALIDATE AND EXECUTE MOVE - Check if move is legal, then execute
                if checklegalmove(selected_piece.color, selected_piece.piece, selected_piece.file, selected_piece.rank):
                    print(f"Legal move! Moving {selected_piece.color} {selected_piece.piece}")
                    
                    # CAPTURE DETECTION - Check if we're capturing an enemy piece
                    for i, piece in enumerate(pieces):
                        if (piece.file - 1 == new_x and 8 - piece.rank == new_y and 
                            piece.color != selected_piece.color):
                            print(f"Capturing {piece.color} {piece.piece}!")
                            
                            # ANIMATE CAPTURE - Visual feedback for captured piece
                            game_animations.animate_capture(piece)
                            
                            # UPDATE CAPTURE COUNTER - For UI display
                            if current_turn == "white":
                                captured_pieces_white += 1
                            else:
                                captured_pieces_black += 1
                                
                            # REMOVE CAPTURED PIECE
                            pieces.pop(i)
                            break
                    
                    # EXECUTE PIECE MOVEMENT - Update piece position with precise coordinates
                    old_pos = ((selected_piece.file-1) * square_size, (8-selected_piece.rank) * square_size + board_start_y)
                    target_file = new_x + 1
                    target_rank = 8 - new_y
                    new_pos = (new_x * square_size, new_y * square_size + board_start_y)
                    
                    # ANIMATE PIECE MOVEMENT - Smooth visual transition
                    game_animations.animate_piece_move(selected_piece, old_pos, new_pos, target_file, target_rank)
                    
                    # Don't immediately update piece position - let animation handle it
                    print(f"Animating {selected_piece.color} {selected_piece.piece} to ({target_file}, {target_rank})")
                    
                    # CLEAR SELECTION - Reset selection state
                    selected_piece = None
                    available_moves = []
                    
                    # CLEAR ANIMATIONS - Remove only selection highlights, keep movement animation
                    game_animations.stop_selection_animations()
                    
                    # CHANGE TURNS - Switch to other player
                    old_turn = current_turn
                    current_turn = "black" if current_turn == "white" else "white"
                    print(f"Turn changed from {old_turn} to {current_turn}")
                    
                    # ANIMATE TURN CHANGE - Visual feedback for turn switch
                    game_animations.animate_turn_change(screen, old_turn, current_turn)
                    
                else:
                    # INVALID MOVE - Clear selection and show feedback
                    print("Invalid move! Selection cleared.")
                    selected_piece = None
                    available_moves = []
                    
                    # CLEAR ANIMATIONS - Remove only selection highlights
                    game_animations.stop_selection_animations()

    # RENDERING SECTION - This draws everything on the screen each frame
    
    # MENU RENDERING - Draw main menu when in menu state
    if game_state == "menu":
        main_menu.draw(screen)
        
    # GAME RENDERING - Draw chess board and pieces when playing
    elif game_state == "playing":
        
        # BOARD BACKGROUND - Fill screen with white background
        screen.fill("White")
        
        # DRAW CHESSBOARD PATTERN - Create alternating black/white squares
        for J in range(board_start_y, board_start_y + board_size, square_size * 2):  # Draw the black squares 2 rows at a time
            for i in range(square_size, screen_width, square_size * 2):
                pygame.draw.rect(screen,(0,0,0),[i, J, square_size, square_size], 0)
            for i in range(0, screen_width, square_size * 2):
                pygame.draw.rect(screen,(0,0,0),[i, J + square_size, square_size, square_size], 0)
        
        # DRAW UI ELEMENTS - Player turn indicator and game status
        game_ui.draw_turn_indicator(screen, current_turn)
        game_ui.draw_player_info(screen, captured_pieces_white, captured_pieces_black)
        
        if selected_piece:
            # DRAW SELECTED PIECE INFO - Show which piece is selected
            game_ui.draw_selected_piece_info(screen, selected_piece)
        
        if game_status_message:
            # DRAW GAME STATUS - Show check, checkmate, etc.
            game_ui.draw_game_status(screen, game_status_message)

        # DRAW MOVE HIGHLIGHTS - Show available moves for selected piece
        if selected_piece is not None and available_moves:
            for tx, ty in available_moves:
                s = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                s.fill((0, 200, 0, 90))  # Translucent green for valid moves
                screen.blit(s, (tx * square_size, ty * square_size + board_start_y))

        # UPDATE ANIMATIONS - Process and draw any active animations
        game_animations.update_animations(screen)

        # DRAW CHESS PIECES - Render all pieces on their current positions
        for piece in pieces:
            # Skip drawing pieces that are currently being animated
            if not game_animations.is_piece_animating(piece):
                piece.draw(screen)

    # DISPLAY UPDATE - Show all rendered content on screen (MUST be at end of rendering)
    pygame.display.flip()

# CLEANUP - Close pygame when game loop ends
pygame.quit()
