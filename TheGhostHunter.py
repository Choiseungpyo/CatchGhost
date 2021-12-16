import pygame, sys #기본세팅
import math ,random, time, threading #내가 추가한 것
from pygame.locals import *

#Set up pygame.
pygame.init()
mainClock = pygame.time.Clock()

#Sound
pygame.mixer.music.load("sound/bgm.mp3")
pygame.mixer.music.set_volume(0.5)

shootSound = pygame.mixer.Sound("sound/shoot.ogg")
shootSound.set_volume(0.2)

buySound = pygame.mixer.Sound("sound/buy.ogg")
buySound.set_volume(0.3)

hitSound = pygame.mixer.Sound("sound/hit.ogg")
hitSound.set_volume(0.7)

pygame.mixer.music.play(-1) #bgm 무한반복

#상수 정의
SCREENHEIGHT = 500
SCREENWIDTH = 600

BLACK = (0,0,0)
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLUE = (0,0,255)
RED = (255,0,0)
YELLOW = (255,204,51)
GRAY = (125,125,125)
BRIGHT_GRAY = (200,200,200)

NUM1 = 49
NUM2 = 50
NUM3 = 51
NUM4 = 52
NUM5 = 53
NUM6 = 54
C = 99

#변수
 #Scene
isMainScene = False
isStartScene = True 
isEndScene = False
isTutorialScene = False

 #엔딩 씬에서 다음씬으로 넘어갈 수 있는지 확인(리셋하는 시간동안 기다려야하기 때문)
CanMoveEndSceneToNextScene = False

 #플레이어의 Hp
playerHp = 3
printEmptyHpCnt = 0

 #아이템 창 itemPos = [x좌표, y좌표, 해당 아이템 번호를 눌렀는지]
itemPos =[]
for i in range(6):
    itemPos.append([150+55*i,440, False])
itemPos[0][2] = True
item = ["WhiteBullet", "None", "None", "None", "None", "None"] 

 #유령 속성
ghost1 = {'num': 0, 'pos': pygame.Rect(-50,75,75,75), 'dir':"RIGHT", 'moveSpeed': 3, 'color': "White"} 
ghost2 = {'num': 1, 'pos': pygame.Rect(SCREENWIDTH,185,75,75), 'dir':"LEFT", 'moveSpeed': 3, 'color': "White"}
ghost3 = {'num': 2, 'pos': pygame.Rect(-50,295,75,75), 'dir':"RIGHT", 'moveSpeed': 3, 'color': "White"}
ghost4 = {'num': 3, 'pos': pygame.Rect(SCREENWIDTH/2,SCREENHEIGHT +100, 75, 45), 'color': "Purple", 'currentItemBoxIndex': "None"}
ghosts = [ghost1,ghost2,ghost3, ghost4]

 #ghost4
isSettingGhost4 = True
alreadyWorking = False #스레드에서 시간 차이로 인한 오류가 생기므로 해당 함수가 끝난 후 동작할 수 있도록 함.
ghost4StartTime = 0
ghost4EndTime = 0
copyGhost4RandTime = 0

 #cheating Ghost
cheatingGhostManagement = False
isDeadCheatingGhost = False

 #유령을 죽였을 시 얻는 가격
ghostPrice = 100
killedGhostCnt = 0
killGhost4Bool = False

 #상점
coin = 0
clickShop = False
shopPos = pygame.Rect(550,450,40,40)
isAvailableTimeForShop = True #상점은 들어갔다 나온 후 5초이후부터 이용가능하다. 

 #제한시간
timeLimit = 60
printTime0 = False
isChangingTime = True #시간

 #아이템 사용
useItemDoubleCoin = False #DoubleCoin 아이템을 사용 지속여부 
useItemReduceGhostSpeed = False #ReduceGhostSpeed 아이템을 사용 지속여부

 #게임오버
isGameOver = False

 #아이템창에 아이템이 있는지를 확인하는 변수
haveItem = True

 #hit effect
hitEffectTimeOver = True

 #튜토리얼 관련
currentPage = 1 #현재 페이지


#이미지
 #배경
imageBG = pygame.image.load("images/background.jpg")
imageBG = pygame.transform.scale(imageBG,(SCREENWIDTH,SCREENHEIGHT))

 #유령
imageWhiteGhostL = pygame.image.load("images/left_WhiteGhost.png")
imageWhiteGhostL = pygame.transform.scale(imageWhiteGhostL,(75,75))
imageWhiteGhostR = pygame.image.load("images/right_WhiteGhost.png")
imageWhiteGhostR = pygame.transform.scale(imageWhiteGhostR,(75,75))

imageRedGhostL = pygame.image.load("images/left_RedGhost.png")
imageRedGhostL = pygame.transform.scale(imageRedGhostL,(75,75))
imageRedGhostR = pygame.image.load("images/right_RedGhost.png")
imageRedGhostR = pygame.transform.scale(imageRedGhostR,(75,75))

imageBlueGhostL = pygame.image.load("images/left_BlueGhost.png")
imageBlueGhostL = pygame.transform.scale(imageBlueGhostL,(75,75))
imageBlueGhostR = pygame.image.load("images/right_BlueGhost.png")
imageBlueGhostR = pygame.transform.scale(imageBlueGhostR,(75,75))

imagePurpleGhost = pygame.image.load("images/purpleGhost.png")
imagePurpleGhost = pygame.transform.scale(imagePurpleGhost,(75,75))

imageCheatingGhost = pygame.image.load("images/cheatingGhost.png")
imageCheatingGhost = pygame.transform.scale(imageCheatingGhost,(150,150))

 #총구
imageGunPoint = pygame.image.load("images/gunPoint.png")
imageGunPoint = pygame.transform.scale(imageGunPoint,(75,75))

 #총알
imageWhiteBullet = pygame.image.load("images/whiteBullet.png")
imageWhiteBullet = pygame.transform.scale(imageWhiteBullet,(50,50))

imageRedBullet = pygame.image.load("images/redBullet.png")
imageRedBullet = pygame.transform.scale(imageRedBullet,(50,50))

imageBlueBullet = pygame.image.load("images/blueBullet.png")
imageBlueBullet = pygame.transform.scale(imageBlueBullet,(50,50))

imagePurpleBullet = pygame.image.load("images/purpleBullet.png")
imagePurpleBullet = pygame.transform.scale(imagePurpleBullet,(50,50))

 #플레이어 Hp
imagePlayerFullHp = pygame.image.load("images/playerFullHp.png")
imagePlayerFullHp = pygame.transform.scale(imagePlayerFullHp,(35,35))

imagePlayerEmptyHp = pygame.image.load("images/playerEmptyHp.png")
imagePlayerEmptyHp = pygame.transform.scale(imagePlayerEmptyHp,(35,35))

 #상점
imageShopIcon = pygame.image.load("images/shopIcon.png")
imageShopIcon = pygame.transform.scale(imageShopIcon,(shopPos.width,shopPos.height))
   
imageShopBG = pygame.image.load("images/shopBG.png")
imageShopBG = pygame.transform.scale(imageShopBG,(500, 400))

imageShopWhiteBullet = pygame.image.load("images/shopWhiteBullet.png")
imageShopWhiteBullet = pygame.transform.scale(imageShopWhiteBullet,(100,130))

