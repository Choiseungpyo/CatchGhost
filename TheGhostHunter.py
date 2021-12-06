import pygame, sys #기본세팅
import random, time, threading #내가 추가한 것
from pygame.locals import *

#Set up pygame.
pygame.init()

mainClock = pygame.time.Clock()

pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.set_volume(0.5)

shootSound = pygame.mixer.Sound("shoot.ogg")
shootSound.set_volume(0.3)

buySound = pygame.mixer.Sound("buy.ogg")
buySound.set_volume(0.3)

hitSound = pygame.mixer.Sound("hit.ogg")
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

#변수 정의
isMainScene = True
isStartScene = False #나중에 StartScene 만들면 이 변수  True로 바꾸고 시작화면부터 할 수 있게 하기.
isEndScene = False

 #플레이어의 Hp
playerHp = 3
printEmptyHpCnt = 0

 #아이템 창 itemPos = [x좌표, y좌표, 해당 아이템 번호를 눌렀는지]
itemPos =[]
for i in range(6):
    itemPos.append([150+55*i,440, False])
itemPos[0][2] = True
item = ["WhiteBullet", "None", "None", "None", "None", "None"] 

 #유령 
ghost1 = {'num': 0, 'pos': pygame.Rect(-50,75,75,75), 'dir':"RIGHT", 'moveSpeed': 3, 'color': "White"} 
ghost2 = {'num': 1, 'pos': pygame.Rect(SCREENWIDTH,185,75,75), 'dir':"LEFT", 'moveSpeed': 3, 'color': "White"}
ghost3 = {'num': 2, 'pos': pygame.Rect(-50,295,75,75), 'dir':"RIGHT", 'moveSpeed': 3, 'color': "White"}
ghost4 = {'num': 3, 'pos': pygame.Rect(SCREENWIDTH/2,SCREENHEIGHT +100, 75, 45), 'color': "Purple", 'currentItemBoxIndex': "None"}
ghosts = [ghost1,ghost2,ghost3, ghost4]

 #유령을 죽였을 시 얻는 가격
ghostPrice = 100
killedGhostCnt = 0
killGhost4Bool = False

 #상점 
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

 #돈
coin = 10000

 #ghost4
isSettingGhost4 = True
alreadyWorking = False #스레드에서 시간 차이로 인한 오류가 생기므로 해당 함수가 끝난 후 동작할 수 있도록 함.

 #hit effect
hitEffectTimeOver = True

 #리셋할 때 필요한 변수들
resetFalseAggregation= [killGhost4Bool, clickShop, printTime0, useItemDoubleCoin,
                            useItemReduceGhostSpeed,alreadyWorking]
resetTrueAggregation = [isAvailableTimeForShop, isChangingTime, haveItem, isSettingGhost4, hitEffectTimeOver]



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
imageDoubleCoinEffect = pygame.image.load("images/doubleCoinEffect.png")
imageDoubleCoinEffect = pygame.transform.scale(imageDoubleCoinEffect,(25,25))

imageReduceGhostSpeedEffect = pygame.image.load("images/reduceGhostSpeedEffect.png")
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


#화면
screen = pygame.display.set_mode((600,500), 0,32)
pygame.display.set_caption("The Ghost Hunter")


#-----------------------------------------------------------------------------------------------
#함수
def checkIsNoHp(): #체력이 없는지 확인한다.
    global playerHp
    global isGameOver
    
    if playerHp <= 0 and printEmptyHpCnt ==3: #0보다 작다고 하면 Hp를 전부 감소시키지 않은상태에서 끝난다.
         #print("체력이 없어 게임종료")
         isGameOver = True
         

def reduceTimeLimit(): #제한시간을 감소시킨다.
    global timeLimit
    global isChangingTime
    global printTime0
    
    if timeLimit ==1:
        printTime0 = True
        
    if clickShop == False: #상점을 눌렀을때는 시간을 감소시키지 않는다.
        timeLimit -=1
        
    isChangingTime = True

def setBackground():
    screen.blit(imageBG,[0,0],Rect(0,0,SCREENWIDTH,SCREENHEIGHT))

    
def setHpUI():
    global printEmptyHpCnt
    printEmptyHpCnt = 0
    
    for i in range(3):
        if i< playerHp: 
            screen.blit(imagePlayerFullHp, [15+40*i,450]) #채워진 하트 
        else:
            screen.blit(imagePlayerEmptyHp, [15+40*i,450])  #빈 하트
            printEmptyHpCnt +=1
            

