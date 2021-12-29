﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using UnityEngine.EventSystems;

public class Item : MonoBehaviour
{
    public Button[] ItemCompartmentBtn = new Button[5];
    public Image[] ItemImg = new Image[6];

    int[] itemCompartmentPosX = new int[5];

    bool itemBtnBV = true; //itemBtn Bool value
    [HideInInspector]
    public string[] playerItem = new string[6]; //플레이어 아이템칸 총 6개 (사용:1 보관:5), UI에서는 우에서 좌순서이다.


    bool usingItemBtn = false;

    static public Item instance;
    private void Awake()
    {
        instance = this;

        if (SceneManager.GetActiveScene().name == "Main")
        {
            for (int i = 0; i < ItemCompartmentBtn.Length; i++)
            {
                ItemCompartmentBtn[i].gameObject.SetActive(false);
            }

            //for (int i = 0; i < playerItem.Length; i++)
            //{
            //    playerItem[i] = ItemImg[i].GetComponent<Image>().sprite.name;           
            //}

            //처음 시작은 하얀색 총알로만 시작
            //ItemImg[0].gameObject.GetComponent<Image>().sprite = Resources.Load("WhiteBullet", typeof(Sprite)) as Sprite;
            //playerItem[0] = ItemImg[0].gameObject.GetComponent<Image>().sprite.name;

            LoadItemData();
            //Debug.Log("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ");
            for (int i = 0; i < playerItem.Length; i++)
            {
                //Debug.Log(playerItem[i]);
            }

            for (int i = 0; i < ItemImg.Length; i++)
            {
                
                ItemImg[i].gameObject.GetComponent<Image>().sprite = Resources.Load(playerItem[i], typeof(Sprite)) as Sprite;
                ItemImg[i].gameObject.SetActive(false);
            }
            ItemImg[0].gameObject.SetActive(true); //사용중인 아이템 이미지만 띄우기
        }
        else if (SceneManager.GetActiveScene().name == "Shop")
        {
            for (int i = 0; i < ItemCompartmentBtn.Length; i++)
            {
                ItemCompartmentBtn[i].gameObject.SetActive(true);
            }

            LoadItemData();

            for (int i = 0; i < ItemImg.Length; i++)
            {
                ItemImg[i].gameObject.GetComponent<Image>().sprite = Resources.Load(playerItem[i], typeof(Sprite)) as Sprite;
            }
        }
          
        itemCompartmentPosX[0] = 330;
        itemCompartmentPosX[1] = 190;
        itemCompartmentPosX[2] = 50;
        itemCompartmentPosX[3] = -90;
        itemCompartmentPosX[4] = -230;
    }


    public void OpenItemCompartmentBtn() //UsingItem 버튼을 누르면 아이템 창을 연다.
    {
        if(usingItemBtn == false)
        {
            usingItemBtn = true;
            if (itemBtnBV == true)
            {
                itemBtnBV = false;
                //UI는 transform.localPosition으로 위치를 변경한다.
                StartCoroutine(OpenItemComaprtmentEffect());
            }
            else
            {
                itemBtnBV = true;
                StartCoroutine(CloseItemComaprtmentEffect());
            }
        } 
    }

    IEnumerator OpenItemComaprtmentEffect() //아이템 창을 우->좌로 열리는 효과
    {
        for (int i = 0; i < 5; i++)
        {
            ItemCompartmentBtn[i].gameObject.SetActive(true);
            ItemImg[i+1].gameObject.SetActive(true);
            while (ItemCompartmentBtn[i].transform.localPosition.x > itemCompartmentPosX[i])
            {
                ItemCompartmentBtn[i].transform.localPosition += new Vector3(-70, 0, 0);
                ItemImg[i+1].transform.localPosition += new Vector3(-70, 0, 0);
                yield return new WaitForSeconds(0.005f);
            }
        }
        usingItemBtn = false;
    }

    IEnumerator CloseItemComaprtmentEffect() //아이템 창을 좌->우로 닫히는 효과
    {
        for (int i = 4; i >= 0; i--)
        {
            while (ItemCompartmentBtn[i].transform.localPosition.x < itemCompartmentPosX[i] + 140)
            {
                ItemCompartmentBtn[i].transform.localPosition += new Vector3(+70, 0, 0);
                ItemImg[i + 1].transform.localPosition += new Vector3(+70, 0, 0);
                yield return new WaitForSeconds(0.005f);
            }
            ItemCompartmentBtn[i].gameObject.SetActive(false);
            ItemImg[i+1].gameObject.SetActive(false);
        }
        usingItemBtn = false;
    }


    public int ChangeItemStringToInt(string itemName)
    {
        int colorNum;

        switch(itemName)
        {
            case "WhiteBullet":
                colorNum = 0;
                break;
            case "RedBullet":
                colorNum = 1;
                break;
            case "BuleBullet":
                colorNum = 2;
                break;
            default:
                colorNum = -1; 
                break;
        }
        return colorNum;
    }

    public void ExchangeItem() // 아이템 칸을 누를시 사용중인 아이템과 해당 칸의 아이템을 교환한다.
    {
        GameObject clickedBtn = EventSystem.current.currentSelectedGameObject;
        Sprite tmpSprite;
        string tmpItemName;

        if (usingItemBtn == false)
        {        
            //Debug.Log(clickedBtn.name);
            for(int i=0; i<5; i++)
            {
                if(clickedBtn.name.Contains((i+1).ToString())) //1,2,3,4,5
                {
                    Debug.Log("클릭한 버튼 :" + (i+1));
                    //Debug.Log(clickedBtn.GetComponent<Image>().sprite);
                    tmpSprite = ItemImg[i + 1].GetComponent<Image>().sprite;
                    ItemImg[i+1].GetComponent<Image>().sprite = ItemImg[0].sprite;
                    ItemImg[0].gameObject.GetComponent<Image>().sprite = tmpSprite;

                    tmpItemName = playerItem[i+1];
                    playerItem[i + 1] = playerItem[0];
                    playerItem[0] = tmpItemName;
                }           
            }
        }
    }

    public void OpneShop()
    {
        //모든 데이터 Shop 이동 전에 저장하기
        Player.instance.SaveHpData();
        TimeController.instance.SaveTimeData();
        GameManager.instance.SaveGameData();
        SaveItemData();

        SceneManager.LoadScene("Shop");     
    }

    public void SaveItemData()
    {
        for (int i = 0; i < playerItem.Length; i++)
        {
            //playerItem을 Item[i]에 저장
            //Item0 Item1 Item2 Item3 Item4 Item5
            PlayerPrefs.SetString("Item" + i.ToString(), playerItem[i]);
            //Debug.Log("(playerItem)item[" + i + "] : " + playerItem[i]);
            //Debug.Log("(playerprefs)item[" + i + "] : " + PlayerPrefs.GetString("Item" + i.ToString()));
        }
        PlayerPrefs.Save();
    }

    void LoadItemData()
    {
        for (int i = 0; i < playerItem.Length; i++)
        {
            if (!PlayerPrefs.HasKey("Item" + i.ToString())) //Item0 Item1 Item2 Item3 Item4 Item5 
            {
                playerItem[i] = PlayerPrefs.GetString("Item" + i.ToString(), ItemImg[i].GetComponent<Image>().sprite.name);
            }
            else
            {
                playerItem[i] = PlayerPrefs.GetString("Item" + i.ToString());
            }        
        }
    }

    }//End Class
