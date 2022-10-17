
import pygame
import random
import time
import socket

pygame.init()
pygame.font.init()

class Move():
    def __init__(self, startSQ, endSQ, boardState):
        self.stRow = startSQ[0]
        self.edRow = endSQ  [0]
        self.stCol = startSQ[1]
        self.edCol = endSQ  [1]

        self.PieceMoved    = boardState[self.stRow][self.stCol]
        self.PieceCaptured = boardState[self.edRow][self.edCol]
        self.PawnPormotion = False
        
        if ((self.PieceMoved == 'wp') and (self.edRow == 0)) or\
           ((self.PieceMoved == 'bp') and (self.edRow == 7)):

            self.PawnPormotion = True

        self.uqID = (self.stRow*1) +\
                    (self.edRow*10) +\
                    (self.stCol*100) +\
                    (self.edCol*1000)

        self.board = boardState

class GameBoard(object):
    def __init__(self):
        self.wKingPos  = (7,4)
        self.bKingPos  = (0,4)
        self.CheckMate = False
        self.StaleMate = False
        self.wMove     = True
        
        self.moveLogStack = []
        self.moveFunction = {
                            'p':self.getPawnMoves,
                            'R':self.getRookMoves,
                            'N':self.getKnightMoves,
                            'B':self.getBishopMoves,
                            'Q':self.getQueenMoves,
                            'K':self.getKingMoves
                            }
        self.board        = [
                            ["bR","bN","bB","bK","bQ","bB","bN","bR"],
                            ["bp","bp","bp","bp","bp","bp","bp","bp"],
                            ["--","--","--","--","--","--","--","--"],
                            ["--","--","--","--","--","--","--","--"],
                            ["--","--","--","--","--","--","--","--"],
                            ["--","--","--","--","--","--","--","--"],
                            ["wp","wp","wp","wp","wp","wp","wp","wp"],
                            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
                            ]


    def getPawnMoves(self, r, c, moves):
        if self.wMove == True:
            if (0<= r <8) and (0<= c <8):
                # forward 1
                if self.board[r-1][c] == '--':
                    moves.append(Move((r,c), (r-1,c), self.board))

                # forward 2
                if (self.board[r-2][c] == '--') and (r==6):
                    moves.append(Move((r,c), (r-2,c), self.board))

                # capture left
                if ((c-1) >=0) and (self.board[r-1][c-1][0] =='b'):
                    moves.append(Move((r,c), (r-1,c-1), self.board))

                # capture right
                if ((c+1) <=7) and (self.board[r-1][c+1][0] =='b'):
                    moves.append(Move((r,c), (r-1,c+1), self.board))

        elif self.wMove == False:
            if (0<= r <=8) and (0<= c <=8):
                # forward 1
                if self.board[r+1][c] == '--':
                    moves.append(Move((r,c), (r+1,c), self.board))

                # forward 2
                if (r == 1):
                    if (self.board[r+2][c] == '--') and (r==1):
                        moves.append(Move((r,c), (r+2,c), self.board))

                # capture left
                if ((c-1) >=0) and (self.board[r+1][c-1][0] =='w'):
                    moves.append(Move((r,c), (r+1,c-1), self.board))

                # capture right
                if ((c+1) <=7) and (self.board[r+1][c+1][0] =='w'):
                    moves.append(Move((r,c), (r+1,c+1), self.board))

                                    
    def getRookMoves(self, r, c, moves):

        RookMoves = ((-1, 0), # left
                     ( 1, 0), # right
                     ( 0,-1), # down
                     ( 0, 1)) # up

        if self.wMove == True:
            enemyColor = 'b'
            allyColor  = 'w'
        else:
            enemyColor = 'w'
            allyColor  = 'b'

        # cycle through all the directions the rook can move
        # if the square is empty then add to moves list
        # if the square is an enemy then add to moves list
        # after an enemy is detected or reach end of board, break out of loop
        
        for m in RookMoves:
            for i in range(1,8):
                edRow = r+(m[0] *i)
                edCol = c+(m[1] *i)

                if (0<= edRow <8) and (0<= edCol <8):
                    edPiece = self.board[edRow][edCol]

                    if edPiece == '--':
                        moves.append(Move((r,c), (edRow,edCol), self.board))
                    elif edPiece[0] == enemyColor:
                        moves.append(Move((r,c), (edRow,edCol), self.board))
                        break
                    else:
                        break
                else:
                    break
                
        
    def getKingMoves(self, r, c, moves):
        
        KingMoves = ((-1,-1), # bottom left
                     (-1, 0), # bottom
                     (-1, 1), # bottom right
                     ( 0,-1), # left
                     ( 0, 1), # right
                     ( 1,-1), # top left
                     ( 1, 0), # top
                     ( 1, 1)) # top right

        if self.wMove == True:
            enemyColor = 'b'
            allyColor  = 'w'
        else:
            enemyColor = 'w'
            allyColor  = 'b'
            
        # loop through 0 to 7 and figure out what the
        # end row is and what the ed collum is
        # check if the square has an ally piece, if it
        # does then dont put the move in the moves list
        
        for i in range(8):
            edRow = r+KingMoves[i][0]
            edCol = c+KingMoves[i][1]

            if (0<= edRow <8) and (0<= edCol <8):
                edPiece = self.board[edRow][edCol]

                if edPiece[0] != allyColor:
                    moves.append(Move((r,c), (edRow,edCol), self.board))
        
    def getBishopMoves(self, r, c, moves):
        
        BishopMoves = ((-1,-1), # bottom left
                       ( 1, 1), # top right
                       ( 1,-1), # bottom right
                       (-1, 1)) # top left

        if self.wMove == True:
            enemyColor = 'b'
            allyColor  = 'w'
        else:
            enemyColor = 'w'
            allyColor  = 'b'

        # loop through all the directions a bishop move
        # for each direction see if the square is empty, if
        # it is then add the move to the moves list
        # if it is an enmey piece then add it to the moves list and break the loop
        
        for m in BishopMoves:
            for i in range(1,8):
                edRow = r+(m[0] *i)
                edCol = c+(m[1] *i)
                
                if (0<= edRow <8) and (0<= edCol <8):
                    edPiece = self.board[edRow][edCol]

                    if edPiece == '--':
                        moves.append(Move((r,c), (edRow,edCol), self.board))
                    elif edPiece[0] == enemyColor:
                        moves.append(Move((r,c), (edRow,edCol), self.board))
                        break
                    else:
                        break
                else:
                    break

        
    def getQueenMoves(self, r, c, moves):
        
        # a queen is basically all the bishop moves and
        # all the rook moves togather so we just call the
        # 2 funtions and that is all we need.
        
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

        
    def getKnightMoves(self, r, c, moves):
        KnightMoves = ((-2,-1),
                       (-2, 1),
                       (-1,-2),
                       (-1, 2),
                       ( 1, 2),
                       ( 1,-2),
                       ( 2,-1),
                       ( 2, 1))

        if self.wMove == True:
            enemyColor = 'b'
            allyColor  = 'w'
        else:
            enemyColor = 'w'
            allyColor  = 'b'
            
        # loop through the knght moves and checks if the square is not an
        # ally piece and also checks if there is an enemy piece.
        # Then it adds it to the moves list

        for m in KnightMoves:
            edRow = r + m[0]
            edCol = c + m[1]

            if (0 <= edRow < 8) and (0 <= edCol < 8):
                edPiece = self.board[edRow][edCol]

                if (edPiece[0] != allyColor) or (edPiece[0] == enemyColor) or (edPiece[0] == '--'):
                    moves.append(Move((r,c), (edRow,edCol), self.board))

        
    def inCheck(self):

        #if king in check then return true else return false
        
        if self.wMove == True:
            return self.SQunderAttack(self.wKingPos[0], self.wKingPos[1])
        else:
            return self.SQunderAttack(self.bKingPos[0], self.bKingPos[1])
        
    def SQunderAttack(self, r, c):

        # gets all the possible oppoent moves ands sees if any of them land on the
        # king position. if it does return true or else return false

        self.wMove = not self.wMove
        oppMoves = self.getPossibleMoves()
        self.wMove = not self.wMove

        for m in oppMoves:
            if (m.edRow ==r) and (m.edCol ==c):
                return True

        return False

        
    def getPossibleMoves(self):
        moves = []

        # loops through each square on the board and finds all the
        # possible moves and add it to the moves list.
        
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                color = self.board[r][c][0]
                piece = self.board[r][c][1]

                if (color == 'w' and self.wMove == True) or\
                   (color == 'b' and self.wMove == False):

                    self.moveFunction[piece](r, c, moves)

        return moves

                
    def getValidMoves(self):
        moves = self.getPossibleMoves()

        # goes through all the possible moves on the board thats possible
        # then it makes the moves and checks if it is in a check state. if it
        # is then it removes. it undos the move and repeat until it goes through
        # all the moves.
        # after it checks if any more moves are possible, if not then it could
        # either be a check mate or stale mate.

        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.wMove = not self.wMove

            if self.inCheck() == True:
                moves.remove(moves[i])

            self.undoMove()
            self.wMove = not self.wMove

        if len(moves) == 0:
            if self.inCheck() == True:
                self.CheckMate = True

            else:
                self.StaleMate = True
        else:
            self.CheckMate = False
            self.StaleMate = False

        return moves


    def makeMove(self, move):

        # makes the move by replacing the starting square with an empty one
        # and moves the piece to the ending square
        # updates the kings position if it is moved and adds the moves to
        # the log stack.
        
        self.board[move.stRow][move.stCol] = '--'
        self.board[move.edRow][move.edCol] = move.PieceMoved
        self.wMove = not self.wMove
        self.moveLogStack.append(move)

        if move.PieceMoved == 'wK':
            self.wKingPos = (move.edRow, move.edCol)
        elif move.PieceMoved == 'bK':
            self.bKingPos = (move.edRow, move.edCol)

        if move.PawnPormotion == True:
            self.board[move.edRow][move.edCol] = move.PieceMoved[0] + 'Q'


    def undoMove(self):

        # checks if the log is empty cause you can remove stuff if stack is empty
        # pops the top most recent moves and makes that move
        # updates the kings position
        
        if len(self.moveLogStack) != 0:
            move = self.moveLogStack.pop()

            self.board[move.stRow][move.stCol] = move.PieceMoved
            self.board[move.edRow][move.edCol] = move.PieceCaptured
            self.wMove = not self.wMove

            if move.PieceMoved == 'wK':
                self.wKingPos = (move.stRow, move.stCol)
            elif move.PieceMoved == 'bK':
                self.bKingPos = (move.stRow, move.stCol)