imageShopRedBullet = pygame.image.load("images/shopRedBullet.png")
imageShopRedBullet = pygame.transform.scale(imageShopRedBullet,(100,130))

imageShopBlueBullet = pygame.image.load("images/shopBlueBullet.png")
imageShopBlueBullet = pygame.transform.scale(imageShopBlueBullet,(100,130))

imageShopPurpleBullet = pygame.image.load("images/shopPurpleBullet.png")
imageShopPurpleBullet = pygame.transform.scale(imageShopPurpleBullet,(100,130))

imageShopIncreaseTime = pygame.image.load("images/shopIncreaseTime.png")
imageShopIncreaseTime = pygame.transform.scale(imageShopIncreaseTime,(105,130))

imageShopReduceGhostSpeed = pygame.image.load("images/shopReduceGhostSpeed.png")
imageShopReduceGhostSpeed = pygame.transform.scale(imageShopReduceGhostSpeed,(110,130))

imageShopHealPack = pygame.image.load("images/shopHealPack.png")
imageShopHealPack = pygame.transform.scale(imageShopHealPack,(100,132))

imageShopDoubleCoin = pygame.image.load("images/shopDoubleCoin.png")
imageShopDoubleCoin = pygame.transform.scale(imageShopDoubleCoin,(100,130))

imageCoin = pygame.image.load("images/coin.png")
imageCoin = pygame.transform.scale(imageCoin,(25,25))

 #아이템 칸에 사용하는 아이템 이미지
imageIncreaseTime = pygame.image.load("images/increaseTime.png")
imageIncreaseTime = pygame.transform.scale(imageIncreaseTime,(50,40))

imageHealPack = pygame.image.load("images/healPack.png")
imageHealPack = pygame.transform.scale(imageHealPack,(40,40))

imageReduceGhostSpeed = pygame.image.load("images/reduceGhostSpeed.png")
imageReduceGhostSpeed = pygame.transform.scale(imageReduceGhostSpeed,(40,40))

imageDoubleCoin = pygame.image.load("images/doubleCoin.png")
imageDoubleCoin = pygame.transform.scale(imageDoubleCoin,(35,35))

 #사용중인 아이템 지속 여부
imageDoubleCoinEffect = pygame.image.load("images/doubleCoin.png")
imageDoubleCoinEffect = pygame.transform.scale(imageDoubleCoinEffect,(25,25))

imageReduceGhostSpeedEffect = pygame.image.load("images/reduceGhostSpeed.png")
imageReduceGhostSpeedEffect = pygame.transform.scale(imageReduceGhostSpeedEffect,(25,25))

 #유령이 플레이어 타격 효과
imageHitEffect = pygame.image.load("images/hitEffect.png")
imageHitEffect = pygame.transform.scale(imageHitEffect,(SCREENWIDTH,SCREENHEIGHT))

 #Game Over일 경우 띄우는 창
imageGameOver = pygame.image.load("images/gameOver.png")
imageGameOver = pygame.transform.scale(imageGameOver,(SCREENWIDTH,SCREENHEIGHT))

 #Replay
imageReplay = pygame.image.load("images/replay.png")
imageReplay = pygame.transform.scale(imageReplay,(75,75))

 #GoTitle
imageGoTitle = pygame.image.load("images/goTitle.png")
imageGoTitle = pygame.transform.scale(imageGoTitle,(75,75))

 #Start BG
imageStartBG = pygame.image.load("images/background.jpg")
imageStartBG = pygame.transform.scale(imageStartBG,(SCREENWIDTH,SCREENHEIGHT))

 #튜토리얼
imageNextPageButton = pygame.image.load("images/nextPageButton.png")
imageNextPageButton = pygame.transform.scale(imageNextPageButton,(25, 30))

imagePreviousPageButton = pygame.image.load("images/previousPageButton.png")
imagePreviousPageButton = pygame.transform.scale(imagePreviousPageButton,(25, 30))

imageGhostAndBullet = pygame.image.load("images/ghostAndBullet.png")
imageGhostAndBullet = pygame.transform.scale(imageGhostAndBullet,(400, 150))

imagePage4Ghost = pygame.image.load("images/page4_ghost.png")
imagePage4Ghost = pygame.transform.scale(imagePage4Ghost,(180, 180))

imagePage5Ghost = pygame.image.load("images/page5_ghost.png")
imagePage5Ghost = pygame.transform.scale(imagePage5Ghost,(150, 150))

imageExitTutorialSceneButton = pygame.image.load("images/exitTutorialSceneButton.png")
imageExitTutorialSceneButton = pygame.transform.scale(imageExitTutorialSceneButton,(30, 30))


#화면
screen = pygame.display.set_mode((600,500), 0,32)
pygame.display.set_caption("The Ghost Hunter")


#-----------------------------------------------------------------------------------------------
#함수
def checkIsNoHp(): #체력이 없는지 확인한다.
    global playerHp, isGameOver 
    
    if playerHp <= 0 and printEmptyHpCnt ==3: 
         isGameOver = True
         

def reduceTimeLimit(): #제한시간을 감소시킨다.
    global timeLimit, isChangingTime, printTime0
    
    if timeLimit ==1:
        printTime0 = True
        
    if clickShop == False: #상점을 눌렀을때는 시간을 감소시키지 않는다.
        timeLimit -=1
        
    isChangingTime = True

def setBackground(): #배경 띄우기
    screen.blit(imageBG,[0,0],Rect(0,0,SCREENWIDTH,SCREENHEIGHT))

    
def setHpUI(): #Hp UI
    global printEmptyHpCnt
    printEmptyHpCnt = 0
    
    for i in range(3):
        if i< playerHp: 
            screen.blit(imagePlayerFullHp, [15+40*i,450]) #채워진 하트 
        else:
            screen.blit(imagePlayerEmptyHp, [15+40*i,450])  #빈 하트
            printEmptyHpCnt +=1
            

def setItemUI(): #Item UI
    for i in range(6):
        pygame.draw.rect(screen, WHITE,[itemPos[i][0],itemPos[i][1],50,50]) #하얀색 바탕
        pygame.draw.rect(screen, GRAY, [itemPos[i][0],itemPos[i][1],50,50],2) #회색 테두리
        
        if item[i] != "None":
            if item[i] == "WhiteBullet":
                screen.blit(imageWhiteBullet, [itemPos[i][0],itemPos[i][1]])
            elif item[i] == "RedBullet":
                screen.blit(imageRedBullet, [itemPos[i][0],itemPos[i][1]])
            elif item[i] == "BlueBullet":
                screen.blit(imageBlueBullet, [itemPos[i][0],itemPos[i][1]])
            elif item[i] == "PurpleBullet":
                screen.blit(imagePurpleBullet, [itemPos[i][0],itemPos[i][1]])
            elif item[i] == "IncreaseTime":
                screen.blit(imageIncreaseTime, [itemPos[i][0]+5,itemPos[i][1]+5])
            elif item[i] == "HealPack":
                screen.blit(imageHealPack, [itemPos[i][0]+5,itemPos[i][1]+5])
            elif item[i] == "ReduceGhostSpeed":
                screen.blit(imageReduceGhostSpeed, [itemPos[i][0]+5,itemPos[i][1]+5])
            elif item[i] == "DoubleCoin":
                screen.blit(imageDoubleCoin, [itemPos[i][0]+7,itemPos[i][1]+7])
                
        if itemPos[i][2] == True: #플레이어가 선택해놓은 아이템 칸 
            pygame.draw.rect(screen, BRIGHT_GRAY, [itemPos[i][0]-2,itemPos[i][1]-2,54,54],3) #선택했을 때 Effect
    