def setItemUI():
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
    

def setTimeUI():
    global timeLimit
    global isChangingTime
    global printTime0
    global isGameOver
            
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
        #print("시간 끝")
        
        
def setShopUI():
    global clickShop
    global isAvailableTimeForShop

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

#key
#------------------------------------------------------------------------------------------
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
    global clickShop

    if clickShop == False:
        if eventKey >= NUM1 and eventKey <= NUM6:
            num = changeEventKeyToNum(eventKey)
            checkSelectedItem(num)


#Ghost4
#-----------------------------------------------------------------------------------------------        
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
    global coin
    global haveItem
    global isGameOver
    
    if coin < 500 and haveItem == False:
        isGameOver = True

        
def takeAwayItem(): #ghost4가 나타난 자리에 아이템을 가져간다.
    global killGhost4Bool

    if killGhost4Bool == False: #ghost4를 못 죽였을 경우
        if ghost4['currentItemBoxIndex'] != "None":
            item[ghost4['currentItemBoxIndex']] = "None"
            
        
def changeGhost4PosToBottomOfScreen(): #ghost4를 화면 바깥으로 위치시킨다.
    global isSettingGhost4
    global killGhost4Bool
    global alreadyWorking
    
    #print("ghost4 화면 밖으로 이동")
    
    ghost4['pos'][0] = SCREENWIDTH/2
    ghost4['pos'][1] = SCREENHEIGHT +100
    takeAwayItem()
    isSettingGhost4 = True
    killGhost4Bool = False
    checkHaveItem()
    alreadyWorking = False
    

def setGhost4RandomPos(): #ghost4의 위치를 아이템이 있는 칸 중에서 랜덤을 정한다.
    global haveItem
    global clickShop
    global alreadyWorking
    
    randNum = random.randrange(0,6)
    checkHaveItem()
    
    if haveItem == False:
        #print("마지막 고스트4 위치:", ghost4['pos'])
        alreadyWorking = False
        return
    
    while item[randNum] == "None": #해당자리에 아이템이 없다면 다시 위치를 선정한다.
        #print(randNum)
        randNum = random.randrange(0,6)

    if clickShop == True: #상점이 열려있으면 Ghost4 생성 x
        #print("상점이 열려있으므로 Ghost4 생성 x")
        alreadyWorking = False
        return
        
    ghost4['pos'][0] = itemPos[randNum][0]-10
    ghost4['pos'][1] = itemPos[randNum][1]-40
    
    ghost4['currentItemBoxIndex'] = randNum #현재 ghost4가 위치한 자리가 어디인지 저장

    threading.Timer(2, changeGhost4PosToBottomOfScreen).start()
    #print("가져갈 아이템 인덱스:", randNum)


def setGhost4RandomTime(): #ghost4의 나타날 시간을 랜덤으로 정한다.
    randTime = random.randrange(20,25) #3~10

    return randTime


#ghost 1~3
#--------------------------------------------------------------------------------------------
def setRandomMovingSpeed(): #유령의 이동속도를 랜덤으로 정한다.
    global useItemReduceGhostSpeed
     
    randMoveSpeed = random.randrange(1, 10) #속도 : 1~15

    if useItemReduceGhostSpeed == True: #스피드 느려지는 아이템 사용시
        if randMoveSpeed >=6:
            randMoveSpeed -=5
        elif randMoveSpeed <=5: #스피드가 5이하인 경우는 최저 스피드인 1로 고정
            randMoveSpeed =1
        #print("reduceGhostSpeed 아이템 사용중!!")
            
    return randMoveSpeed


def setRandomColor(ghostNum): #좌우로 움직이는 유령의 색깔을 랜덤으로 정한다.
    color = ["White","Blue","Red"]
    randNum = random.randrange(0,3) # 0,1,2
    return color[randNum]    


def matchGhostImage(ghostColor, ghostDir): #유령의 색깔에 맞게 이미지를 대응시킨다.
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
    global clickShop
    global haveItem
    global isSettingGhost4
    global alreadyWorking

 
    #이미지 출력 및 방향에 따른 이동 계산
    for ghost in ghosts:      
        if ghost['num'] ==3: #ghost4
            if clickShop == False: #상점이 닫혀있을 경우만
                if haveItem == True:
                    if ghost['pos'][1] < SCREENHEIGHT: #ghost4의 위치가 화면 안에 있을 경우
                        screen.blit(imagePurpleGhost,[ghost['pos'][0],ghost['pos'][1]])
                    else:
                        if alreadyWorking == False:
                            if isSettingGhost4 == True:
                                isSettingGhost4 = False
                                randTime = setGhost4RandomTime()
                                #print(randTime, " 후에 ghost4 등장")
                                threading.Timer(randTime, setGhost4RandomPos).start()
                                alreadyWorking = True       
                else:
                    checkHaveItem()
                    checkNoItemAndCoin()
            break
        
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
    global killGhost4Bool #ghost4를 죽였는지 확인하는 변수
    global coin
    global ghostPrice
    global killedGhostCnt
    
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
        #print("ghost4를 죽였습니다.")

    killedGhostCnt +=1  
    coin += ghostPrice


