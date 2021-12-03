import pygame, sys #기본세팅
import random, time, threading #내가 추가한 것
from pygame.locals import *

#Set up pygame.
pygame.init()
mainClock = pygame.time.Clock()

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

GHOSTPRICE = 100

#변수 정의
 #플레이어의 Hp
playerHp = 3

 #아이템 창 itemPos = [x좌표, y좌표, 해당 아이템 번호를 눌렀는지]
itemPos =[]
for i in range(6):
    itemPos.append([150+55*i,440, False])
itemPos[0][2] = True

item = ["WhiteBullet", "RedBullet", "BlueBullet", "PurpleBullet", "None", "None"] 

 #유령 
ghost1 = {'num': 0, 'pos': pygame.Rect(-50,75,75,75), 'dir':"RIGHT", 'moveSpeed': 10, 'color': "White"} 
ghost2 = {'num': 1, 'pos': pygame.Rect(SCREENWIDTH,185,75,75), 'dir':"LEFT", 'moveSpeed': 10, 'color': "White"}
ghost3 = {'num': 2, 'pos': pygame.Rect(-50,295,75,75), 'dir':"RIGHT", 'moveSpeed': 10, 'color': "White"}
ghost4 = {'num': 3, 'pos': pygame.Rect(SCREENWIDTH/2,SCREENHEIGHT +100, 75, 45), 'color': "Purple", 'currentItemBoxIndex': "None"}
ghosts = [ghost1,ghost2,ghost3, ghost4]


killGhost4Bool = False

 #상점 
clickShop = False
shopPos = pygame.Rect(550,450,40,40)
isAvailableTimeForShop = True #상점은 들어갔다 나온 후 5초이후부터 이용가능하다.


 #제한시간
timeLimit = 100
printTime0 = False

 #쓰레드를 제어하기 위한 변수
isChangingTime = True #시간 


 #Hp
printEmptyHpCnt = 0
 
 #게임오버
isGameOver = False

 #아이템창에 아이템이 있는지를 확인하는 변수
haveItem = True

 #돈
coin = 0

 #ghost4
isSettingGhost4 = True
alreadyWorking = False #스레드에서 시간 차이로 인한 오류가 생기므로 해당 함수가 끝난 후 동작할 수 있도록 함.
 


#이미지
 #배경
imageBG = pygame.image.load("background.jpg")
imageBG = pygame.transform.scale(imageBG,(SCREENWIDTH,SCREENHEIGHT))

 #유령
imageWhiteGhostL = pygame.image.load("left_WhiteGhost.png")
imageWhiteGhostL = pygame.transform.scale(imageWhiteGhostL,(75,75))
imageWhiteGhostR = pygame.image.load("right_WhiteGhost.png")
imageWhiteGhostR = pygame.transform.scale(imageWhiteGhostR,(75,75))

imageRedGhostL = pygame.image.load("left_RedGhost.png")
imageRedGhostL = pygame.transform.scale(imageRedGhostL,(75,75))
imageRedGhostR = pygame.image.load("right_RedGhost.png")
imageRedGhostR = pygame.transform.scale(imageRedGhostR,(75,75))

imageBlueGhostL = pygame.image.load("left_BlueGhost.png")
imageBlueGhostL = pygame.transform.scale(imageBlueGhostL,(75,75))
imageBlueGhostR = pygame.image.load("right_BlueGhost.png")
imageBlueGhostR = pygame.transform.scale(imageBlueGhostR,(75,75))

imagePurpleGhost = pygame.image.load("purpleGhost.png")
imagePurpleGhost = pygame.transform.scale(imagePurpleGhost,(75,75))

#총구
imageGunPoint = pygame.image.load("gunPoint.png")
imageGunPoint = pygame.transform.scale(imageGunPoint,(75,75))

 #총알
imageWhiteBullet = pygame.image.load("whiteBullet.png")
imageWhiteBullet = pygame.transform.scale(imageWhiteBullet,(50,50))

imageRedBullet = pygame.image.load("redBullet.png")
imageRedBullet = pygame.transform.scale(imageRedBullet,(50,50))

imageBlueBullet = pygame.image.load("blueBullet.png")
imageBlueBullet = pygame.transform.scale(imageBlueBullet,(50,50))

