using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using UnityEngine.SceneManagement;


public class Shop : MonoBehaviour
{
    //coin text
    public Text CoinText;

    //이전, 다음 페이지 이동 버튼
    public GameObject NextPageBtn;
    public GameObject PreviousPageBtn;

    //구매 가격 버튼
    public Text[] ItemPriceTxt = new Text[6];

    int page = 0;

    string[,,] shopItem = new string[2,6,2];
    // [구매할 아이템 이름 , 가격]


    //아이템 칸 위치
    Vector3[] itemPos = new Vector3[6];

    GameObject ClickedItem = null;

    bool isCliked = false;

    static public Shop instance;
    private void Awake()
    {
        instance = this;
       
        //for (int row =0; row<6; row++)
        //{
        //    for (int col = 0; col < 2; col++)
        //    {
        //        if(col ==1)
        //        {
        //            shopItem[row, col] = "300";
        //        }
        //        else
        //        {
        //            shopItem[row, col] = "empty";
        //        }
        //    }
        //}

        shopItem[0, 0, 0] = "WhiteWool";
        shopItem[0, 1, 0] = "RedWool";
        shopItem[0, 2, 0] = "BlueWool";
        shopItem[0, 3, 0] = "PurpleWool";
        shopItem[0, 4, 0] = "BlackWool";
        shopItem[0, 5, 0] = "YellowMouseWool";

        shopItem[0, 0, 1] = "300";
        shopItem[0, 1, 1] = "300";
        shopItem[0, 2, 1] = "300";
        shopItem[0, 3, 1] = "500";
        shopItem[0, 4, 1] = "500";
        shopItem[0, 5, 1] = "500";

        shopItem[1, 0, 0] = "ReduceGhostSpeed";
        shopItem[1, 1, 0] = "IncreaseTime";
        shopItem[1, 2, 0] = "HealPack";
        shopItem[1, 3, 0] = "DoubleCoin";
        shopItem[1, 4, 0] = "empty";
        shopItem[1, 5, 0] = "empty";

        shopItem[1, 0, 1] = "300";
        shopItem[1, 1, 1] = "300";
        shopItem[1, 2, 1] = "500";
        shopItem[1, 3, 1] = "300";
        shopItem[1, 4, 1] = "";
        shopItem[1, 5, 1] = "";

        for (int i =0; i< ItemPriceTxt.Length; i++)
        {
            ItemPriceTxt[i].text = shopItem[0, i, 1];
        }
       
        PreviousPageBtn.SetActive(false);
        NextPageBtn.SetActive(true);

        for (int i = 0; i < itemPos.Length; i++)
        {
            itemPos[i] = new Vector3(450 - (130 * i), -870, 0);
        }
    }

    private void Update()
    {
        if (SceneManager.GetActiveScene().name == "Shop")
        {
            CoinText.text = Item.instance.coin.ToString();

            SelectItem();
            MoveClickedItem();
        }
    }

    //Open Shop은 Item Class에서 진행
    public void CloseShop()
    {
        Item.instance.SaveItemData();
        Item.instance.SaveCoinData();
        Item.instance.SaveUsingItemRGSData();
        Item.instance.SaveUsingItemIGPData();
        SceneManager.LoadScene("Main");
    }


    public void BuyItem()
    {
        GameObject clickedBtn = EventSystem.current.currentSelectedGameObject.transform.GetChild(0).gameObject;
        
        for(int i=0; i<6; i++) //버튼 인덱스 검사
        {
            if(clickedBtn.name.Contains((i+1).ToString()))
            {
                if (CheckSameItem(shopItem[page, i, 0]) == true)
                {
                    Debug.Log("똑같은 아이템이 이미 있습니다. ");
                    break;
                }
                  

                if(int.Parse(shopItem[page, i, 1]) <= Item.instance.coin)
                {
                    for(int a=0; a <6; a++)
                    {
                        if(Item.instance.playerItem[a] == "empty") //플레이어가 가지고 있는 아이템 창이 비어있을 경우
                        {
                            if (shopItem[page, i, 0] == "empty") //구매하고자 하는 아이템이 비어있다면 구매 x
                                continue;

                            //총알이 아닌 다른 아이템은 item칸에 제일 앞칸(사용중인 총알)에 들어가지 않게 함.
                            if (!shopItem[page, i, 0].Contains("Wool") && a == 0) 
                                continue;

                            Item.instance.coin -= int.Parse(shopItem[page, i, 1]); //코인 차감

                            //구매한 아이템을 아이템 창에 오른쪽부터 채우기
                            Item.instance.playerItem[a] = shopItem[page, i, 0];
                            Item.instance.ItemImg[a].sprite = Resources.Load<Sprite>("Item/"+shopItem[page, i, 0]);
                            break;
                        }
                    }                   
                }
            }
        }
    }