# -------------------------------------------------------------------------------------------------
Black   = (0,0,0)
White   = (255,255,255)
Red     = (255,0,0)
Lime    = (0,255,0)
Blue    = (0,0,255)
Yellow  = (255,255,0)
Cyan    = (0,255,255)
Magenta = (255,0,255)
Silver  = (192,192,192)
Gray    = (128,128,128)
Maroon  = (128,0,0)
Olive   = (128,128,0)
Green   = (0,128,0)
Purple  = (128,0,128)
Teal    = (0,128,128)
Navy    = (0,0,128)

windowWidth  = 600
windowHeight = 520

window  = pygame.display.set_mode((windowWidth,windowHeight))
caption = pygame.display.set_caption('Chess')
screen  = 0
load    = pygame.image.load
clock   = pygame.time.Clock()


myfont1 = pygame.font.SysFont('Comic Sans MS', 35)
myfont2 = pygame.font.Font("Hollow.ttf", 100)
myfont3 = pygame.font.Font("Evander-ExtraBold.ttf", 100)
myfont4 = pygame.font.Font("Evander-ExtraBold.ttf", 30)
myfont5 = pygame.font.Font("Evander-ExtraBold.ttf", 37)
myfont6 = pygame.font.Font("Evander-ExtraBold.ttf", 25)
myfont7 = pygame.font.Font("Evander-ExtraBold.ttf", 70)
l = '\''

