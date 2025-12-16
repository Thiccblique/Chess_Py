board = ["-","-","-","-","-","-","-","-","-"]
wins = [
    #Horizantal Wins
    [0,1,2],
    [3,4,5],
    [6,7,8],
    #Vertical Wins
    [0,3,6],
    [1,4,7],
    [2,5,8],
    #Diagonal Wins
    [0,4,8],
    [2,4,6]
]

x_turn = True

x_spaces = []
o_spaces = []

while True:
    print(board[0:3])
    print(board[3:6])
    print(board[6:])
    space = int(input("What space do you want?(0-8) >"))

    if space in x_spaces or space in o_spaces:
        print("Already Claimed.")
        continue

    if x_turn:
        x_spaces.append(space)
        board[space] = "X"
    else:
        o_spaces.append(space)
        board[space] = "O"
    
    for win_state in wins:
        if x_turn:
            for num in win_state:
                if num not in x_spaces:
                    break
            else:
                print("X wins!")
                quit()
        else:
            for num in win_state:
                if num not in o_spaces:
                    break
            else:
                print("O wins!")
                quit()
    x_turn = not x_turn
    if len(x_spaces) + len(o_spaces) == 9:
        print("Cats!")
        quit()