def checkCurrentBulletAndGhostColor(ghost): #현재 총알과 유령의 색깔을 확인한다.
    for i in range(6):
        if itemPos[i][2] == True: # 현재 선택되어있는 아이템 칸.
            if "White" in item[i]: 
                if ghost['color'] == "White":#현재 선택한 유령의 색깔이 하얀색일 경우
                    #print("하얀색")
                    return True
                
            elif "Red" in item[i]:
                if ghost['color'] == "Red":
                    #print("빨간색")
                    return True
                
            elif "Blue" in item[i]:
                if ghost['color'] == "Blue":
                    #print("파란색")
                    return True

            elif "Purple" in item[i]:
                if ghost['color'] == "Purple":
                    #print("보라색")
                    return True
                
            #총알 말고 다른 다른 아이템일 경우
            #print("총알이 아닌 다른 아이템")
            return False
            
    print("오류")
    return "오류"


def changeAvailableTimeForShopToTrue():
    global isAvailableTimeForShop
    
    isAvailableTimeForShop = True #샵을 이용할 수 있도록 한다.


def compareMousePosAndShopPos(): #마우스와 Shop 위치를 비교
    global clickShop
    global isSettingGhost4
    global isAvailableTimeForShop
    openShop = False 
    isSamePos =[False,False] 
    mousePos = pygame.mouse.get_pos()
    if isAvailableTimeForShop == False:
        return
        
    if ghost4['pos'][1] < SCREENHEIGHT : #Ghost4가 나타나있을 경우 상점을 못열게 함.
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
            #print("상점을 엽니다.")
    else: #상점이 열린상태일 경우
        if isSamePos[0] == True and isSamePos[1] == True:
            clickShop = False #상점을 닫는다.
            isAvailableTimeForShop = False
            threading.Timer(5, changeAvailableTimeForShopToTrue).start() #5초 후 상점 이용가능하게 함.
            isSettingGhost4 = True #Ghost4를 생성할수 있도록 함.
            #print("상점을 닫습니다.")
        
    
def compareMousePosAndGhostPos(mousePos):  #마우스와 유령의 위치를 비교
    isSamePos = [[False, False],[False, False],[False, False], [False,False]] # 같은 위치인가? = [x, y]
    
    for ghost in ghosts:     
        if mousePos[0] >= ghost['pos'].left and mousePos[0] <= ghost['pos'].right:
            isSamePos[ghost['num']][0] = True
                     
        if mousePos[1] >= ghost['pos'].top and mousePos[1] <= ghost['pos'].bottom:
            isSamePos[ghost['num']][1] = True 

    for ghost in ghosts:       
        if isSamePos[ghost['num']][0] == True and isSamePos[ghost['num']][1] == True: #마우스의 위치와 유령의 위치가 일치할 경우
            return (True, ghost) #마우스의 위치와 유령이 같은 위치일 경우,  
     
    return (False, None)  #마우스의 위치와 유령이 다른 위치일 경우


def makeMousePosLookLikeGun(): #마우스가 위치한 곳을 총구로 보이게 한다.
    mousePos = pygame.mouse.get_pos()
    screen.blit(imageGunPoint,[mousePos[0]-32.5,mousePos[1]-32.5])


def changeHitTimeOverToFalse():
    global hitEffectTimeOver
    hitEffectTimeOver = True


def setHitEffect(): #유령의 색깔에 맞지 않게 공격했을 경우 유령에게 플레이어가 공격당한다.
    global hitEffectTimeOver
    if hitEffectTimeOver == False:
        screen.blit(imageHitEffect,[0,0],Rect(0,0,SCREENWIDTH,SCREENHEIGHT))
        

    
