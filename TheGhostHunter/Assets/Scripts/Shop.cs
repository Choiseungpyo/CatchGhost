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

    int page = 1;

    string[,] shopItem = new string[6,2];
    // [구매할 아이템 이름 , 가격]

   

    static public Shop instance;
    private void Awake()
    {
        instance = this;
       
        for (int row =0; row<6; row++)
        {
            for (int col = 0; col < 2; col++)
            {
                if(col ==1)
                {
                    shopItem[row, col] = "500";
                }
                else
                {
                    shopItem[row, col] = "empty";
                }               
            }
        }
        
        shopItem[0,0] = "WhiteBullet";
        shopItem[1,0] = "RedBullet";
        shopItem[2,0] = "BlueBullet";
        shopItem[3,0] = "PurpleBullet";
        shopItem[3, 1] = "700";

        PreviousPageBtn.SetActive(false);
        NextPageBtn.SetActive(true);
    }

    private void Update()
    {
        if (SceneManager.GetActiveScene().name == "Shop")
        {
            CoinText.text = Item.instance.coin.ToString();
        }
        //Debug.Log("Shop Time Data : " + PlayerPrefs.GetFloat("Time"));
    }

    //Open Shop은 Item Class에서 진행
    public void CloseShop()
    {
        Item.instance.SaveItemData();
        Item.instance.SaveCoinData();
        Item.instance.SaveUsingItemRGSData();
        SceneManager.LoadScene("Main");
    }


    public void BuyItem()
    {
        GameObject clickedBtn = EventSystem.current.currentSelectedGameObject;
        
        for(int i=0; i<6; i++)
        {
            if(clickedBtn.name.Contains((i+1).ToString()))
            {
                if(int.Parse(shopItem[i,1]) <= Item.instance.coin)
                {
                    for(int a=0; a <6; a++)
                    {
                        if(Item.instance.playerItem[a] == "empty")
                        {
                            if (shopItem[i, 0] == "empty")
                                continue;

                            Item.instance.coin -= int.Parse(shopItem[i, 1]); //코인 차감

                            //구매한 아이템을 아이템 창에 오른쪽부터 채우기
                            Item.instance.playerItem[a] = shopItem[i, 0];
                            Item.instance.ItemImg[a].sprite = Resources.Load(shopItem[i,0], typeof(Sprite)) as Sprite;
                            break;
                        }
                    }                   
                }
            }
        }
    }


    void ChangeShopItem()
    {
        //페이지를 넘길때 아이템목록과 가격들을 바꾼다.
        if(page == 1)
        {    
            shopItem[0, 0] = "WhiteBullet";
            shopItem[1, 0] = "RedBullet";
            shopItem[2, 0] = "BlueBullet";
            shopItem[3, 0] = "PurpleBullet";
            
            shopItem[0, 1] = "500";
            shopItem[1, 1] = "500";
            shopItem[2, 1] = "500";
            shopItem[3, 1] = "700";
        }
        else if(page == 2)
        {
            shopItem[0, 0] = "ReduceGhostSpeed";
            shopItem[1, 0] = "IncreaseTime";
            shopItem[2, 0] = "HealPack";
            shopItem[3, 0] = "DoubleCoin";

            shopItem[0, 1] = "500";
            shopItem[1, 1] = "500";
            shopItem[2, 1] = "700";
            shopItem[3, 1] = "500";
        }

        for (int i = 0; i < ItemPriceTxt.Length; i++)
        {
            ItemPriceTxt[i].text = shopItem[i, 1];
            GameObject.Find("BuyItemImg"+(i+1).ToString()).GetComponent<Image>().sprite 
            = Resources.Load(shopItem[i,0], typeof(Sprite)) as Sprite;
        }
    }

    public void moveNextPage()
    {
        if(page == 1)
        {
            PreviousPageBtn.SetActive(true);
            NextPageBtn.SetActive(false);
            ++page;
            ChangeShopItem();
        }
    }

    public void movePreviousPage()
    {
        if (page == 2)
        {
            PreviousPageBtn.SetActive(false);
            NextPageBtn.SetActive(true);
            --page;
            ChangeShopItem();
        }
    }
}//End Class