def setTimeUI(): #TIme UI
    global timeLimit, isChangingTime, printTime0, isGameOver 
            
    if isChangingTime == True:
        isChangingTime = False
        threading.Timer(1, reduceTimeLimit).start()
    
    pygame.draw.circle(screen, WHITE, [550, 50], 28)
    pygame.draw.circle(screen, BLUE, [550, 50], 30,2)
    
    font = pygame.font.SysFont("arial",35,True)
    timeText = font.render(str(timeLimit), True, BLACK)
    timeTextCircleObj = timeText.get_rect()
    timeTextCircleObj.centerx = 550
    timeTextCircleObj.centery = 50
    screen.blit(timeText, timeTextCircleObj)
    
    if timeLimit <=0 and printTime0 == True:
        isGameOver = True
        
        
def setShopUI(): #Shop UI
    global clickShop, isAvailableTimeForShop 

    if isAvailableTimeForShop == True:
        screen.blit(imageShopIcon,[shopPos.left, shopPos.top])

        if clickShop == True:
            screen.blit(imageShopBG,[50,50])

            screen.blit(imageCoin,[80,80])
            screen.blit(imageShopWhiteBullet,[80,120])
            screen.blit(imageShopRedBullet,[190,120])
            screen.blit(imageShopIncreaseTime,[306,120])
            screen.blit(imageShopReduceGhostSpeed,[412,120])

            screen.blit(imageShopBlueBullet,[80,275])
            screen.blit(imageShopPurpleBullet,[190,275])
            screen.blit(imageShopHealPack,[310,273])
            screen.blit(imageShopDoubleCoin,[420,275])

            font = pygame.font.SysFont("arial",30,True)
            timeText = font.render(str(coin)+"$", True, WHITE)
            screen.blit(timeText, [110,75])


#------------------------------------------------------------------------------------------
#key
def checkSelectedItem(itemPosNum): #번호를 눌렀을때 해당 아이템 창으로 이동할 수 있도록 확인, 화면에 띄우는 것은 setItemUI()
    for i in range(6):
        if i == itemPosNum-1:
            itemPos[i][2] = True
        else:
            itemPos[i][2] = False
            

def changeEventKeyToNum(eventKey): #1~6 키 입력받기
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

    
def checkInput(eventKey): #입력받은 값 확인
    global clickShop

    if clickShop == False:
        if eventKey >= NUM1 and eventKey <= NUM6:
            num = changeEventKeyToNum(eventKey)
            checkSelectedItem(num)
            


#-----------------------------------------------------------------------------------------------
#Cheating Ghost - 플레이어는 모르지만 제작자만 아는 치트키를 위한 유령(기말 최종 발표때 코드를 바꾸지 않고 편히 설명하기 위함)
def checkConditionCanMakeCheatingGhost(eventKey): #치트 유령을 만들 수 있는 조건인지 확인한다.
    global currentPage, cheatingGhostManagement
    
    if currentPage == 6:
        if eventKey == C:
            cheatingGhostManagement = True
            return 

    cheatingGhostManagement = False


def removeCheatingGhost(): #치트유령 제거하기
    global cheatingGhostManagement, isDeadCheatingGhost

    mousePos = pygame.mouse.get_pos()

    if cheatingGhostManagement == True:
        if mousePos[0] >= 500 and mousePos[0] <= 600:
                if mousePos[1] >= 420 and mousePos[1] <=500:
                    cheatingGhostManagement = False
                    isDeadCheatingGhost = True
                    shootSound.play()

                
#-----------------------------------------------------------------------------------------------
#Ghost4
def calculateGhost4EndTimeMinusGameEndTime(ghost4EndTime): #게임 끝날시 ghost4가 초기화 하는 시간 계산
    global copyGhost4RandTime
 
    ghost4ResetTime = copyGhost4RandTime - ghost4EndTime
    if ghost4ResetTime < 0:
        ghost4ResetTime = 0
    return ghost4ResetTime

    
def changeCanMoveEndSceneToNextSceneToTrue(): #게임 끝날시 ghost4를 초기화 하는 시간만큼 지난 후 게임 시작할 수 있게 한다.
    global CanMoveEndSceneToNextScene
    CanMoveEndSceneToNextScene = True

    
def checkHaveItem(): #아이템창에 아이템을 가지고있는지 확인한다.
    global haveItem

    for i in range(6):
        if item[i] == "None":
            if i==5:
                haveItem = False #아이템을 하나도 가지고 있지 않다고 변경.             
                ghost4['currentItemBoxIndex'] = "None"              
        else:
            haveItem = True
            break


def checkNoItemAndCoin(): #아이템창에 아이템이 하나도 없고, 상점에서 아이템을 살 수 없을 경우 게임 종료.
    global coin, haveItem, isGameOver
    
    if coin < 500 and haveItem == False:
        isGameOver = True

        
def takeAwayItem(): #ghost4가 나타난 자리의 아이템을 가져간다.
    global killGhost4Bool

    if killGhost4Bool == False: #ghost4를 못 죽였을 경우
        if ghost4['currentItemBoxIndex'] != "None":
            item[ghost4['currentItemBoxIndex']] = "None"
            
        
def changeGhost4PosToBottomOfScreen(): #ghost4를 화면 바깥으로 위치시킨다.(ghost4가 사라진 것처럼 보이게)
    global isSettingGhost4, killGhost4Bool, alreadyWorking 
    
    ghost4['pos'][0] = SCREENWIDTH/2
    ghost4['pos'][1] = SCREENHEIGHT +100
    takeAwayItem()
    isSettingGhost4 = True
    killGhost4Bool = False
    checkHaveItem()
    alreadyWorking = False
    

def setGhost4RandomPos(): #ghost4의 위치를 아이템이 있는 칸 중에서 랜덤을 정한다.
    global haveItem, clickShop, alreadyWorking 
    global isMainScene, isEndScene
    
    randNum = random.randrange(0,6)
    checkHaveItem()

    if isMainScene == False or isEndScene == True:
        return
    
    if haveItem == False:
        alreadyWorking = False
        return
    
    while item[randNum] == "None": #해당자리에 아이템이 없다면 다시 위치를 선정한다.
        randNum = random.randrange(0,6)

    if clickShop == True: #상점이 열려있으면 Ghost4 생성 x
        alreadyWorking = False
        return
        
    ghost4['pos'][0] = itemPos[randNum][0]-10
    ghost4['pos'][1] = itemPos[randNum][1]-40
    
    ghost4['currentItemBoxIndex'] = randNum #현재 ghost4가 위치한 자리가 어디인지 저장

    threading.Timer(2, changeGhost4PosToBottomOfScreen).start()


def setGhost4RandomTime(): #ghost4의 나타날 시간을 랜덤으로 정한다.
    randTime = random.randrange(8,16) #8~15

    return randTime


