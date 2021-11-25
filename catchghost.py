import pygame, sys #기본세팅
import random, time, threading #내가 추가한 것
from pygame.locals import *

#Set up pygame.
pygame.init()
mainClock = pygame.time.Clock()



    
    
    


#상수 정의
SCREEN =8

BLACK = (0,0,0)
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLUE = (0,0,255)
RED = (255,0,0)
YELLOW = (255,204,51)
GRAY = (125,125,125)

NUM1 = 49
NUM2 = 50
NUM3 = 51
NUM4 = 52
NUM5 = 53
NUM6 = 54

#변수 정의

#아이템 창 itemPos = [x좌표, y좌표, 해당 아이템 번호를 눌렀는지]
itemPos =[]
for i in range(6):
    itemPos.append([200+35*i,455, False])

#유령이 지나다니는 길
areaGhostAppearPos =[[],[],[]]
moveGhostPos =[[80,75],[80,185],[80,295]]
for row in range(3):
    for col in range(3):
        areaGhostAppearPos[row].append([140+col * 110,50+row *110])



screen = pygame.display.set_mode((600,500), 0,32)
pygame.display.set_caption("Catch a Ghost")

#화면 세팅
screen.fill(WHITE)


#UI 세팅
def setLifeUI():
    for i in range(3):
        pygame.draw.circle(screen, RED, [30+35*i,470],15)

def setItemUI():
    for i in range(6):
        pygame.draw.rect(screen, BLACK, [itemPos[i][0],itemPos[i][1],30,30],2)
        if itemPos[i][2] == True:
            pygame.draw.rect(screen, GRAY, [itemPos[i][0]-3,itemPos[i][1]-3,36,36],2)
    

def setScore():
    font = pygame.font.SysFont("arial",25,True)
    scoreText = font.render("Score", True, BLACK)
    screen.blit(scoreText, [520,420])

    socreContentText = font.render("100", True, BLACK)
    screen.blit(socreContentText, [530,450])


def setTimeUI():
    pygame.draw.circle(screen, BLUE, [550, 50], 30,2)
    font = pygame.font.SysFont("arial",35,True)
    timeText = font.render("60", True, BLACK)
    timeTextCircleObj = timeText.get_rect()
    timeTextCircleObj.centerx = 550
    timeTextCircleObj.centery = 50  
    screen.blit(timeText, timeTextCircleObj)

def setAreaGhostAppear():
    for row in range(3):
        for col in range(3):
            pygame.draw.rect(screen, BLACK, [140+col * 110,50+row *110 ,100,100],2)


def checkSelectedItem(itemPosNum): #번호를 눌렀을때 해당 아이템 창으로 이동할 수 있도록 확인,  화면에 띄우는 것은 setItemUI()
    for i in range(6):
        if i == itemPosNum-1:
            itemPos[i][2] = True
        else:
            itemPos[i][2] = False
            

def changeEventKeyToNum(eventKey):
    if eventKey == NUM1:
        return 1
    elif eventKey == NUM2:
        return 2
    elif eventKey == NUM3:
        return 3
    elif eventKey == NUM4:
        return 4
    elif eventKey == NUM5:
        return 5
    elif eventKey == NUM6:
        return 6


def checkInput(eventKey):
    if event.key >= NUM1 and event.key <= NUM6:
        num = changeEventKeyToNum(eventKey)
        checkSelectedItem(num)
        print(num)


    
def checkDistance(xPos):
    if xPos == 250: # 2초
        return True
    elif xPos == 360:
        return True
    elif xPos == 470:
        return 0
    



imageScale =0
checkMovedArea = [[True,False,False,False],[True,False,False,False],[True,False,False,False]] # 1구간 중간, 2구간 중간, 3구간 중간, 구간 끝
moveInterval =[1,1,1]
restartGhost = False
def returnRandomGhostMoveSpeed(): #스피드 종류 : 1, 2, 3
    return random.randrange(1,4)
    

def changeMoveBool(row,col):
    global restartGhost
    checkMovedArea[row][col] = True
    if col == 3:
        print("!!!!!!!!!!!!!!!")
        restartGhost =True