boards = [load('chessboard.png') , load('chessboard2.png'),
          load('chessboard3.png'), load('chessboard4.png'),
          load('chessboard5.png')]
piece = [load('wK.png'), load('wK2.png'), load('wK3.png')]
piecename = ['Pieces 1', 'Pieces 2', 'Pieces 3']
boardname = ['Chessboard 1', 'Chessboard 2', 'Chessboard 3',
             'Chessboard 4', 'Chessboard 5']
pieces = ['wp','bp','wR','bR','wN','bN','wB','bB','wQ','bQ','wK','bK']
pieceImages = {}
num  = 0
num2 = 0

gameboard = GameBoard()
validMoves = gameboard.getValidMoves()
chessboard = boards[0]
pieceset = 0
fps = 60

#------------------------------------------------------------------------------------------------------------------------------------------------------


def textbox(font, text, x, y, color):
    surface = font.render(text, True, color)
    window.blit(surface, (x, y))

def selected_row(x,y,bpx,bpy):
    for i in range(8):
        if ( (bpy+((i+1)*62)) >= y >= (bpy+(i*62))):
            row = i
    return row

def selected_col(x,y,bpx,bpy):
    for i in range(8):
        if ( (((i+1)*62)+bpx) >= x >= (bpx+(i * 62)) ):
            col = i
    return col

def load_images():
    global pieceImages
    l = str(pieceset+1)
    
    if pieceset == 0:
        for i in pieces:
            name = str(i + '.png')
            pieceImages[i] = load(name)
            pieceImages[i] = pygame.transform.scale(pieceImages[i], (62,62))
            pieceImages[i] = pieceImages[i].convert_alpha()
    else:
        for i in pieces:
            name = str(i + l + '.png')
            pieceImages[i] = load(name)
            pieceImages[i] = pygame.transform.scale(pieceImages[i], (62,62))
            pieceImages[i] = pieceImages[i].convert_alpha()
        

def draw_board(surface, chessboard, vm, gb, sqq, bpx,bpy):
    surface.blit(chessboard, (bpx,bpy))
    Highlight(surface, vm, sqq, gb, bpx,bpy)

    for r in range(8):
        for c in range(8):
            x = c*62
            y = r*62

            p = gb.board[r][c]
            if p != '--':
                surface.blit(pieceImages[p], (x+bpx,y+bpy))

def Highlight(surface, vm, sqq,gb, bpx,bpy):
    if sqq != ():
        r,c = sqq

        if ((gb.board[r][c][0] == 'w') and (gb.wMove == True)) or\
           ((gb.board[r][c][0] == 'b') and (gb.wMove == False)):

           square = pygame.Surface((62,62))
           square.set_alpha(200)
           square.fill(Purple)

           x = ((c*62) +1)+bpx
           y = ((r*62) +1)+bpy

           surface.blit(square, (x,y))
           pygame.draw.rect(window, Black, (x,y,62,62), 1)

           square.fill(Red)
           for m in vm:
               if m.stRow == r and m.stCol == c:
                   x = ((m.edCol*62) +1) +bpx
                   y = ((m.edRow*62) +1) +bpy

                   surface.blit(square, (x,y))
                   pygame.draw.rect(window, Black, (x,y,62,62), 1)

def ai(vm):
    num = random.randint(0,len(vm)-1)
    #print(len(vm))
    return vm[num]

def inter(text):
    num = ['1','2','3','4','5','6','7','8','9','0']
    temp = []
    #[(1, 2), (3, 2)]
    text = list(text)
    for i in text:
        if i in num:
            temp.append(int(i))

    pc = [(7-temp[0],7-temp[1]), (7-temp[2],7-temp[3])]
    return pc
    









