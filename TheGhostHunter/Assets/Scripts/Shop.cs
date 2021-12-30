using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using UnityEngine.SceneManagement;


public class Shop : MonoBehaviour
{
    public Text CoinText;

    [HideInInspector]
    public int coin = 10000;

    string[,] shopItem = new string[6,2];
    // 구매할 아이템 이름 / 가격

    static public Shop instance;
    private void Awake()
    {
        instance = this;

        for(int row =0; row<6; row++)
        {
            for (int col = 0; col < 2; col++)
            {
                if(col ==1)
                {
                    shopItem[row, col] = "500";
                }
                else
                {
                    shopItem[row, col] = "";
                }               
            }
        }
        
        shopItem[0,0] = "WhiteBullet";
        shopItem[1,0] = "RedBullet";
        shopItem[2,0] = "BlueBullet";
        shopItem[3,0] = "PurpleBullet";
    }

    private void Update()
    {
        if (SceneManager.GetActiveScene().name == "Shop")
        {
            CoinText.text = coin.ToString();
        }
        //Debug.Log("Shop Time Data : " + PlayerPrefs.GetFloat("Time"));
    }

    public void CloseShop()
    {
        Item.instance.SaveItemData();
        SceneManager.LoadScene("Main");
    }


    public void BuyItem()
    {
        GameObject clickedBtn = EventSystem.current.currentSelectedGameObject;
        
        for(int i=0; i<6; i++)
        {
            if(clickedBtn.name.Contains((i+1).ToString()))
            {
                if(int.Parse(shopItem[i,1]) <= coin)
                {
                    for(int a=5; a >=0; a--)
                    {
                        if(Item.instance.playerItem[a] == "empty")
                        {
                            if (shopItem[i, 0] == "")
                                continue;

                            coin -= int.Parse(shopItem[i, 1]); //코인 차감

                            //구매한 아이템을 아이템 창에 왼쪽부터 채우기
                            Item.instance.playerItem[a] = shopItem[i, 0];
                            Item.instance.ItemImg[a].sprite = Resources.Load(shopItem[i,0], typeof(Sprite)) as Sprite;
                            break;
                        }
                    }                   
                }
            }
        }
    }
}//End Class