#--------------------------------------------------------------------------------------------
#Ghost 1~3
def setRandomMovingSpeed(): #유령의 이동속도를 랜덤으로 정한다.
    global useItemReduceGhostSpeed
     
    randMoveSpeed = random.randrange(1, 16) #속도 : 1~15

    if useItemReduceGhostSpeed == True: #스피드 느려지는 아이템 사용시
        if randMoveSpeed >=6:
            randMoveSpeed -=5
        elif randMoveSpeed <=5: #스피드가 5이하인 경우는 최저 스피드인 1로 고정
            randMoveSpeed =1
            
    return randMoveSpeed


def setRandomColor(ghostNum): #좌우로 움직이는 유령의 색깔을 랜덤으로 정한다.
    global timeLimit,isDeadCheatingGhost
    
    color = ["White","Blue","Red"]
    randNum = random.randrange(0,3) # 0~2

    if isDeadCheatingGhost == True:
        if timeLimit >= 290:
            randNum = 0 #게임을 시작한뒤 10초까지는 하얀색 유령만 나오게 설정.
    else:
        if timeLimit >= 50:
            randNum = 0 #게임을 시작한뒤 10초까지는 하얀색 유령만 나오게 설정.
        
    return color[randNum]    


def matchGhostImage(ghostColor, ghostDir): #유령의 색깔에 맞게 이미지를 매치시킨다.
    if ghostColor == "White": #하얀색일 경우 
        if ghostDir == "LEFT":
            return imageWhiteGhostL
        else: #오른쪽일경우
            return imageWhiteGhostR
    elif ghostColor == "Red": #빨간색일 경우 
        if ghostDir == "LEFT":
            return imageRedGhostL
        else: #오른쪽일경우
            return imageRedGhostR
    else: #파랑색일 경우 
        if ghostDir == "LEFT":
            return imageBlueGhostL
        else: #오른쪽일경우
            return imageBlueGhostR


def moveGhost(): #유령들을 이동시키며 유령의 이미지 출력
    global clickShop, haveItem
    global isSettingGhost4, alreadyWorking, ghost4StartTime, copyGhost4RandTime

    for ghost in ghosts:      
        if ghost['num'] ==3: #ghost4
            if clickShop == False: #상점이 닫혀있을 경우만
                if haveItem == True:
                    if ghost['pos'][1] < SCREENHEIGHT: #ghost4의 위치가 화면 안에 있을 경우
                        screen.blit(imagePurpleGhost,[ghost['pos'][0],ghost['pos'][1]])
                    else:
                        if alreadyWorking == False: 
                            if isSettingGhost4 == True:
                                ghost4StartTime = time.time()
                                isSettingGhost4 = False
                                randTime = setGhost4RandomTime()
                                copyGhost4RandTime = randTime
                                threading.Timer(randTime, setGhost4RandomPos).start()
                                alreadyWorking = True       
                else:
                    checkHaveItem()
                    checkNoItemAndCoin()
            break

        #up, middle, down line ghost
        imageGhost = matchGhostImage(ghost['color'],ghost['dir'])
        if ghost['dir'] == "RIGHT":
            screen.blit(imageGhost,[ghost['pos'][0],ghost['pos'][1]],Rect(0,0,75,75))
            if clickShop == False:
                ghost['pos'][0] += ghost['moveSpeed']
        elif ghost['dir'] == "LEFT":
            screen.blit(imageGhost,[ghost['pos'][0],ghost['pos'][1]],Rect(0,0,75,75))
            if clickShop == False:
                ghost['pos'][0] -= ghost['moveSpeed']
        
        checkReachedEnd(ghost['num']) 
       

def checkReachedEnd(ghostNum): #유령이 끝에 도달했는지 확인    
    if ghosts[ghostNum]['dir'] == "RIGHT":
        if ghosts[ghostNum]['pos'].x > SCREENWIDTH:
            ghosts[ghostNum]['moveSpeed'] = setRandomMovingSpeed() #다시 소환될 유령의 스피드 랜덤으로 변화
            ghosts[ghostNum]['color'] = setRandomColor(ghostNum) #다시 소환될 유령의 색깔 랜덤으로 변화
            ghosts[ghostNum]['pos'].x = -75
           
    elif ghosts[ghostNum]['dir'] == "LEFT":
        if ghosts[ghostNum]['pos'].x < -75:
            ghosts[ghostNum]['moveSpeed'] = setRandomMovingSpeed() #다시 소환될 유령의 스피드 랜덤으로 변화
            ghosts[ghostNum]['color'] = setRandomColor(ghostNum) #다시 소환될 유령의 색깔 랜덤으로 변화
            ghosts[ghostNum]['pos'].x = SCREENWIDTH
 

def removeGhost(ghost): #유령을 제거한다.
    global killGhost4Bool, killedGhostCnt
    global coin, ghostPrice 
    
    if ghost['num'] !=3: #좌우로 움직이는 유령일 경우
        ghost['moveSpeed'] = setRandomMovingSpeed() #다시 소환될 유령의 스피드 랜덤으로 변화
        ghost['color'] = setRandomColor(ghost['num']) #다시 소환될 유령의 색깔 랜덤으로 변화
    
        #위치를 시작 지점으로 되돌린다.
        if ghost['dir'] == "RIGHT": 
            ghost['pos'][0] = -75 
        elif ghost['dir'] == "LEFT": 
            ghost['pos'][0] = SCREENWIDTH
    else:
        ghost['pos'][0] = SCREENWIDTH /2
        ghost['pos'][1] = SCREENHEIGHT +100
        killGhost4Bool = True

    killedGhostCnt +=1  
    coin += ghostPrice


def checkCurrentBulletAndGhostColor(ghost): #현재 총알과 유령의 색깔을 확인한다.
    for i in range(6):
        if itemPos[i][2] == True: # 현재 선택되어있는 아이템 칸.
            if "White" in item[i]: 
                if ghost['color'] == "White":#현재 선택한 유령의 색깔이 하얀색일 경우
                    return True
                
            elif "Red" in item[i]:
                if ghost['color'] == "Red":#현재 선택한 유령의 색깔이 빨간색일 경우
                    return True
                
            elif "Blue" in item[i]:
                if ghost['color'] == "Blue":#현재 선택한 유령의 색깔이 파란색일 경우
                    return True

            elif "Purple" in item[i]:
                if ghost['color'] == "Purple":#현재 선택한 유령의 색깔이 보라색일 경우
                    return True
                
            #총알 말고 다른 다른 아이템일 경우
            return False


def changeAvailableTimeForShopToTrue(): #Shop을 이용할 수 있도록 한다.
    global isAvailableTimeForShop
    
    isAvailableTimeForShop = True 