def menu():
    global screen

    # Loading the pictures and scaling them to fit the screen
    # Also set the coordinates for each picture
    knl = load('wN.png')
    knl2= load('wN.png')
    pwl = load('wp.png')
    pwl2= load('wp.png')
    knl = pygame.transform.scale(knl , (150,150))
    knl2= pygame.transform.scale(knl2, (180,180))
    pwl = pygame.transform.scale(pwl , (150,150))
    pwl2= pygame.transform.scale(pwl2, (180,180))

    x1 = windowWidth //2 -150
    y1 = windowHeight//2 -75
    x2 = windowWidth //2 +25
    y2 = windowHeight//2 -75
    wt,ht = myfont3.size("Chess")
    xt = int((windowWidth /2) - (wt/2))
    yt = ht

    while screen == 0:
        p,m = pygame.mouse.get_pos()
        window.fill(Black)
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen = 9

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (x1+150>p>x1) and (y1+150>m>y1):
                        screen = 1

                    elif (x2+150>p>x2) and (y2+150>m>y2):
                        screen = 2

            

        if (x1+150>p>x1) and (y1+150>m>y1):
            window.blit(knl2, (x1-15,y1-15))
        else:
            window.blit(knl, (x1, y1))




        if (x2+150>p>x2) and (y2+150>m>y2):
            window.blit(pwl2, (x2-15,y2-15))
        else:
            window.blit(pwl, (x2, y2))

        textbox(myfont3, 'Chess', xt, 0, White)
        textbox(myfont4, 'Login', x1+50, y1+150, White)
        textbox(myfont4, 'Register', x2+10, y2+150, White)
        pygame.draw.rect(window, White, (xt,yt,wt,20))
        
        pygame.display.update()

        
def login():
    global screen

    wt,ht = myfont3.size("Chess")
    xt = int((windowWidth /2) - (wt/2))
    xt = int((windowWidth /2) - (wt/2))
    yt = ht

    us = False
    pw = False

    ttext = ''
    btext = ''

    count = 0

    while screen == 1:
        p,m = pygame.mouse.get_pos()
        window.fill(Black)
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen = 9

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (0<p<41) and (0<m<41):
                        screen = 0

                    elif ((xt+150)<p<(xt+150+180)) and ((ht+60)<m<(ht+60+45)):
                        us = True
                        pw = False
                        count = 0

                    elif ((xt+150)<p<(xt+150+180)) and ((ht+140)<m<(ht+140+45)):
                        us = False
                        pw = True
                        count = 0

                    elif ((xt+60)<p<(xt+60+150)) and ((400)<m<(450)):
                        us = False
                        pw = False
                        count = 0
                        screen = 3

                    else:
                        us = False
                        pw = False
                        count = 0

            if event.type == pygame.KEYDOWN:
                if us == True:
                    if event.key == pygame.K_BACKSPACE:
                        ttext = ttext[:-1]
                    else:
                        ttext += event.unicode
                        width, height = myfont6.size(ttext)

                        if width > 178:
                            ttext = ttext[:-1]

                elif pw == True:
                    if event.key == pygame.K_BACKSPACE:
                        btext = btext[:-1]
                    else:
                        btext += event.unicode
                        width, height = myfont6.size(btext)

                        if width > 178:
                            btext = btext[:-1]
                            

        textbox(myfont3, 'Chess', xt, 0, White)
        
        textbox(myfont6, 'UserName:', xt-30, ht+60, White)
        pygame.draw.rect(window, White, (xt+150, ht+60, 180, 45),5)
        if us == True:
            width,height = myfont6.size(ttext)

            xl = xt+150 + width+3
            yl = ht+60 + 5
            w = 2
            h = 35

            if (0 <= count <= 10):
                pygame.draw.rect(window, White, (xl,yl,w,h))
            elif count >30:
                count = 0


        textbox(myfont6, 'PassWord:', xt-30, ht+140, White)
        pygame.draw.rect(window, White, (xt+150, ht+140, 180, 45),5)
        if pw == True:
            width,height = myfont6.size(btext)

            xl = xt+150 + width+3
            yl = ht+140 + 5
            w = 2
            h = 35

            if (0 <= count <= 10):
                pygame.draw.rect(window, White, (xl,yl,w,h))
            elif count >30:
                count = 0
                

        # display the back button
        pygame.draw.line(window, White, (7,20), (20,4), 5)
        pygame.draw.line(window, White, (7,20), (20,36), 5)
        pygame.draw.line(window, White, (7,20), (35,20), 5)
        pygame.draw.rect(window, White, (0,0,41,41), 4)

        
        pygame.draw.rect(window, White, (xt,yt,wt,20))

        textsurface1 = myfont6.render(ttext, False, White)
        window.blit(textsurface1, ((xt+153),(ht+63)))
        textsurface2 = myfont6.render(btext, False, White)
        window.blit(textsurface2, ((xt+153),(ht+143)))

        if ((xt+60)<p<(xt+60+150)) and ((400)<m<(450)):
            pygame.draw.rect(window, White, (xt+55, 395, 160, 60), 5)
            textbox(myfont5, '  Login', xt+60, 400, White)
            

            
        else:
            pygame.draw.rect(window, White, (xt+60, 400, 150, 50), 5)
            textbox(myfont4, '   Login', xt+70, 405, White)


        pygame.display.update()
        count += 1