    void ChangeShopItem()
    {
        for (int i = 0; i < ItemPriceTxt.Length; i++)
        {
            ItemPriceTxt[i].text = shopItem[page, i, 1];
            GameObject.Find("BuyItemImg"+(i+1).ToString()).GetComponent<Image>().sprite = Resources.Load<Sprite>("Item/" + shopItem[page, i, 0]);
        }
    }

    bool CheckSameItem(string itemNameIWantToBuy)
    {
        for(int i=0; i<6; i++)
        {
            if(Item.instance.playerItem[i] == itemNameIWantToBuy)
            {
                return true;
            }
        }
        return false;
    }

    public void moveNextPage()
    {
        if(page == 0)
        {
            PreviousPageBtn.SetActive(true);
            NextPageBtn.SetActive(false);
            ++page;
            ChangeShopItem();
        }
    }

    public void movePreviousPage()
    {
        if (page == 1)
        {
            PreviousPageBtn.SetActive(false);
            NextPageBtn.SetActive(true);
            --page;
            ChangeShopItem();
        }
    }


    // 상점에서의 Item

    //아이템을 되팔기하는 기능
    // <아이템을 드래그 앤 드롭>
    //  - 클릭한 아이템은 클릭한 버튼의 번호를 이용하여 정보를 얻는다.
    //  - 해당 이미지를 드래그가 끝날때까지 마우스의 위치로 이동시킨다.
    //  - 드래그가 끝났을 때 휴지통의 위치라면 되팔기 + 아이템 없애기
    //  - 드래그가 끝났을 때 휴지통의 위치가 아니라면 원래 아이템의 위치로 되돌리기

    void SelectItem()
    {
        if (isCliked)
            return;

        for (int i = 0; i < itemPos.Length; i++)
        {
            if (Input.mousePosition.x - 540 >= itemPos[i].x - 50 && Input.mousePosition.x - 540 <= itemPos[i].x + 50)
            {
                if (Input.mousePosition.y - 960 >= itemPos[i].y - 60 && Input.mousePosition.y - 960 <= itemPos[i].y + 60)
                {
                    // 현재 마우스가 아이템 칸에 있다는 뜻
                    //Debug.Log(i +" : " + (Input.mousePosition + new Vector3(-540, -960, 0)));
                    if (Input.GetMouseButtonDown(0) && GameObject.Find("itemImg" + i.ToString()).GetComponent<Image>().sprite.name != "empty")
                    {
                        ClickedItem = GameObject.Find("itemImg" + i.ToString());
                        isCliked = true;
                        Debug.Log("마우스 누르는 중 ");
                        break;                    }
                   
                }
            }
        }
    }

    void MoveClickedItem()
    {
        if (isCliked == false)
            return;

        ClickedItem.transform.position = Input.mousePosition;

        if (Input.GetMouseButtonUp(0))
        {
            
            Debug.Log("마우스 뗌 ");
            if(Input.mousePosition.x - 540 >= -50 && Input.mousePosition.x -540 <=  50)
            {
                if(Input.mousePosition.y - 960 >= -600 - 50 && Input.mousePosition.y - 960 <= -600 + 50)
                {
                    // 드래그한 아이템이 쓰레기통에 위치한 채 마우스에서 손을 떼었을 경우

                    //해당 아이템 원래 가격 - 200의 돈을 Money에 넣어준다.
                    Item.instance.coin += ReturnClickedItemPrice(ClickedItem.GetComponent<Image>().sprite.name) - 200; //원래 아이템 가격 - 200
                    Item.instance.playerItem[int.Parse(ClickedItem.name.Split('g')[1])] = "empty";
                    // 해당 아이템 빈칸으로
                    ClickedItem.GetComponent<Image>().sprite = Resources.Load<Sprite>("Item/empty");
                }
            }  

            ClickedItem.transform.localPosition = itemPos[int.Parse(ClickedItem.name.Split('g')[1])];
            ClickedItem = null;
            isCliked = false;
        }
    }

    int ReturnClickedItemPrice(string clickedItemName) //아이템을 되팔기할 때 해당 아이템 가격을 리턴한다.
    {
        for(int a=0; a<shopItem.GetLength(0); a++)
        {
            for (int b = 0; b < shopItem.GetLength(1); b++)
            {
                if (shopItem[a, b, 0] == clickedItemName)
                {
                    //Debug.Log("클릭한 아이템 가격" + shopItem[a, b, 1]);
                    return int.Parse(shopItem[a, b, 1]);
                }
            }
        }

        return 0;
    }

}//End Class