def manageAfterShooting():
    global playerHp
    global clickShop
    global hitEffectTimeOver

    
    if clickShop == True: #상점이 열려있는 경우에는 화면상에 있는 유령을 제거하지 못하게 한다.
        return
    
    ghostObj = compareMousePosAndGhostPos(pygame.mouse.get_pos())[1]
     #유령이랑 총구위치 이 일치하는지 확인
    if compareMousePosAndGhostPos(pygame.mouse.get_pos())[0] == False:
        #print("유령과 총구가 불일치")
        return
    
    if checkCurrentBulletAndGhostColor(ghostObj) == False: #총구와 유령은 일치하나 총알과 유령의 색이 다를경우
        #print("유령과 총구가 일치, 유령의 색깔과 총알 색 불일치")
        hitEffectTimeOver = False
        if hitEffectTimeOver == False:
            #print("hit Sound 재생")
            hitSound.play()
            threading.Timer(0.5, changeHitTimeOverToFalse).start()
        playerHp -=1
        return

    shootSound.play() #총 소리 재생
    #print("shoot Sound 재생")
    #유령과 총구가 일치할 경우 + 유령의 색깔과 총알 색 일치할경우
    #print("유령과 총구가 일치, 유령의 색깔과 총알 색 일치")
    removeGhost(ghostObj)

        
#----------------------------------------------------------------------------------------
# 상점 아이템 사용 관련
def putShopItemInItemBox(shopItem): #상점에서 구매를 누른 후 구매 가능하면 해당 아이템을 빈 아이템 칸에 넣는다.
    #아이템 칸의 왼쪽부터 검사하여 빈곳이 있으면 해당자리에 아이템을 넣는다.
    for i in range(6):
        if item[i] == "None":
            item[i] = shopItem
            break


def compareClickedItemPriceToCoin(shopItemName):
    global coin
    #상점 아이템 가격
    shopItemPrice = {'WhiteBullet': 500, 'RedBullet':500, 'IncreaseTime': 1500,
                 'ReduceGhostSpeed': 1000, 'BlueBullet':500, 'PurpleBullet': 700,
                 'HealPack': 2000, 'DoubleCoin': 1500}

    if shopItemPrice[shopItemName] <= coin:
        buySound.play()
        #print("현재 코인: ", coin)
        print(shopItemName+ "구매")
        coin -= shopItemPrice[shopItemName]
        #print("남은 코인: ", coin)
        putShopItemInItemBox(shopItemName)
 
##    else:
##        print(shopItemName+"사지 못합니다.")
##
##    print(item)


def changeShopItemIndexToString(shopItemIndex):
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
            #print("이미 아이템을 가지고있으므로 살 수 없습니다")
            return True #이미 해당 아이템을 가지고 있음을 리턴
        
    return False #해당 아이템을 가지고 있지 않음을 리턴


#아이템 창이 전부 아이템으로 채워져 있는지 검사
def checkAllItemBoxIsFilled():
    global item
    
    for i in range(6):
        if item[i] == "None":
            break
        if i ==5:
            #print("아이템으로 전부 채워져있습니다.")
            return False
    return True


def checkClickPurchase(): #상점에서 아이템 구매를 클릭했는지 검사
    global clickShop
    startShopItemPos = [80, 215]
    shopItemXInterval = [0,110,230,340] #상점 아이템 간격 짧은 부분 x  
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
    global useItemDoubleCoin
    global useItemReduceGhostSpeed
    
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
    global playerHp
    global item

    if playerHp<3:
        playerHp +=1
        item[itemIndex] = "None"


def changeDCItemTimeToFalse(): #10초동안 DoubleCoin(DC)효과 지속 후 아이템 효과 끄기
    global ghostPrice
    global useItemDoubleCoin

    useItemDoubleCoin = False
    ghostPrice = 100


def makeDoubleCoin(itemIndex): #유령을 죽일 시 얻는 코인 2배 증가(10초간)
    global ghostPrice
    global useItemDoubleCoin
    
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
            #Random으로 스피드 를 만드는 함수에서도 이와같은 내용 써야 적용됨.
            #없으면 한턴만 적용됨.


def setUsingItemEffect(): #사용중인 아이템 화면 왼쪽 상단에 띄우기
    global useItemDoubleCoin
    global useItemReduceGhostSpeed

    if useItemDoubleCoin == True:
        screen.blit(imageDoubleCoinEffect,[35,5])
    if useItemReduceGhostSpeed == True:
        screen.blit(imageReduceGhostSpeedEffect,[5,5])