def register():
    global screen
    
    wt,ht = myfont3.size("Chess")
    xt = int((windowWidth /2) - (wt/2))
    xt = int((windowWidth /2) - (wt/2))
    yt = ht

    fn = False
    ln = False
    un = False
    pw = False

    ftext = ''
    ltext = ''
    utext = ''
    ptext = ''

    count = 0

    while screen == 2:
        p,m = pygame.mouse.get_pos()
        window.fill(Black)
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen = 9

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (0<p<41) and (0<m<41):
                        screen = 0

                    if ((xt+160)<p<(xt+160+180)) and ((160)<m<(200)):
                        fn = True
                        ln = False
                        un = False
                        pw = False

                    elif ((xt+160)<p<(xt+160+180)) and ((210)<m<(250)):
                        fn = False
                        ln = True
                        un = False
                        pw = False

                    elif ((xt+160)<p<(xt+160+180)) and ((260)<m<(300)):
                        fn = False
                        ln = False
                        un = True
                        pw = False

                    elif ((xt+160)<p<(xt+160+180)) and ((310)<m<(350)):
                        fn = False
                        ln = False
                        un = False
                        pw = True

                    elif ((xt+60)<p<(xt+60+150)) and ((400)<m<(450)):
                        screen = 0
                        fn = False
                        ln = False
                        un = False
                        pw = False

                    else:
                        fn = False
                        ln = False
                        un = False
                        pw = False
                        count = 0


            elif event.type == pygame.KEYDOWN:
                if fn == True:
                    if event.key == pygame.K_BACKSPACE:
                        ftext = ftext[:-1]
                    else:
                        ftext += event.unicode
                        width, height = myfont6.size(ftext)

                        if width > 175:
                            ftext = ftext[:-1]

                elif ln == True:
                    if event.key == pygame.K_BACKSPACE:
                        ltext = ltext[:-1]
                    else:
                        ltext += event.unicode
                        width, height = myfont6.size(ltext)

                        if width > 175:
                            ltext = ltext[:-1]

                elif un == True:
                    if event.key == pygame.K_BACKSPACE:
                        utext = utext[:-1]
                    else:
                        utext += event.unicode
                        width, height = myfont6.size(utext)

                        if width > 175:
                            utext = utext[:-1]

                elif pw == True:
                    if event.key == pygame.K_BACKSPACE:
                        ptext = ptext[:-1]
                    else:
                        ptext += event.unicode
                        width, height = myfont6.size(ptext)

                        if width > 175:
                            ptext = ptext[:-1]

                





        textbox(myfont3, 'Chess', xt, 0, White)

        textbox(myfont6, 'First Name:', xt, 160, White)
        pygame.draw.rect(window, White, (xt+160, 160, 180, 40), 5)

        if fn == True:
            width,height = myfont6.size(ftext)

            xl = xt+160 + width+3
            yl = 160 + 5
            w = 2
            h = 35

            if (0 <= count <= 10):
                pygame.draw.rect(window, White, (xl,yl,w,h))
            elif count >30:
                count = 0


        
        textbox(myfont6, ' Last Name:', xt, 210, White)
        pygame.draw.rect(window, White, (xt+160, 210, 180, 40), 5)

        if ln == True:
            width,height = myfont6.size(ltext)

            xl = xt+160 + width+3
            yl = 210 + 5
            w = 2
            h = 35

            if (0 <= count <= 10):
                pygame.draw.rect(window, White, (xl,yl,w,h))
            elif count >30:
                count = 0


        
        textbox(myfont6, ' User Name:', xt-6, 260, White)
        pygame.draw.rect(window, White, (xt+160, 260, 180, 40), 5)

        if un == True:
            width,height = myfont6.size(utext)

            xl = xt+160 + width+3
            yl = 260 + 5
            w = 2
            h = 35

            if (0 <= count <= 10):
                pygame.draw.rect(window, White, (xl,yl,w,h))
            elif count >30:
                count = 0



        
        textbox(myfont6, '  PassWord:', xt, 310, White)
        pygame.draw.rect(window, White, (xt+160, 310, 180, 40), 5)

        if pw == True:
            width,height = myfont6.size(ptext)

            xl = xt+160 + width+3
            yl = 310 + 5
            w = 2
            h = 35

            if (0 <= count <= 10):
                pygame.draw.rect(window, White, (xl,yl,w,h))
            elif count >30:
                count = 0
        
        pygame.draw.line(window, White, (7,20), (20,4), 5)
        pygame.draw.line(window, White, (7,20), (20,36), 5)
        pygame.draw.line(window, White, (7,20), (35,20), 5)
        pygame.draw.rect(window, White, (0,0,41,41), 4)
        pygame.draw.rect(window, White, (xt,yt,wt,20))

        textsurface1 = myfont6.render(ftext, False, White)
        window.blit(textsurface1, ((xt+165),(164)))

        textsurface2 = myfont6.render(ltext, False, White)
        window.blit(textsurface2, ((xt+165),(214)))

        textsurface3 = myfont6.render(utext, False, White)
        window.blit(textsurface3, ((xt+165),(264)))

        textsurface4 = myfont6.render(ptext, False, White)
        window.blit(textsurface4, ((xt+165),(314)))



        if ((xt+60)<p<(xt+60+150)) and ((400)<m<(450)):
            pygame.draw.rect(window, White, (xt+55, 395, 160, 60), 5)
            textbox(myfont5, '  Done ', xt+60, 400, White)

            
        else:
            pygame.draw.rect(window, White, (xt+60, 400, 150, 50), 5)
            textbox(myfont4, '   Done ', xt+70, 405, White)

        

        pygame.display.update()
        count += 1