def compareMousePosAndShopPos(): #마우스와 Shop 위치를 비교
    global clickShop, isAvailableTimeForShop
    global isSettingGhost4

    openShop = False 
    isSamePos =[False,False] 
    mousePos = pygame.mouse.get_pos()
    if isAvailableTimeForShop == False:
        return
        
    if ghost4['pos'][1] < SCREENHEIGHT : #ghost4가 나타나있을 경우 상점을 못열게 한다.
        return
    
    if clickShop == True: #상점을 눌렀을 때
        openShop = True
        
    for i in range(2):
        if mousePos[0] >= shopPos.left and mousePos[0] <= shopPos.right:
            isSamePos[0] = True
                     
        if mousePos[1] >= shopPos.top and mousePos[1] <= shopPos.bottom:
            isSamePos[1] = True
    
    if openShop == False:
        if isSamePos[0] == True and isSamePos[1] == True:
            clickShop = True
        
    else: #상점이 열린상태일 경우
        if isSamePos[0] == True and isSamePos[1] == True:
            clickShop = False #상점을 닫는다.
            isAvailableTimeForShop = False
            threading.Timer(5, changeAvailableTimeForShopToTrue).start() #상점을 닫은 후 5초 후 상점 이용 가능하게 함.
            isSettingGhost4 = True #ghost4를 생성할수 있도록 함.
        
    
def compareMousePosAndGhostPos(mousePos):  #마우스와 유령의 위치를 비교
    isSamePos = [[False, False],[False, False],[False, False], [False,False]] # 같은 위치인가? = [x, y]
    
    for ghost in ghosts:
        if ghost['num'] != 3:          
            if mousePos[0] >= ghost['pos'].left and mousePos[0] <= ghost['pos'].right:
                isSamePos[ghost['num']][0] = True
                         
            if mousePos[1] >= ghost['pos'].top and mousePos[1] <= ghost['pos'].bottom:
                isSamePos[ghost['num']][1] = True
        else: #ghost4(아이템 뺏는 유령)
            if mousePos[0] >= ghost['pos'].left and mousePos[0] <= ghost['pos'].right:
                isSamePos[ghost['num']][0] = True
                     
            if mousePos[1] >= ghost['pos'].top and mousePos[1] <= 430:
                isSamePos[ghost['num']][1] = True
                

    for ghost in ghosts:       
        if isSamePos[ghost['num']][0] == True and isSamePos[ghost['num']][1] == True: #마우스의 위치와 유령의 위치가 일치할 경우
            return (True, ghost) #마우스의 위치와 유령이 같은 위치일 경우,  
     
    return (False, None)  #마우스의 위치와 유령이 다른 위치일 경우


def makeMousePosLookLikeGun(): #마우스가 위치한 곳을 총구로 보이게 한다.
    mousePos = pygame.mouse.get_pos()
    screen.blit(imageGunPoint,[mousePos[0]-32.5,mousePos[1]-32.5])


def changeHitTimeOverToFalse(): #유령에게 플레이어가 맞았을 시(총알 색깔 잘못 사용시) 0.5초만큼 이펙트 띄우기 관련
    global hitEffectTimeOver
    hitEffectTimeOver = True


def setHitEffect(): #유령의 색깔에 맞지 않게 공격했을 경우 유령에게 플레이어가 공격당한다.
    global hitEffectTimeOver
    
    if hitEffectTimeOver == False:
        screen.blit(imageHitEffect,[0,0],Rect(0,0,SCREENWIDTH,SCREENHEIGHT))
        

    
def manageAfterShooting(): #총을 쏜 이후 관리
    global playerHp, clickShop, hitEffectTimeOver
    
    if clickShop == True: #상점이 열려있는 경우에는 화면상에 있는 유령을 제거하지 못하게 한다.
        return
    
    ghostObj = compareMousePosAndGhostPos(pygame.mouse.get_pos())[1]
    
    #유령이랑 총구위치 일치하는지 확인
    if compareMousePosAndGhostPos(pygame.mouse.get_pos())[0] == False:
        return
    
    if checkCurrentBulletAndGhostColor(ghostObj) == False: #총구와 유령은 일치하나 총알과 유령의 색이 다를경우
        hitEffectTimeOver = False
        if hitEffectTimeOver == False:
            hitSound.play()
            threading.Timer(0.5, changeHitTimeOverToFalse).start()
        playerHp -=1
        return

    shootSound.play() #총 소리 재생
    #유령과 총구가 일치할 경우 + 유령의 색깔과 총알 색 일치할경우
    removeGhost(ghostObj)

        
#----------------------------------------------------------------------------------------
# 상점 아이템 사용 관련
def putShopItemInItemBox(shopItem): #상점에서 구매를 누른 후 구매 가능하면 해당 아이템을 빈 아이템 칸에 넣는다.
    #아이템 칸의 왼쪽부터 검사하여 빈곳이 있으면 해당자리에 아이템을 넣는다.
    for i in range(6):
        if item[i] == "None":
            item[i] = shopItem
            break


def compareClickedItemPriceToCoin(shopItemName): #사고싶은 아이템과 현재 코인 비교
    global coin
    
    #상점 아이템 가격
    shopItemPrice = {'WhiteBullet': 500, 'RedBullet':500, 'IncreaseTime': 1500,
                 'ReduceGhostSpeed': 1000, 'BlueBullet':500, 'PurpleBullet': 700,
                 'HealPack': 2000, 'DoubleCoin': 1500}

    if shopItemPrice[shopItemName] <= coin:
        buySound.play()
        coin -= shopItemPrice[shopItemName]
        putShopItemInItemBox(shopItemName)


def changeShopItemIndexToString(shopItemIndex): #아이템 인덱스를 문자열로 바꾼다.
    if shopItemIndex==0:
        return 'WhiteBullet'
    elif shopItemIndex==1:
        return 'RedBullet'
    elif shopItemIndex==2:
        return 'IncreaseTime'
    elif shopItemIndex==3:
        return 'ReduceGhostSpeed'
    elif shopItemIndex==4:
        return 'BlueBullet'
    elif shopItemIndex==5:
        return 'PurpleBullet'
    elif shopItemIndex==6:
        return 'HealPack'
    elif shopItemIndex==7:
        return 'DoubleCoin'


def checkAlreadyHaveItem(selectedShopItem): #구매하고 싶은 아이템이 아이템 창에 이미 있는지 확인   
    for i in range(6):
        if item[i] == selectedShopItem: #사고싶은 아이템이 이미 아이템창에 있는경우
            return True #이미 해당 아이템을 가지고 있음을 리턴
        
    return False #해당 아이템을 가지고 있지 않음을 리턴


#아이템 창이 전부 아이템으로 채워져 있는지 검사
def checkAllItemBoxIsFilled():
    global item
    
    for i in range(6):
        if item[i] == "None":
            break
        if i ==5:
            return False
    return True


def checkClickPurchase(): #상점에서 아이템 구매를 클릭했는지 검사
    global clickShop
    
    startShopItemPos = [80, 215]
    shopItemXInterval = [0,110,230,340] #상점 아이템 간격 짧은 부분 x좌표  
    shopItemClickBuyBool = []
    mousePos = pygame.mouse.get_pos()
    
    if clickShop == False: #상점이 닫혀있다면 구매할수 없게 만든다.
        return
    
    for i in range(8):
        shopItemClickBuyBool.append([False,False]) #모두 False로 초기화
        
    #상점 아이템 인덱스
    # 0 1 2 3
    # 4 5 6 7
    shopItemIndex =0
    for a in range(2):
        for b in range(4):
            if mousePos[0] >=startShopItemPos[0]+shopItemXInterval[b]:
                if mousePos[0] <= startShopItemPos[0]+shopItemXInterval[b]+100:
                    shopItemClickBuyBool[shopItemIndex][0] = True                 
            
            if mousePos[1] >= startShopItemPos[1]:
                if mousePos[1] <= startShopItemPos[1] + 35:
                    shopItemClickBuyBool[shopItemIndex][1] = True
            shopItemIndex +=1
            
        startShopItemPos[1] = 370

    for i in range(8):
        if shopItemClickBuyBool[i][0] == True and shopItemClickBuyBool[i][1] == True:
            shopItemName = changeShopItemIndexToString(i)
            alreadyHaveItem = checkAlreadyHaveItem(shopItemName) #구매하고자하는 아이템을 이미 소지하고 있는가?
            canFillInItemSpace = checkAllItemBoxIsFilled() #아이템 창이 전부 채워져 있는가?
            if alreadyHaveItem == False and canFillInItemSpace == True:
                compareClickedItemPriceToCoin(shopItemName)    
            break
        
        
