import pygame, sys #기본세팅
import random, time, threading #내가 추가한 것
from pygame.locals import *

#Set up pygame.
pygame.init()
mainClock = pygame.time.Clock()

#상수 정의
SCREENHEIGHT = 500
SCREENWIDTH = 600


imageBG = pygame.image.load("background.jpg")
imageBG = pygame.transform.scale(imageBG,(SCREENWIDTH,SCREENHEIGHT))

imageShopBG = pygame.image.load("shopBG.png")
imageShopBG = pygame.transform.scale(imageShopBG,(500, 400))

imageShopWhiteBullet = pygame.image.load("shopWhiteBullet.png")
imageShopWhiteBullet = pygame.transform.scale(imageShopWhiteBullet,(100,130))

imageShopRedBullet = pygame.image.load("shopRedBullet.png")
imageShopRedBullet = pygame.transform.scale(imageShopRedBullet,(100,130))

imageShopBlueBullet = pygame.image.load("shopBlueBullet.png")
imageShopBlueBullet = pygame.transform.scale(imageShopBlueBullet,(100,130))

imageShopPurpleBullet = pygame.image.load("shopPurpleBullet.png")
imageShopPurpleBullet = pygame.transform.scale(imageShopPurpleBullet,(100,130))

imageShopIncreaseTime = pygame.image.load("shopIncreaseTime.png")
imageShopIncreaseTime = pygame.transform.scale(imageShopIncreaseTime,(100,130))

imageShopReduceGhostSpeed = pygame.image.load("shopReduceGhostSpeed.png")
imageShopReduceGhostSpeed = pygame.transform.scale(imageShopReduceGhostSpeed,(110,130))

imageShopHealPack = pygame.image.load("shopHealPack.png")
imageShopHealPack = pygame.transform.scale(imageShopHealPack,(100,130))

imageShopDoubleCoin = pygame.image.load("shopDoubleCoin.png")
imageShopDoubleCoin = pygame.transform.scale(imageShopDoubleCoin,(100,130))

imageCoin = pygame.image.load("coin.png")
imageCoin = pygame.transform.scale(imageCoin,(25,25))

imageDoubleCoinEffect = pygame.image.load("doubleCoinEffect.png")
imageDoubleCoinEffect = pygame.transform.scale(imageDoubleCoinEffect,(25,25))

imageReduceGhostSpeedEffect = pygame.image.load("reduceGhostSpeedEffect.png")
imageReduceGhostSpeedEffect = pygame.transform.scale(imageReduceGhostSpeedEffect,(25,25))

#사운드
#구매 성공 사운드
#구매 실패 사운드


#변수
coin = 10000
GHOSTPRICE =2

item = ["WhiteBullet", "None", "None", "None", "None", "None"]



#쓰레드 관련
timeToReduceGhostSpeedOver = True 
timeToMakeDoubleCoinOver = True

useItemDoubleCoin = False


screen = pygame.display.set_mode((600,500), 0,32)
pygame.display.set_caption("The Ghost Hunter")

def setShopUI():
    startShopItemPos = [80, 215]
    shopItemXInterval = [0,110,230,340] #상점 아이템 간격 짧은 부분 x

    shopItemPos = []
    screen.blit(imageShopBG,[50,50])

    screen.blit(imageCoin,[80,80])
    screen.blit(imageShopWhiteBullet,[80,120])
    screen.blit(imageShopRedBullet,[190,120])
    screen.blit(imageShopIncreaseTime,[310,120])
    screen.blit(imageShopReduceGhostSpeed,[412,120])

    screen.blit(imageShopBlueBullet,[80,275])
    screen.blit(imageShopPurpleBullet,[190,275])
    screen.blit(imageShopHealPack,[310,275])
    screen.blit(imageShopDoubleCoin,[420,275])

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



#상점에서 구매를 누른 후 구매 가능하면 해당 아이템을 빈 아이템 칸에 넣는다.
def putShopItemInItemBox(shopItem):
    #아이템 칸의 왼쪽부터 검사하여 빈곳이 있으면 해당자리에 아이템을 넣는다.
    for i in range(6):
        if item[i] == "None":
            item[i] = shopItem
            break