def game_menu():
    global screen
    knl = load('wN.png')
    knl2= load('wN.png')
    pwl = load('wp.png')
    pwl2= load('wp.png')
    rkl = load('wR.png')
    rkl2= load('wR.png')
    bsl = load('wB.png')
    bsl2= load('wB.png')
    sett = load('settings.png')

    
    knl = pygame.transform.scale(knl , (150,150))
    knl2= pygame.transform.scale(knl2, (180,180))
    pwl = pygame.transform.scale(pwl , (150,150))
    pwl2= pygame.transform.scale(pwl2, (180,180))
    rkl = pygame.transform.scale(rkl , (150,150))
    rkl2= pygame.transform.scale(rkl2, (180,180))
    bsl = pygame.transform.scale(bsl , (150,150))
    bsl2= pygame.transform.scale(bsl2, (180,180))
    sett = pygame.transform.scale(sett, (50,50))

    y  = 170
    x1 = 0
    x2 = 150
    x3 = 300
    x4 = 450
  


    
    wt,ht = myfont3.size("Chess")
    xt = int((windowWidth /2) - (wt/2))
    xt = int((windowWidth /2) - (wt/2))
    yt = ht

    while screen == 3:
        p,m = pygame.mouse.get_pos()
        window.fill(Black)
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen = 9

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (0<p<41) and (0<m<41):
                        screen = 0

                    if ((x1)<p<(x1+150)) and ((y)<m<(y+150)):
                        screen = 5

                    if ((x2)<p<(x2+150)) and ((y)<m<(y+150)):
                        screen = 6

                    if ((x3)<p<(x3+150)) and ((y)<m<(y+150)):
                        screen = 7

                    if ((x4)<p<(x4+150)) and ((y)<m<(y+150)):
                        screen = 8

                    if ((540)<p<(590)) and ((465)<m<(465+50)):
                        screen = 4


        textbox(myfont3, 'Chess', xt, 0, White)
        pygame.draw.rect(window, White, (xt,yt,wt,20))

            
        if ((x1)<p<(x1+150)) and ((y)<m<(y+150)):
            window.blit(knl2, (x1-15,y-15))
        else:
            window.blit(knl, (x1,y))

        if ((x2)<p<(x2+150)) and ((y)<m<(y+150)):
            window.blit(pwl2, (x2-15,y-15))
        else:
            window.blit(pwl, (x2,y))

        if ((x3)<p<(x3+150)) and ((y)<m<(y+150)):
            window.blit(rkl2, (x3-15,y-15))
        else:
            window.blit(rkl, (x3,y))

        if ((x4)<p<(x4+150)) and ((y)<m<(y+150)):
            window.blit(bsl2, (x4-15,y-15))
        else:
            window.blit(bsl, (x4,y))


        window.blit(sett, (540,465))

        textbox(myfont6, 'Player', 50, 315, White)
        textbox(myfont6, '   vs ', 50, 340, White)
        textbox(myfont6, 'Player', 50, 365, White)

        textbox(myfont6, 'Player', 185, 315, White)
        textbox(myfont6, '   vs ', 185, 340, White)
        textbox(myfont6, '  cpu ', 185, 365, White)

        textbox(myfont6, ' Host', 337, 315, White)
        textbox(myfont6, ' Join', 490, 315, White)
        
        

        # display the back button
        pygame.draw.line(window, White, (7,20), (20,4), 5)
        pygame.draw.line(window, White, (7,20), (20,36), 5)
        pygame.draw.line(window, White, (7,20), (35,20), 5)
        pygame.draw.rect(window, White, (0,0,41,41), 4)
        
        
        pygame.display.update()



def settings():
    global screen, chessboard, pieceset,num,num2
    wt,ht = myfont7.size("Settings")
    xt = int((windowWidth /2) - (wt/2))


    name  = boardname[num]
    name2 = piecename[num2]

    while screen == 4:
        p,m = pygame.mouse.get_pos()
        window.fill(Black)
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen = 9

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (0<p<41) and (0<m<41):
                        screen = 3
                        chessboard = boards[num]
                        pieceset = num2
                        load_images()
                        

                    elif (170<p<190) and (120<m<160):
                        num -= 1
                        if num <0:
                            num = 0
                            name = boardname[num]

                        else:
                            name = boardname[num]

                    elif (390<p<410) and (120<m<160):
                        num += 1
                        if num>len(boardname) -1:
                            num = len(boardname) -1
                            name = boardname[num]
                        else:
                            name = boardname[num]

                    elif (170<p<190) and (350<m<390):
                        num2 -= 1
                        if num2 <0:
                            num2 = 0
                            name2 = piecename[num2]

                        else:
                            name2 = piecename[num2]

                    elif (390<p<410) and (350<m<390):
                        num2 += 1
                        if num2 >len(piecename) -1:
                            num2 = len(piecename) -1
                            name2 = piecename[num2]

                        else:
                            name2 = piecename[num2]
                
                        
                            

        textbox(myfont7, 'Settings', xt,0, White)

        pygame.draw.line(window, White, (170,140), (190,120), 5)
        pygame.draw.line(window, White, (170,140), (190,160), 5)
        pygame.draw.line(window, White, (190,120), (190,160), 5)

        pygame.draw.line(window, White, (390,120), (410,140), 5)
        pygame.draw.line(window, White, (390,160), (410,140), 5)
        pygame.draw.line(window, White, (390,160), (390,120), 5)

        textbox(myfont6,name, 205, 120, White)
        b = pygame.transform.scale(boards[num], (180,180))
        window.blit(b, (203,160) )

        pygame.draw.line(window, White, (170,370), (190,350), 5)
        pygame.draw.line(window, White, (170,370), (190,390), 5)
        pygame.draw.line(window, White, (190,350), (190,390), 5)

        pygame.draw.line(window, White, (390,350), (410,370), 5)
        pygame.draw.line(window, White, (390,390), (410,370), 5)
        pygame.draw.line(window, White, (390,390), (390,350), 5)

        textbox(myfont6,name2, 240, 355, White)
        if num2 == 1:
            p = pygame.transform.scale(piece[num2], (170,120))
            window.blit(p, (210,360))
        elif num2 == 2:
            p = pygame.transform.scale(piece[num2], (75,75))
            window.blit(p, (250,390))
        else:
            p = pygame.transform.scale(piece[num2], (100,100))
            window.blit(p, (240,380))

        


        pygame.draw.line(window, White, (7,20), (20,4), 5)
        pygame.draw.line(window, White, (7,20), (20,36), 5)
        pygame.draw.line(window, White, (7,20), (35,20), 5)
        pygame.draw.rect(window, White, (0,0,41,41), 4)

        

        

        pygame.display.update()

    