#-------------------------------------------------------------------------------------------------------
#아이템 사용(총알 제외)
def useItemExceptBullet(): #아이템 사용키 - Space Bar
    global useItemDoubleCoin, useItemReduceGhostSpeed 
    
    for i in range(6):
        if itemPos[i][2] == True: #현재 선택한 아이템 확인
            if item[i] == "IncreaseTime":
                increaseTime(i)
                
            elif item[i] == "ReduceGhostSpeed":
                if useItemReduceGhostSpeed == False:
                    reduceGhostSpeed(i)
                
            elif item[i] == "HealPack":
                healPlayerHp(i)
                
            elif item[i] == "DoubleCoin":
                if useItemDoubleCoin == False:
                    makeDoubleCoin(i)


def increaseTime(itemIndex): #시간 증가시키기
    global timeLimit

    timeLimit +=10
    item[itemIndex] = "None"
        

def healPlayerHp(itemIndex): #Player Hp 회복
    global playerHp, item 

    if playerHp < 3:
        playerHp +=1
        item[itemIndex] = "None"


def changeDCItemTimeToFalse(): #10초동안 DoubleCoin(DC)효과 지속 후 아이템 효과 끄기
    global ghostPrice, useItemDoubleCoin 

    useItemDoubleCoin = False
    ghostPrice = 100


def makeDoubleCoin(itemIndex): #유령을 죽일 시 얻는 코인 2배 증가(10초간)
    global ghostPrice, useItemDoubleCoin
    
    item[itemIndex] = "None" 
    useItemDoubleCoin = True
    ghostPrice = 200
    threading.Timer(10, changeDCItemTimeToFalse).start()


def changeRGSItemTimeToFalse(): #7초동안 ReduceGhostSpeed(RGS)효과 지속 후 아이템 효과 끄기
    global useItemReduceGhostSpeed
    useItemReduceGhostSpeed = False

 
def reduceGhostSpeed(itemIndex): #유령 스피드 5 감소(7초간)
    global useItemReduceGhostSpeed
    
    useItemReduceGhostSpeed = True
    item[itemIndex] = "None"
    
    for ghost in ghosts:
        if ghost['num'] !=3: #좌우로 움직이는 유령일 경우
            if ghost['moveSpeed'] >=6:
                ghost['moveSpeed'] -=5
            elif ghost['moveSpeed'] <=5: #스피드가 5이하인 경우는 최저 스피드인 1로 고정
                ghost['moveSpeed'] =1
                    
    threading.Timer(7, changeRGSItemTimeToFalse).start()                  


def setUsingItemEffect(): #사용중인 아이템 화면 왼쪽 상단에 띄우기
    global useItemDoubleCoin, useItemReduceGhostSpeed

    if useItemDoubleCoin == True:
        screen.blit(imageDoubleCoinEffect,[35,5])
    if useItemReduceGhostSpeed == True:
        screen.blit(imageReduceGhostSpeedEffect,[5,5])

        
#-------------------------------------------------------------------------------------------
#Tutorial Scene 관리
def viewTutorialTitle(): #Tutorial 제목 띄우기
    font = pygame.font.SysFont("arial",40,True)
    tutorialText = font.render("Tutorial", True, WHITE)
    screen.blit(tutorialText, [225, 70])


def setTutorialPage1(): #게임에 대한 간략한 설명을 하는 페이지
    viewTutorialTitle()

    font = pygame.font.SysFont("arial",25,True)
    topicText = ["Your job :", "Goal :", "1 to 6 key :", "Space Bar :", "Left Click :"]
    for i in range(5):
        text = font.render(topicText[i], True, BLACK)
        screen.blit(text, [100, 150 + 50 * i])

    font = pygame.font.SysFont("arial",20,True)
    contentText = ["Ghost Hunter", "kill many ghosts within the time limit",
                   "choose an item", "use items other than bullets", "can kill ghost"]
    contentTextPos = [205, 165, 215, 220, 215]
    for i in range(5):
        text = font.render(contentText[i], True, WHITE)
        screen.blit(text, [contentTextPos[i], (150 + 50 * i)+5])


def setTutorialPage2(): #규칙 설명하는 페이지
    viewTutorialTitle()

    screen.blit(imageGhostAndBullet,[100,130])
    font = pygame.font.SysFont("arial",20,True)
    contentText = ["You have to kill the ghost according to the color of ", "the bullet you are using. Otherwise, your Hp will"
                   ,"decrease.", "If you kill a ghost, you get 100$."]
    for i in range(4):
        text = font.render(contentText[i], True, WHITE)
        screen.blit(text, [100, 300+ 25 *i])
    

def setTutorialPage3(): #게임이 끝나는 조건을 알려주는 페이지
    viewTutorialTitle()

    font = pygame.font.SysFont("arial",25,True)
    text = font.render("<Condition where the game ends>", True, BLACK)
    screen.blit(text, [125, 150])

    font = pygame.font.SysFont("arial",20,True)
    contentText = ["1. When the time is up", "2. If Hp becomes 0"
                   ,"3. If you lose all your items and don't have money", "    to buy them"]
    for i in range(4):
        text = font.render(contentText[i], True, WHITE)
        screen.blit(text, [100,  200 + 40 *i])


def setTutorialPage4(): #좌우로 움직이는 유령에 대해 설명을 해주는 페이지
    viewTutorialTitle()
    screen.blit(imagePage4Ghost,[100,130])
    
    font = pygame.font.SysFont("arial",20,True)
    topicText = ["Speed :", "Color :", "Pos :"]
    for i in range(3):
        text = font.render(topicText[i], True, BLACK)
        screen.blit(text, [300, 160 + 40 * i])

    font = pygame.font.SysFont("arial",20,True)
    contentText = ["1~15", "white, blue, red", "up, middle, down line"]
    contentTextPosX = [365,360,345]
    for i in range(3):
        text = font.render(contentText[i], True, WHITE)
        screen.blit(text, [contentTextPosX[i], 160 + 40 * i])

    descriptionText = ["In a total of three lines, ghosts appear with random"
                   , "attribute values. It keeps moving from side to side."
                   , "Only white ghosts appear for 10 seconds after the start."]
    for i in range(3):
        text = font.render(descriptionText[i], True, WHITE)
        screen.blit(text, [100, 320 + 30 * i])


