import pygame, random, sys
from pygame.locals import *


pygame.init()

#------------------------------------------------------------------------------------------------------------------------------------
# DICTIONARY-------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------

BLACK = (0, 0, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
BOXWIDTH = 20
BOXHEIGHT = 20
MARGIN = 5


#------------------------------------------------------------------------------------------------------------------------------------
# CUSTOM VARIABLES-------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------
BOARDWIDTH = 999
BOARDHEIGHT = 999
global numMines
numMines = 100


#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------


gameStart = False
gameDone = False


numFlags = numMines


grid = []
for row in range(BOARDHEIGHT):
    grid.append([])
    for column in range(BOARDWIDTH):
        grid[row].append(0)


def resetGrid():
    global grid
    global checkedGrid
    global flagList
    global mineList
    checkedGrid = []
    for row in range(BOARDHEIGHT):
        checkedGrid.append([])
        for column in range(BOARDWIDTH):
            checkedGrid[row].append(0)
    grid = []
    for row in range(BOARDHEIGHT):
        grid.append([])
        for column in range(BOARDWIDTH):
            grid[row].append(0)
    flagList = []
    for row in range(BOARDHEIGHT):
        flagList.append([])
        for column in range(BOARDWIDTH):
            flagList[row].append(0)
    mineList = grid

checkedGrid = []
for row in range(BOARDHEIGHT):
    checkedGrid.append([])
    for column in range(BOARDWIDTH):
        checkedGrid[row].append(0)

mineList = grid

font1 = pygame.font.SysFont("arial", 24)
img0 = font1.render("", False, "blue")
img1 = font1.render("1", True, "blue")
img2 = font1.render("2", True, "green")
img3 = font1.render("3", True, "red")
img4 = font1.render("4", True, "magenta")
img5 = font1.render("5", True, "orange")
img6 = font1.render("6", True, "yellow")
img7 = font1.render("7", True, "pink")
img8 = font1.render("8", True, "cyan")
imgF = font1.render("F", True, "black")


#------------------------------------------------------------------------------------------------------------------------------------
# Checking for mines-----------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------

def checkRightCenter(row, column):
    if column < BOARDWIDTH - 1 and column != BOARDWIDTH and row != BOARDHEIGHT and row != -1 and column != -1:
        if grid[row][column + 1] == -10:
            if grid[row][column] != -10:
                grid[row][column] += 1


def checkRightTop(row, column):
    if column < BOARDWIDTH - 1 and row > 0 and column != BOARDWIDTH and row != BOARDHEIGHT and row != -1 and column != -1:
        if grid[row - 1][column + 1] == -10:
            if grid[row][column] != -10:
                grid[row][column] += 1


def checkRightBottom(row, column):
    if column < BOARDWIDTH - 1 and row < BOARDHEIGHT - 1 and column != BOARDWIDTH and row != BOARDHEIGHT and row != -1 and column != -1:
        if grid[row + 1][column + 1] == -10:
            if grid[row][column] != -10:
                grid[row][column] += 1


def checkTop(row, column):
    if row > 0 and column != BOARDWIDTH and row != BOARDHEIGHT and row != -1 and column != -1:
        if grid[row - 1][column] == -10:
            if grid[row][column] != -10:
                grid[row][column] += 1


def checkBottom(row, column):
    if row < BOARDHEIGHT - 1 and column != BOARDWIDTH and row != BOARDHEIGHT and row != -1 and column != -1:
        if grid[row + 1][column] == -10:
            if grid[row][column] != -10:
                grid[row][column] += 1


def checkLeftCenter(row, column):
    if column > 0 and column != BOARDWIDTH and row != BOARDHEIGHT and row != -1 and column != -1:
        if grid[row][column - 1] == -10:
            if grid[row][column] != -10:
                grid[row][column] += 1


def checkLeftTop(row, column):
    if column > 0 and row > 0 and column != BOARDWIDTH and row != BOARDHEIGHT and row != -1 and column != -1:
        if grid[row - 1][column - 1] == -10:
            if grid[row][column] != -10:
                grid[row][column] += 1


def checkLeftBottom(row, column):
    if column > 0 and row < BOARDHEIGHT - 1 and column != BOARDWIDTH and row != BOARDHEIGHT and row != -1 and column != -1:
        if grid[row + 1][column - 1] == -10:
            if grid[row][column] != -10:
                grid[row][column] += 1

# this function is used to check all the tiles touching the selected tile
def checkTile(row, column):
    if column != BOARDWIDTH and row != BOARDHEIGHT and row != -1 and column != -1 and checkedGrid[row][column] == 0:
        checkRightCenter(row, column)
        checkRightTop(row, column)
        checkRightBottom(row, column)
        checkTop(row, column)
        checkBottom(row, column)
        checkLeftCenter(row, column)
        checkLeftTop(row, column)
        checkLeftBottom(row, column)
        if grid[row][column] == 0:
            grid[row][column] = -1
            return "blank"
        checkedGrid[row][column] = 1


# this function is used to check the area around the tiles touching the selected tile
def checkArea(row, column):
    if checkTile(row, column) == "blank":
        checkArea(row + 1, column + 1)
        checkArea(row - 1, column - 1)
        checkArea(row + 1, column - 1)
        checkArea(row - 1, column + 1)
        checkArea(row, column + 1)
        checkArea(row, column - 1)
        checkArea(row + 1, column)
        checkArea(row - 1, column)

# if player enters too many mines they will be forced to enter a valid amount 
def TooManyMines():
    global numMines
    if numMines >= BOARDHEIGHT * BOARDWIDTH:
        print("Woah, that's too many mines!")
        numMines = int(input("how many mines do you want? It's reccommended to have around 20 percent of the area be mines, in your case it would be " + (str(((BOARDHEIGHT * BOARDWIDTH) * 0.2))) + ": "))
        print("\n")
        TooManyMines()
    elif numMines <= 0:
        print("you should have at least 1 mine to play the game ")
        numMines = int(input("how many mines do you want? It's reccommended to have around 20 percent of the area be mines, in your case it would be " + (str(((BOARDHEIGHT * BOARDWIDTH) * 0.2))) + ": "))
        print("\n")
        TooManyMines()
    else:
        return 

def notNumberWIDTH():
    global BOARDWIDTH
    if BOARDWIDTH.isdigit():
        BOARDWIDTH = int(BOARDWIDTH)
        if BOARDWIDTH <= 3:
            print("Come on, choose more than that. ")
            BOARDWIDTH = input("what do you want the width of the board to be? ")
            print("\n")
            notNumberWIDTH()
        if BOARDWIDTH >= 45:
            print("Woah, that grid is a bit too big!")
            BOARDWIDTH = input("what do you want the width of the board to be? ")
            print("\n")
            notNumberWIDTH()
    else:
        print("Please input a valid number.")
        BOARDWIDTH = input("what do you want the width of the board to be? ")
        print("\n")
        notNumberWIDTH()

def notNumberHEIGHT():
    global BOARDHEIGHT
    if BOARDHEIGHT.isdigit():
        BOARDHEIGHT = int(BOARDHEIGHT)
        if BOARDHEIGHT <= 3:
            print("Come on, choose more than that. ")
            BOARDHEIGHT = input("what do you want the height of the board to be? ")
            print("\n")
            notNumberHEIGHT()
        if BOARDHEIGHT >= 45:
            print("Woah, that grid is a bit too big!")
            BOARDHEIGHT = input("what do you want the height of the board to be? ")
            print("\n")
            notNumberHEIGHT()
    else:
        print("Please input a valid number.")
        BOARDHEIGHT = input("what do you want the height of the board to be? ")
        print("\n")
        notNumberHEIGHT()

def notNumberMINES():
    global numMines
    if numMines.isdigit():
        numMines = int(numMines)
    else:
        print("Please input a valid number.")
        numMines = input("how many mines do you want? It's reccommended to have less than around 20 percent of the area be mines, in your case it would be " + (str(((BOARDHEIGHT * BOARDWIDTH) * 0.2))) + ": ")
        print("\n")
        notNumberMINES()
    

# this will be changed depending on the size of the grid chosen by the player
WINDOW_SIZE = None
screen = None

# player inputs grid size and amount of mines
if gameStart == False:
    print("\n")
    BOARDWIDTH = input("what do you want the width of the board to be? ")
    notNumberWIDTH()
    print("\n")
    BOARDHEIGHT = input("what do you want the height of the board to be? ")
    notNumberHEIGHT()
    print("\n")
    numMines = input("how many mines do you want? It's reccommended to have less than around 20 percent of the area be mines, in your case it would be " + (str(((BOARDHEIGHT * BOARDWIDTH) * 0.2))) + ": ")
    notNumberMINES()
    print("\n")
    TooManyMines()
    numFlags = numMines
    WINDOW_SIZE = [BOXWIDTH * BOARDWIDTH + BOARDWIDTH * MARGIN + 5, BOXHEIGHT * BOARDHEIGHT + BOARDHEIGHT * MARGIN + 5]
    screen = pygame.display.set_mode(WINDOW_SIZE)

 
pygame.display.set_caption("Minesweeper")
done = False
clock = pygame.time.Clock()


flagList = []
for row in range(BOARDHEIGHT):
    flagList.append([])
    for column in range(BOARDWIDTH):
        flagList[row].append(0)


image = img0


correctFlags = 0
w = False


num1 = 0
num2 = 0


minesGenerated = False

# create mines 
def generateMines():
    resetGrid()
    numMine = 0
    for x in range(numMines):
        num1 = random.randrange(0, BOARDHEIGHT)
        num2 = random.randrange(0, BOARDWIDTH)
        while grid[num1][num2] == -10:
            num1 = random.randrange(0, BOARDHEIGHT)
            num2 = random.randrange(0, BOARDWIDTH)
        grid[num1][num2] = -10
        numMine = numMine + 1

#------------------------------------------------------------------------------------------------------------------------------------
# GAME LOOP--------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (BOXWIDTH + MARGIN)
            if column == BOARDWIDTH:
                column -= 1
            row = pos[1] // (BOXHEIGHT + MARGIN)
            if row == BOARDHEIGHT:
                row -= 1
            if minesGenerated == False:
                generateMines()
                checkArea(row, column)
                while grid[row][column] != -1:
                    resetGrid()
                    generateMines()
                    checkArea(row, column)
                minesGenerated = True
                gameStart = True
            if grid[row][column] == -10 and gameDone == False and gameStart == True and flagList[row][column] != -10:
                print("\n BOOM! You lose! Press the space bar to play again \n")
                gameDone = True
            if grid[row][column] != -1 and gameDone == False and gameStart == True:
                checkArea(row, column)
        elif event.type == pygame.KEYDOWN:
            if event.key == K_f and gameDone == False and gameStart == True:
                correctFlags = 0
                pos = pygame.mouse.get_pos()
                column = pos[0] // (BOXWIDTH + MARGIN)
                row = pos[1] // (BOXHEIGHT + MARGIN)
                if flagList[row][column] == 0 and numFlags >= 1:
                    if grid[row][column] == 0 or grid[row][column] == -10:
                        flagList[row][column] = -10
                        numFlags -= 1
                        print("\n you have " + str(numFlags) + " flags left \n")
                elif flagList[row][column] == -10:
                    flagList[row][column] = 0
                    numFlags += 1
                    print("\n you have " + str(numFlags) + " flags left \n")
                elif numFlags <= 1:
                    print("\n out of flags! \n")
                for row in range(len(mineList)):
                    for column in range(len(mineList[row])):
                        if flagList[row][column] == -10 and flagList[row][column] == mineList[row][column]:
                            correctFlags += 1
                if correctFlags == numMines:
                    print('\n Congratulations! You win! Press the space bar to play again \n')
                    gameDone = True
            if event.key == K_SPACE and gameDone == True and gameStart == True:
                resetGrid()
                minesGenerated = False
                gameStart = True
                gameDone = False
                BOARDWIDTH = 999
                BOARDHEIGHT = 999
                numMines = 999
                print("\n")
                BOARDWIDTH = input("what do you want the width of the board to be? ")
                notNumberWIDTH()
                print("\n")
                BOARDHEIGHT = input("what do you want the height of the board to be? ")
                notNumberHEIGHT()
                print("\n")
                numMines = input("how many mines do you want? It's reccommended to have less than around 20 percent of the area be mines, in your case it would be " + (str(((BOARDHEIGHT * BOARDWIDTH) * 0.2))) + ": ")
                notNumberMINES()
                print("\n")
                TooManyMines()
                numFlags = numMines
                WINDOW_SIZE = [BOXWIDTH * BOARDWIDTH + BOARDWIDTH * MARGIN + 5, BOXHEIGHT * BOARDHEIGHT + BOARDHEIGHT * MARGIN + 5]
                screen = pygame.display.set_mode(WINDOW_SIZE)


    screen.fill(BLACK)
   
    if gameDone == True:
        for row in range(BOARDHEIGHT):
            for column in range(BOARDWIDTH):
                if grid[row][column] == -10:
                    grid[row][column] = -11


    for row in range(BOARDHEIGHT):
        for column in range(BOARDWIDTH):
            color = WHITE
            image = img0
            if grid[row][column] == -1:
                color = GREY
            if grid[row][column] == -11:
                color = "red"
            if grid[row][column] == 1:
                image = img1
                color = GREY
            if grid[row][column] == 2:
                image = img2
                color = GREY
            if grid[row][column] == 3:
                image = img3
                color = GREY
            if grid[row][column] == 4:
                image = img4
                color = GREY
            if grid[row][column] == 5:
                image = img5
                color = GREY
            if grid[row][column] == 6:
                image = img6
                color = GREY
            if grid[row][column] == 7:
                image = img7
                color = GREY
            if grid[row][column] == 8:
                image = img8
                color = GREY
            if flagList[row][column] == -10:
                image = imgF
           


            pygame.draw.rect(screen, color,
                             [(MARGIN + BOXWIDTH) * column + MARGIN,
                              (MARGIN + BOXHEIGHT) * row + MARGIN,
                              BOXWIDTH,
                              BOXHEIGHT])


            rectangle = image.get_rect(center = ((MARGIN + BOXWIDTH) * column + MARGIN + 10, (MARGIN + BOXHEIGHT) * row + MARGIN + 10))
            screen.blit(image, rectangle)


 
    clock.tick(60)
 
    pygame.display.flip()
 
pygame.quit()