def PVP():
    global screen, chessboard

    gameboard  = GameBoard()
    validMoves = gameboard.getValidMoves()
    SQselected   = ()
    playerClicks = []
    moveMade = False
    stSQ =0
    edSQ =0

    bpx = 51
    bpy = 11

    
    

    while screen == 5:
        p,m = pygame.mouse.get_pos()
        window.fill(Black)
        clock.tick(fps)

        if moveMade == True:
            validMoves = []
            validMoves = gameboard.getValidMoves()
            moveMade = False


            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen = 9

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (0<p<41) and (0<m<41):
                        screen = 3
                    
                    if (bpx<p<497+bpx) and (bpy<m<497+bpy):
                        row = selected_row(p,m,bpx,bpy)
                        col = selected_col(p,m,bpx,bpy)

                        if SQselected == (row,col):
                            SQselected   = ()
                            playerClicks = []

                        else:
                            SQselected = (row,col)
                            playerClicks.append(SQselected)


                        if len(playerClicks) == 2:
                            move = Move(playerClicks[0], playerClicks[1], gameboard.board)

                            for i in range(len(validMoves)):
                                if move.uqID == validMoves[i].uqID:
                                    gameboard.makeMove(validMoves[i])
                                    moveMade = True
                                    SQselected   = ()
                                    playerClicks = []


                            if not moveMade:
                                playerClicks = [SQselected]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gameboard.undoMove()
                    moveMade = True



        pygame.draw.line(window, White, (7,20), (20,4), 5)
        pygame.draw.line(window, White, (7,20), (20,36), 5)
        pygame.draw.line(window, White, (7,20), (35,20), 5)
        pygame.draw.rect(window, White, (0,0,41,41), 4)



        draw_board(window, chessboard, validMoves, gameboard, SQselected,bpx,bpy)
        pygame.display.update()

load_images()

def PVC():
    global screen, chessboard

    gameboard  = GameBoard()
    validMoves = gameboard.getValidMoves()
    SQselected   = ()
    playerClicks = []
    moveMade = False
    stSQ =0
    edSQ =0

    bpx = 51
    bpy = 11

    
    

    while screen == 6:
        p,m = pygame.mouse.get_pos()
        window.fill(Black)
        clock.tick(fps)

        if moveMade == True:
            validMoves = []
            validMoves = gameboard.getValidMoves()
            moveMade = False


            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen = 9

            if gameboard.wMove == False:
                move = ai(validMoves)
                gameboard.makeMove(move)
                moveMade = True
                
                
            elif gameboard.wMove == True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if (0<p<41) and (0<m<41):
                            screen = 3
                        
                        if (bpx<p<497+bpx) and (bpy<m<497+bpy):
                            row = selected_row(p,m,bpx,bpy)
                            col = selected_col(p,m,bpx,bpy)

                            if SQselected == (row,col):
                                SQselected   = ()
                                playerClicks = []

                            else:
                                SQselected = (row,col)
                                playerClicks.append(SQselected)


                            if len(playerClicks) == 2:
                                move = Move(playerClicks[0], playerClicks[1], gameboard.board)

                                for i in range(len(validMoves)):
                                    if move.uqID == validMoves[i].uqID:
                                        gameboard.makeMove(validMoves[i])
                                        moveMade = True
                                        SQselected   = ()
                                        playerClicks = []


                                if not moveMade:
                                    playerClicks = [SQselected]

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        gameboard.undoMove()
                        moveMade = True



        pygame.draw.line(window, White, (7,20), (20,4), 5)
        pygame.draw.line(window, White, (7,20), (20,36), 5)
        pygame.draw.line(window, White, (7,20), (35,20), 5)
        pygame.draw.rect(window, White, (0,0,41,41), 4)



        draw_board(window, chessboard, validMoves, gameboard, SQselected,bpx,bpy)
        pygame.display.update()


def hostset():
    global screen
    online = True

    while online == True:
        p,m = pygame.mouse.get_pos()
        window.fill(Black)
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                online = False


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (0<p<41) and (0<m<41):
                        screen = 3


        pygame.draw.line(window, White, (7,20), (20,4), 5)
        pygame.draw.line(window, White, (7,20), (20,36), 5)
        pygame.draw.line(window, White, (7,20), (35,20), 5)
        pygame.draw.rect(window, White, (0,0,41,41), 4)

        pygame.display.update()
                        
        