def setTutorialPage5(): #보라색 유령에 대해 설명을 해주는 페이지
    viewTutorialTitle()
    screen.blit(imagePage5Ghost,[125,150])
    
    font = pygame.font.SysFont("arial",20,True)
    topicText = ["Color :", "Pos :", "Time to appear :"]
    topicTextPos = [(300, 160),(300, 200), (300,260)]
    for i in range(3):
        text = font.render(topicText[i], True, BLACK)
        screen.blit(text, topicTextPos[i])
        
    font = pygame.font.SysFont("arial",20,True)
    contentText = ["purple", "The item compartment", "that the player has", "8~15s"]
    contentTextPos = [(365, 160),(355, 200), (355,230),(435, 260)]
    for i in range(4):
        text = font.render(contentText[i], True, WHITE)
        screen.blit(text, contentTextPos[i])

    descriptionText = ["Ghosts appear in random item compartments at",
                       "random times. If the player fails to kill the purple"
                   , "ghost in 2 seconds, steal the item."]
    for i in range(3):
        text = font.render(descriptionText[i], True, WHITE)
        screen.blit(text, [100, 320 + 30 * i])


def setTutorialPage6(): #아이템에 대해 설명해주는 페이지
    global cheatingGhostManagement, isDeadCheatingGhost
    
    viewTutorialTitle()

    font = pygame.font.SysFont("arial",25,True)
    text = font.render("<Item : Press the space bar to use it>", True, BLACK)
    screen.blit(text, [125, 150])

    font = pygame.font.SysFont("arial",17,True)
    contentText = ["Increase the time by 10 seconds.", "Reduce the ghost's speed for 7 seconds."
                   , "Increase Hp by 1.", "Change the price of the ghost to 200$ for 10 seconds."]
    for i in range(4):   
        text = font.render(contentText[i], True, WHITE)
        screen.blit(text, [150, 207 + (50 * i)])
    
    screen.blit(imageIncreaseTime, [100, 200])
    screen.blit(imageReduceGhostSpeed, [100, 250])
    screen.blit(imageHealPack, [100, 300])
    screen.blit(imageDoubleCoin, [102, 350])

    if cheatingGhostManagement == True and isDeadCheatingGhost == False: 
        #6페이지에서 c누를 경우 치트유령 죽일 수 있게 띄우기 + 한번만 치트유령이 나타날수 있게.
        screen.blit(imageCheatingGhost, [500, 420]) 

    
def checkPreviousOrNextPageButton(): #이전, 다음 페이지 이동 버튼 눌렀는지 체크한다.
    global currentPage
    
    mousePos = pygame.mouse.get_pos()

    #이전 페이지로 넘어가는 버튼 눌렀는지 검사
    if mousePos[0] >=70 and mousePos[0] <=95:
        if mousePos[1] >=400 and mousePos[1] <= 430:
            if currentPage > 1:
                buySound.play()
                currentPage = currentPage-1
    
    #다음 페이지로 넘어가는 버튼 눌렀는지 검사
    if mousePos[0] >=510 and mousePos[0] <=535:
        if mousePos[1] >=400 and mousePos[1] <= 430:
            if currentPage < 6:
                buySound.play()
                currentPage = currentPage+1


def checkExitTutorialSceneButton(): #Tutorial에서 X버튼(오른쪽 상단에 있는 UI) 눌렀는지 확인한다.
    global isTutorialScene, isStartScene
    global currentPage
    
    mousePos = pygame.mouse.get_pos()

    #이전 페이지로 넘어가는 버튼 눌렀는지 검사
    if mousePos[0] >=505 and mousePos[0] <=535:
        if mousePos[1] >=70 and mousePos[1] <= 100:
            buySound.play()
            isTutorialScene = False
            isStartScene = True
            currentPage = 1

    
def viewCurrentPage(): #현재 페이지에 해당되는 페이지를 보여주기
    global currentPage, cheatingGhostManagement

    for i in range(1,6): #1~5
        if currentPage == i:
            cheatingGhostManagement = False
    
    if currentPage == 1:
        setTutorialPage1() 
    elif currentPage == 2:
        setTutorialPage2()
    elif currentPage == 3:
        setTutorialPage3()
    elif currentPage == 4:
        setTutorialPage4()
    elif currentPage == 5:
        setTutorialPage5()
    elif currentPage == 6:
        setTutorialPage6()

    setPreviousAndNextPageButton()
                   

def setPreviousAndNextPageButton(): #이전, 다음 페이지 이동 버튼 띄우기
    global currentPage

    if currentPage ==1:
        screen.blit(imageNextPageButton, [510, 400])    
    elif currentPage == 6:
        screen.blit(imagePreviousPageButton, [70, 400])
    else:
        screen.blit(imagePreviousPageButton, [70, 400])
        screen.blit(imageNextPageButton, [510, 400])

        
#-------------------------------------------------------------------------------------------
#Scene 관리        
def resetGame(): #게임 관련 정보를 초기화한다. - isGameOver,killedGhostCnt는 제외.(다른 곳에서 제어)
    global ghostPrice, timeLimit, coin, playerHp, printEmptyHpCnt, item, itemPos, isDeadCheatingGhost
    global isAvailableTimeForShop, isChangingTime, haveItem, isSettingGhost4, hitEffectTimeOver, alreadyWorking #True로 초기화
    global killGhost4Bool, clickShop, printTime0, useItemDoubleCoin ,useItemReduceGhostSpeed #False로 초기화

    for i in range(6):
        itemPos[i][2] = False
    
    itemPos[0][2] = True
    item = ["WhiteBullet", "None", "None", "None", "None", "None"]
    
    ghost1['pos'] = pygame.Rect(-50,75,75,75)
    ghost1['dir'] = "RIGHT"
    ghost2['pos'] = pygame.Rect(SCREENWIDTH,185,75,75)
    ghost2['dir'] = "LEFT"
    ghost3['pos'] = pygame.Rect(-50,295,75,75)
    ghost3['dir'] = "RIGHT"
    ghost4['pos'] = pygame.Rect(SCREENWIDTH/2,SCREENHEIGHT +100, 75, 45)
    ghost4['currentItemBoxIndex'] = "None"
    ghost4['color'] = "Purple"
    
    for ghost in ghosts:
        if ghost['num'] != 3:
            ghost['color'] = "White"
            ghost['moveSpeed'] = 3

    ghostPrice = 100
    playerHp = 3
    printEmptyHpCnt = 0

    #치트 유령을 잡을 경우 값이 바뀌는 변수
    if isDeadCheatingGhost == True:
        timeLimit = 300
        coin = 50000
    else:
        timeLimit = 60
        coin = 0
    
    #True로 초기화
    boolValue = True

    isAvailableTimeForShop = boolValue
    isChangingTime = boolValue
    haveItem = boolValue
    isSettingGhost4 = boolValue
    hitEffectTimeOver = boolValue
    

    #False로 초기화
    boolValue = False
    
    killGhost4Bool = boolValue
    clickShop = boolValue
    printTime0 = boolValue
    useItemDoubleCoin = boolValue  
    useItemReduceGhostSpeed = boolValue
    alreadyWorking = boolValue
        