def moveGhost():
    global checkMovedArea
    global imageScale
    global restartGhost
    imageGhost = pygame.image.load("ghost.png")
    stoppedGhostImg = pygame.image.load("stoppedGhost.png")
    imageGhost = pygame.transform.scale(imageGhost,(50,50))
    stoppedGhostImg = pygame.transform.scale(stoppedGhostImg,(50,50))

    
    for i in range(3):
        if moveGhostPos[i][0] >= 165 and checkMovedArea[i][0] == True:
            print("1구간 중간")
            checkMovedArea[i][0] = False       
            #2초뒤 움직이게 만들기
            threading.Timer(1, changeMoveBool, args=[i,1]).start()
            restartGhost = False

        elif moveGhostPos[i][0] >= 275 and checkMovedArea[i][1] == True:
            print("2구간 중간")
            checkMovedArea[i][1] = False     
            threading.Timer(1, changeMoveBool, args=[i,2]).start()
            
        elif moveGhostPos[i][0] >= 385 and checkMovedArea[i][2] == True:
            print("3구간 중간")
            checkMovedArea[i][2] = False          
            threading.Timer(1, changeMoveBool, args=[i,3]).start()
                  
        elif moveGhostPos[i][0] >= 480 and checkMovedArea[i][3] == True:
            print("구간 끝")
            checkMovedArea[i][3] = False
            
            threading.Timer(1.5, changeMoveBool, args=[i,0]).start()
            moveGhostPos[i][0] = 80 #유령이 나오는 지점
  



    for i in range(4):
            if restartGhost == True:           
                screen.blit(imageGhost,[moveGhostPos[0][0],moveGhostPos[0][1]],Rect(0,0,50,50))
                screen.blit(imageGhost,[moveGhostPos[1][0],moveGhostPos[1][1]],Rect(0,0,50,50))
                screen.blit(imageGhost,[moveGhostPos[2][0],moveGhostPos[2][1]],Rect(0,0,50,50))
                break
            if checkMovedArea[0][i] == True: #Ghost가 움직일 경우
                screen.blit(imageGhost,[moveGhostPos[0][0],moveGhostPos[0][1]],Rect(0,0,50,50))
                screen.blit(imageGhost,[moveGhostPos[1][0],moveGhostPos[1][1]],Rect(0,0,50,50))
                screen.blit(imageGhost,[moveGhostPos[2][0],moveGhostPos[2][1]],Rect(0,0,50,50))
                break
            else:
                if i==2: #  checkMovedArea[0][i]가 전부 False일 경우, 즉 중간에 멈췄을때  
                    screen.blit(stoppedGhostImg,[moveGhostPos[0][0],moveGhostPos[0][1]],Rect(0,0,50,50))
                    screen.blit(stoppedGhostImg,[moveGhostPos[1][0],moveGhostPos[1][1]],Rect(0,0,50,50))
                    screen.blit(stoppedGhostImg,[moveGhostPos[2][0],moveGhostPos[2][1]],Rect(0,0,50,50))
                    
                    break



    for col in range(4):
        if checkMovedArea[0][col] == True:
            if col ==3:
                moveInterval[0] =returnRandomGhostMoveSpeed()

            moveGhostPos[0][0] = moveGhostPos[0][0]+moveInterval[0]
            
        if checkMovedArea[1][col] == True:
            if col ==3:
                moveInterval[1] =returnRandomGhostMoveSpeed()
            moveGhostPos[1][0] = moveGhostPos[1][0]+moveInterval[1]
            
        if checkMovedArea[2][col] == True:
            if col ==3:
                moveInterval[2] =returnRandomGhostMoveSpeed()
            moveGhostPos[2][0] = moveGhostPos[2][0]+moveInterval[2]
         
 



setLifeUI()
setItemUI()
setScore()
setAreaGhostAppear()
setTimeUI()
moveGhost()











#Game Loop
while True:
    screen.fill(WHITE)
        
    setLifeUI()
    setItemUI()
    setScore()
    setAreaGhostAppear()
    setTimeUI()
    moveGhost()

    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            #print(event.key)
            
            checkInput(event.key)
       
    


    mainClock.tick(100)
    pygame.display.update()
