def compareClickedItemPriceToCoin(shopItemName):
    #상점 아이템 가격
    #10초에 한 10마리 이상 나옴.
    global coin
    
    shopItemPrice = {'WhiteBullet': 500, 'RedBullet':500, 'IncreaseTime': 1500,
                 'ReduceGhostSpeed': 1000, 'BlueBullet':500, 'PurpleBullet': 700,
                 'HealPack': 2000, 'DoubleCoin': 1500}


    if shopItemPrice[shopItemName] <= coin:
        print("현재 코인: ", coin)
        print(shopItemName+ "구매")
        coin -= shopItemPrice[shopItemName]
        print("남은 코인: ", coin)
        putShopItemInItemBox(shopItemName)
 
    else:
        print(shopItemName+"사지 못합니다.")

    print(item)

#상점에서 아이템을 구매할때 만약 구매하고 싶은 아이템이 아이템 창에 이미 있는지 확인한다.
def checkAlreadyHaveItem(selectedShopItem):
    global item
    
    for i in range(6):
        if item[i] == selectedShopItem: #사고싶은 아이템이 이미 아이템창에 있는경우
            print("이미 아이템을 가지고있으므로 살 수 없습니다")
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

def checkClickPurchase(mousePos): #상점에서 아이템 구매를 클릭했는지 검사
    startShopItemPos = [80, 215]
    shopItemXInterval = [0,110,230,340] #상점 아이템 간격 짧은 부분 x
   
    shopItemClickBuyBool = []

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
            


#총알을 제외한 나머지 아이템 사용키 - Z
def useItemExceptBullet():
    global timeToReduceGhostSpeedOver
    global timeToMakeDoubleCoinOver
    
    for i in range(6):
        if itemPos[i][2] == True: #현재 선택한 아이템 확인
            if item[i] == "IncreaseTime":
                increaseTime()
            elif item[i] == "ReduceGhostSpeed":
                if timeToReduceGhostSpeedOver ==True:
                    timeToReduceGhostSpeedOver = False
                    reduceGhostSpeed()
            elif item[i] == "HealPack":
                healPlayerHp()
            elif item[i] == "DoubleCoin":
                if timeToMakeDoubleCoinOver == True:
                    timeToMakeDoubleCoinOver = False
                    makeDoubleCoin()

                
#아이템 동작 함수
 #시간 증가시키기
def increaseTime():
    global timeLimit

    timeLimit +=10

def changeRGSvariableToTrue():
    global timeToReduceGhostSpeedOver

    timeToReduceGhostSpeedOver = True

#아이템을 사용중이라는 것을 왼쪽 위 UI에 나타내기
#이 함수는 합치면서 작업 해야할듯 
 #유령 스피드 5 감소(7초간)
def reduceGhostSpeed():
    for ghost in ghosts:
        if ghost['num'] !=3: #좌우로 움직이는 유령일 경우
            if ghost['moveSpeed'] >=6:
                ghost['moveSpeed'] -=5
            elif ghost['moveSpeed'] <=5: #스피드가 5이하인 경우는 최저 스피드인 1로 고정
                host['moveSpeed'] =1
                
            for i in range(6):
                if item[i] == "ReduceGhostSpeed":
                    item[i] = "None"
                    threading.Timer(7, changeRGSvariableToTrue).start()
                    return
            #Random으로 스피드 를 만드는 함수에서도 이와같은 내용 써야 적용됨.
            #없으면 한턴만 적용됨.
            


#Hp 회복
def healPlayerHp():
    global playerHp
    global item

    if playerHp<3:
        playerHp +=1
        for i in range(6):
            if item[i] == "HealPack":
                item[i] = "None"


def changeDCVariableToTrue():
    global timeToMakeDoubleCoinOver
    global useItemDoubleCoin
    
    timeToMakeDoubleCoinOver = True
    useItemDoubleCoin = False

#유령을 죽일 시 얻는 코인 2배 증가
def makeDoubleCoin():
    global coin
    global useItemDoubleCoin
    
    GHOSTPRICE = 200
    useItemDoubleCoin = True
    threading.Timer(7, changeDCVariableToTrue).start()
    #10초후 원래대로 돌려놓기 
    #아이템을 사용중이라는 것을 왼쪽 위 UI에 나타내기


def setEffect(): #사용중인 아이템 화면 왼쪽 상단에 띄우기
    global useItemDoubleCoin

    if useItemDoubleCoin == True:
        screen.blit(imageDoubleCoinEffect,[35,5])
        
    screen.blit(imageReduceGhostSpeedEffect,[5,5])


    

print(item)
setShopUI()


#Game Loop
while True:
    setShopUI()
    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            #print(pygame.mouse.get_pos())
            checkClickPurchase(pygame.mouse.get_pos())
            
    checkAllItemBoxIsFilled()


    
    
    mainClock.tick(60)
    pygame.display.update()


