def checkGoTitleAndReplay(): #GameOver시 클릭 검사. 
    global isStartScene ,isEndScene, isMainScene, CanMoveEndSceneToNextScene
    global isGameOver, killedGhostCnt
    
    mousePos = pygame.mouse.get_pos()

    #왼쪽의 Go Title 클릭시
    if mousePos[0] >= 5 and mousePos[0] <=80:
        if mousePos[1] >=420 and mousePos[1] <= 495:
            isStartScene = True
            isEndScene = False
            isGameOver = False
            killedGhostCnt = 0
            CanMoveEndSceneToNextScene = False
            return
        
    #오른쪽의 Replay 클릭시
    if mousePos[0] >= 520 and mousePos[0] <=595:
        if mousePos[1] >=420 and mousePos[1] <= 495:
            isMainScene = True
            isEndScene = False
            isGameOver = False
            killedGhostCnt = 0
            CanMoveEndSceneToNextScene = False
            resetGame()
            return
            

def printEndScene(): #End Scene 출력
    global killedGhostCnt, CanMoveEndSceneToNextScene 
    
    screen.blit(imageGameOver, [0,0])
    if CanMoveEndSceneToNextScene == True:
        screen.blit(imageGoTitle, [5,420])
        screen.blit(imageReplay, [520,420])
    
    font = pygame.font.SysFont("arial",30,True)
    killedGhostContentText = font.render("Killed Ghost :", True, RED)
    killedGhostCntText = font.render(str(killedGhostCnt), True, RED)
    
    screen.blit(killedGhostContentText, [195,5])
    screen.blit(killedGhostCntText, [365,5])


def setEndScene(): #End Scene Game Loop
    global killedGhostCnt, isStartScene, CanMoveEndSceneToNextScene
    
    screen.fill(WHITE)
    printEndScene() #EndScene 출력
        
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if CanMoveEndSceneToNextScene == True:
                checkGoTitleAndReplay()
    
    mainClock.tick(60)
    pygame.display.update()
        

def fixStartSceneGhostColor(): #Start Scene에서 유령의 색깔을 고정해놓는다.
    global haveItem
    
    for ghost in ghosts:
        if ghost['num'] !=3:
            ghost['moveSpeed'] = 1
            
    ghost1['color'] = "White"
    ghost2['color'] = "Blue"
    ghost3['color'] = "Red"
    haveItem = False #시작화면에서는 ghost4사용 x, 따라서 ghost4 안나타나게 조건 설정


def makeGhostNameAtStartScreen(): #시작화면에서 유령의 이름 붙여주기
    font = pygame.font.SysFont("arial",20,True)
    ghost1NameText = font.render("Game Start", True, WHITE)
    ghost2NameText = font.render("Go Turtorial", True, WHITE)
    ghost3NameText = font.render("Game Exit", True, WHITE)
    
    screen.blit(ghost1NameText, [ghost1['pos'][0], ghost1['pos'][1]-15])
    screen.blit(ghost2NameText, [ghost2['pos'][0]-15, ghost2['pos'][1]-15])
    screen.blit(ghost3NameText, [ghost3['pos'][0]+5, ghost3['pos'][1]-15])


def printTitle(): #제목(The Ghost Hunter) 출력
    font = pygame.font.SysFont("arial",50,True)
    titleText = font.render("The Ghost Hunter", True, WHITE)
    screen.blit(titleText, [125, 420])


def moveNextScene(): #StartScene에서 선택한 유령의 이름대로 Scene 이동하기
    global isStartScene,isMainScene ,isTutorialScene 
    global killedGhostCnt
 
    isSamePos = compareMousePosAndGhostPos(pygame.mouse.get_pos())

    if isSamePos[0] == True: #유령과 마우스 위치가 같을 경우
        shootSound.play()
        if isSamePos[1]['num'] == 0: #Game Start일 경우
            shootSound.play()
            isStartScene = False
            isMainScene = True
            resetGame()
            killedGhostCnt =0
            return
        elif isSamePos[1]['num'] == 1: #Go Turtorial일 경우
            shootSound.play()
            isStartScene = False
            isTutorialScene = True
            return
        elif isSamePos[1]['num'] == 2: #Game Exit일 경우
            shootSound.play()
            pygame.quit()
            sys.exit()


def setStartScene(): #Start Scene Game Loop
    screen.fill(WHITE)
    screen.blit(imageStartBG, [0,0])
    fixStartSceneGhostColor()
    moveGhost()
    makeGhostNameAtStartScreen()
    printTitle()
    
    for event in pygame.event.get(): 
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            moveNextScene()

    makeMousePosLookLikeGun()
    mainClock.tick(60)
    pygame.display.update()


def setTutorialScene(): #Tutorial Scene Game Loop
    global cheatingGhostManagement, isDeadCheatingGhost
    
    screen.fill(WHITE)
    screen.blit(imageBG,[0,0])
    screen.blit(imageShopBG,[50,50])
    screen.blit(imageExitTutorialSceneButton, [505, 70])
    viewCurrentPage()
    
    for event in pygame.event.get():  
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                checkPreviousOrNextPageButton()
                checkExitTutorialSceneButton()
                removeCheatingGhost()
            if event.type == pygame.KEYDOWN:
                checkConditionCanMakeCheatingGhost(event.key)
                    
    makeMousePosLookLikeGun()
    mainClock.tick(60)
    pygame.display.update()
        


def setMain(): #Main Scene Game Loop
    global isMainScene, isEndScene, isGameOver 
    global ghost4StartTime, ghost4EndTime, CanMoveEndSceneToNextScene
    
    if isGameOver == True:
        ghost4EndTime = time.time()  
        ghost4EndTime = round(ghost4EndTime - ghost4StartTime)
        ghost4ResetTime = calculateGhost4EndTimeMinusGameEndTime(ghost4EndTime)
        threading.Timer(ghost4ResetTime, changeCanMoveEndSceneToNextSceneToTrue).start()
        isMainScene = False
        isEndScene = True
        resetGame()
        return
    
    screen.fill(WHITE)
    setBackground()
    setHpUI()
    moveGhost()
    setItemUI()
    setTimeUI()
    setShopUI()
    setUsingItemEffect()
    setHitEffect()
  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            checkInput(event.key)
            if event.key == pygame.K_SPACE:
                useItemExceptBullet()
        if event.type == pygame.MOUSEBUTTONUP:
            manageAfterShooting()
            compareMousePosAndShopPos()
            checkClickPurchase()
            
    makeMousePosLookLikeGun()
    mainClock.tick(60)
    pygame.display.update()
    checkIsNoHp()




#아이템 구매, 구매한 아이템을 아이템창에 넣기, 돈 계산, 오류처리 까지 완성.
#아이템을 사용하는 거 구현완료 (12월 4일- 토요일 새벽 2시)
#씬 나누기 구현 완료 (12월 5일 - 새벽 1시 25분)
#씬 간 이동 구현 완료 (12월 5일 - 새벽 3시 41분)
#12월 15일 튜토리얼 구현 완료
#그냥 ghost4생성함수가 동작한 시간을 기준으로 게임이 끝난 시간까지 계산을 해서 그 시간만큼 기다린 다음 게임 재시작 하게 하기.
#위 사항까지 모든 내용 구현 완료 (12월 15일 7시 40분)
#추가적으로 치트 유령 구현 완료.(12월 16일 3시 30분)



#Game Loop
while True:

    while isStartScene:       
        setStartScene()
        
    while isMainScene:
        setMain()

    while isEndScene:
        setEndScene()

    while isTutorialScene:
        setTutorialScene()