def host():
    global screen, chessboard


    gameboard  = GameBoard()
    validMoves = gameboard.getValidMoves()
    SQselected   = ()
    playerClicks = []
    moveMade = False
    stSQ =0
    edSQ =0

    bpx = 51
    bpy = 11

    # socket.gethostbyname(socket.gethostname())
    
    BYTES  = 1024
    HOST   = socket.gethostbyname(socket.gethostname())
    PORT   = 1111
    ADDR   = (HOST,PORT)
    CLOSE  = 'quit'

    s = socket.socket()
    s.bind(ADDR)
    s.listen()
    conn, addr = s.accept()



    while screen == 7:
        p,m = pygame.mouse.get_pos()
        window.fill(Black)
        clock.tick(fps)

        
        if moveMade == True:
            validMoves = []
            validMoves = gameboard.getValidMoves()
            moveMade = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen = 9
                conn.send(CLOSE.encode())
                conn.close()


            if gameboard.wMove == False:
                rmsg = conn.recv(BYTES)
                rmsg = str(rmsg.decode())

                if rmsg == CLOSE:
                    conn.close()
                    screen = 3

                else:
                    
                    pc = inter(rmsg)
                        
                    move = Move(pc[0],pc[1], gameboard.board)
                    gameboard.makeMove(move)
                    moveMade = True
                
                
            elif gameboard.wMove == True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if (0<p<41) and (0<m<41):
                            screen = 3
                            conn.send((CLOSE).encode())
                        
                        if (bpx<p<497+bpx) and (bpy<m<497+bpy):
                            row = selected_row(p,m,bpx,bpy)
                            col = selected_col(p,m,bpx,bpy)

                            if SQselected == (row,col):
                                SQselected   = ()
                                playerClicks = []

                            else:
                                SQselected = (row,col)
                                playerClicks.append(SQselected)


                            if len(playerClicks) == 2:
                                move = Move(playerClicks[0], playerClicks[1], gameboard.board)

                                for i in range(len(validMoves)):
                                    if move.uqID == validMoves[i].uqID:
                                        lig = str(playerClicks)
                                        conn.send(lig.encode())
                                        gameboard.makeMove(validMoves[i])
                                        moveMade = True
                                        SQselected   = ()
                                        playerClicks = []


                                if not moveMade:
                                    playerClicks = [SQselected]

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        gameboard.undoMove()
                        moveMade = True



        pygame.draw.line(window, White, (7,20), (20,4), 5)
        pygame.draw.line(window, White, (7,20), (20,36), 5)
        pygame.draw.line(window, White, (7,20), (35,20), 5)
        pygame.draw.rect(window, White, (0,0,41,41), 4)



        draw_board(window, chessboard, validMoves, gameboard, SQselected,bpx,bpy)
        pygame.display.update()

            


def join():
    global screen, chessboard

    gameboard  = GameBoard()
    validMoves = gameboard.getValidMoves()
    gameboard.wMove = False
    SQselected   = ()
    playerClicks = []
    moveMade = False
    stSQ =0
    edSQ =0

    bpx = 51
    bpy = 11
    
    ONLINE = True
    BYTES  = 1024
    HOST   = socket.gethostbyname(socket.gethostname())
    PORT   = 1111
    ADDR   = (HOST,PORT)
    CLOSE  = 'quit'

    s = socket.socket()
    s.connect(ADDR)


    
    while screen == 8:
        
        p,m = pygame.mouse.get_pos()
        window.fill(Black)
        clock.tick(fps)

        draw_board(window, chessboard, validMoves, gameboard, SQselected,bpx,bpy)

        
        if moveMade == True:
            validMoves = []
            validMoves = gameboard.getValidMoves()
            moveMade = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen = 9
                s.send((CLOSE).encode())
                ONLINE = False


            if gameboard.wMove == False:
                rmsg = s.recv(BYTES)
                rmsg = str(rmsg.decode())


                if rmsg == CLOSE:
                    screen = 3
                else:
                    pc = inter(rmsg)
                        
                    move = Move(pc[0],pc[1], gameboard.board)
                    gameboard.makeMove(move)
                    moveMade = True
                
                
            elif gameboard.wMove == True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if (0<p<41) and (0<m<41):
                            screen = 3
                        
                        if (bpx<p<497+bpx) and (bpy<m<497+bpy):
                            row = selected_row(p,m,bpx,bpy)
                            col = selected_col(p,m,bpx,bpy)

                            if SQselected == (row,col):
                                SQselected   = ()
                                playerClicks = []

                            else:
                                SQselected = (row,col)
                                playerClicks.append(SQselected)


                            if len(playerClicks) == 2:
                                move = Move(playerClicks[0], playerClicks[1], gameboard.board)

                                for i in range(len(validMoves)):
                                    if move.uqID == validMoves[i].uqID:

                                        msg = str(playerClicks)
                                        s.send((msg.encode()))

                                        if msg == CLOSE:
                                            screen = 3

                                    
                                        gameboard.makeMove(validMoves[i])
                                        moveMade = True
                                        SQselected   = ()
                                        playerClicks = []


                                if not moveMade:
                                    playerClicks = [SQselected]

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        gameboard.undoMove()
                        moveMade = True



        pygame.draw.line(window, White, (7,20), (20,4), 5)
        pygame.draw.line(window, White, (7,20), (20,36), 5)
        pygame.draw.line(window, White, (7,20), (35,20), 5)
        pygame.draw.rect(window, White, (0,0,41,41), 4)



        draw_board(window, chessboard, validMoves, gameboard, SQselected,bpx,bpy)
        pygame.display.update()

    

while True:

    if screen == 0:
        menu()
    elif screen == 1:
        login()
    elif screen == 2:
        register()
    elif screen == 3:
        game_menu()
    elif screen == 4:
        settings()
    elif screen == 5:
        PVP()
    elif screen == 6:
        PVC()
    elif screen == 7:
        host()
    elif screen == 8:
        join()
        
    else:
        pygame.quit()