imagePurpleBullet = pygame.image.load("purpleBullet.png")
imagePurpleBullet = pygame.transform.scale(imagePurpleBullet,(50,50))

 #플레이어 Hp
imagePlayerFullHp = pygame.image.load("playerFullHp.png")
imagePlayerFullHp = pygame.transform.scale(imagePlayerFullHp,(35,35))

imagePlayerEmptyHp = pygame.image.load("playerEmptyHp.png")
imagePlayerEmptyHp = pygame.transform.scale(imagePlayerEmptyHp,(35,35))

 #상점
# 투명화 imageBG.set_alpha(100)
imageShopIcon = pygame.image.load("shopIcon.png")
imageShopIcon = pygame.transform.scale(imageShopIcon,(shopPos.width,shopPos.height))
   
imageShopUI = pygame.image.load("shopUI.png")
imageShopUI = pygame.transform.scale(imageShopUI,(500, 400))
##imageShopUI.set_alpha(200)

 #돈
imageCoin = pygame.image.load("coin.png")
imageCoin = pygame.transform.scale(imageCoin,(25, 25))



#화면
screen = pygame.display.set_mode((600,500), 0,32)
pygame.display.set_caption("The Ghost Hunter")

#화면 세팅
screen.fill(WHITE)


def checkIsNoHp(): #체력이 없는지 확인한다.
    global playerHp
    global isGameOver
    
    if playerHp <= 0 and printEmptyHpCnt ==3: #0보다 작다고 하면 Hp를 전부 감소시키지 않은상태에서 끝난다.
         print("체력이 없어 게임종료")
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


#UI 세팅
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
        print("시간 끝")
        
        

def setShopUI():
    global clickShop
    global isAvailableTimeForShop

    if isAvailableTimeForShop == True:
        screen.blit(imageShopIcon,[shopPos.left, shopPos.top])

        if clickShop == True:
            screen.blit(imageShopUI,[50,50])
        



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
        if event.key >= NUM1 and event.key <= NUM6:
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
                print("haveItem 을 False로 바꿈")
                ghost4['currentItemBoxIndex'] = "None"
                print("아이템을 하나도 갖고있지 않습니다.")
        else:
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
    randTime = random.randrange(3,5) #3~10

    return randTime





#ghost 1~3
#--------------------------------------------------------------------------------------------
def setRandomMovingSpeed(): #유령의 이동속도를 랜덤으로 정한다.
    randMoveSpeed = random.randrange(1, 16) #속도 : 1~15 
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
        print("ghost4를 죽였습니다.")
        
    coin += GHOSTPRICE


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


def manageAfterShooting():
    global playerHp
    global clickShop

    if clickShop == True: #상점이 열려있는 경우에는 화면상에 있는 유령을 제거하지 못하게 한다.
        return
    
    ghostObj = compareMousePosAndGhostPos(pygame.mouse.get_pos())[1]
     #유령이랑 총구위치 이 일치하는지 확인
    if compareMousePosAndGhostPos(pygame.mouse.get_pos())[0] == False:
        #print("유령과 총구가 불일치")
        return
    
    if checkCurrentBulletAndGhostColor(ghostObj) == False: #총구와 유령은 일치하나 총알과 유령의 색이 다를경우
        #print("유령과 총구가 일치, 유령의 색깔과 총알 색 불일치")
        playerHp -=1
        return
    
    #유령과 총구가 일치할 경우 + 유령의 색깔과 총알 색 일치할경우
    #print("유령과 총구가 일치, 유령의 색깔과 총알 색 일치")
    removeGhost(ghostObj)
        





##
##setHpUI()
##setItemUI()
##setTimeUI()
##moveGhost()
##setShopUI()



#Game Loop
while True:
    if isGameOver == True:
        print("GameOver")
        time.sleep(5) #5초뒤 종료
        pygame.quit()

    screen.fill(WHITE)
    setBackground()
    setHpUI()
    moveGhost()
    setItemUI()
    setTimeUI()
    setShopUI()

   
    
    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            checkInput(event.key)
        if event.type == pygame.MOUSEBUTTONUP:
            manageAfterShooting()
            compareMousePosAndShopPos()
            
    makeMousePosLookLikeGun()
    mainClock.tick(60)
    pygame.display.update()
    checkIsNoHp()