#-------------------------------------------------------------------------------------------
#Scene 관리
def resetGame(): #게임을 리셋한다. - isGameOver,killedGhostCnt는 제외.
    global ghostPrice
    global timeLimit
    global coin
    global resetFalseAggregation, resetTrueAggregation
    global playerHp, printEmptyHpCnt
  
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
    timeLimit = 60
    coin = 0
    playerHp = 3
    printEmptyHpCnt = 0
    
    for resetFalse in resetFalseAggregation:
        resetFalse = False
    for resetTrue in resetTrueAggregation:
        resetTrue = True


def checkGoTitleAndReplay(): #GameOver시 클릭 검사.
    global isStartScene
    global isEndScene
    global isMainScene
    global isGameOver
    global killedGhostCnt
    
    mousePos = pygame.mouse.get_pos()

    #왼쪽의 Go Title 클릭시
    if mousePos[0] >= 5 and mousePos[0] <=80:
        if mousePos[1] >=420 and mousePos[1] <= 495:
            #print("GO Title 클릭")
            isStartScene = True
            isEndScene = False
            isGameOver = False
            killedGhostCnt = 0
            return
        
    #오른쪽의 Replay 클릭시
    if mousePos[0] >= 520 and mousePos[0] <=595:
        if mousePos[1] >=420 and mousePos[1] <= 495:
            #print("Replay 클릭")
            isMainScene = True
            isEndScene = False
            isGameOver = False
            killedGhostCnt = 0
            return
            

def printEndScene():
    global killedGhostCnt
    
    screen.blit(imageGameOver, [0,0])
    screen.blit(imageGoTitle, [5,420])
    screen.blit(imageReplay, [520,420])
    
    font = pygame.font.SysFont("arial",30,True)
    killedGhostContentText = font.render("Killed Ghost :", True, RED)
    killedGhostCntText = font.render(str(killedGhostCnt), True, RED)
    
    screen.blit(killedGhostContentText, [190,5])
    screen.blit(killedGhostCntText, [360,5])


def setEndScene():
    global killedGhostCnt
    global isStartScene
    
    screen.fill(WHITE)
    
    printEndScene() #EndScene 출력
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            checkGoTitleAndReplay()
    
    mainClock.tick(60)
    pygame.display.update()
        

def fixStartSceneGhostColor():
    global haveItem
    for ghost in ghosts:
        if ghost['num'] !=3:
            ghost['moveSpeed'] = 1
    ghost1['color'] = "White"
    ghost2['color'] = "Blue"
    ghost3['color'] = "Red"
    haveItem = False #시작화면에서는 ghost4사용 x, 따라서 ghost4 안나타나게 조건 설정

def makeGhostNameAtStartScreen(): #시작화면에서 유령의 이름만들기
    font = pygame.font.SysFont("arial",20,True)
    ghost1NameText = font.render("Game Start", True, WHITE)
    ghost2NameText = font.render("Go Turtorial", True, WHITE)
    ghost3NameText = font.render("Game Exit", True, WHITE)
    
    screen.blit(ghost1NameText, [ghost1['pos'][0], ghost1['pos'][1]-15])
    screen.blit(ghost2NameText, [ghost2['pos'][0]-15, ghost2['pos'][1]-15])
    screen.blit(ghost3NameText, [ghost3['pos'][0]+5, ghost3['pos'][1]-15])

def printTitle(): #제목 출력
    font = pygame.font.SysFont("arial",50,True)
    titleText = font.render("The Ghost Hunter", True, WHITE)
    screen.blit(titleText, [125, 420])

def moveNextScene():
    global isStartScene
    global isMainScene
    global killedGhostCnt
    
    isSamePos = compareMousePosAndGhostPos(pygame.mouse.get_pos())

    if isSamePos[0] == True: #유령과 마우스 위치가 같을 경우
        shootSound.play()
        if isSamePos[1]['num'] == 0: #Game Start 일경우
            isStartScene = False
            isMainScene = True
            resetGame()
            killedGhostCnt =0
            return
##        elif isSamePos[1]['num'] == 1: #Go Turtorial 일경우
        #shootSound.play()
##            return
        elif isSamePos[1]['num'] == 2: #Game Exit 일경우
            shootSound.play()
            pygame.quit()
            sys.exit()


def setStartScene(): #시작화면
    
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


        


def setMain():
    global isMainScene
    global isGameOver
    global isEndScene
    
    if isGameOver == True:
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


#Game Loop
while True:

    while isStartScene:       
        setStartScene()
        
    while isMainScene:
        setMain()
        print(haveItem)

    while isEndScene:
        setEndScene()
