using System.Collections;
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

    [HideInInspector]
    public bool itemBtnBV = true; //itemBtn Bool value
    [HideInInspector]
    public string[] playerItem = new string[6]; //플레이어 아이템칸 총 6개 (사용:1 보관:5), UI에서는 우에서 좌순서이다.

    bool usingItemBtn = false;

    //총알을 제외한 아이템 사용 관련
    static int usingItemIndex;

    Vector4 orangeColor = new Vector4(1, 180f / 255, 0, 1);

    //Reduce Ghost Speed
    [HideInInspector]
    public  bool usingItemRGS = false;
    static float timeToUseRGS = 7; //Scene 이동시에도 아이템 사용시간은 흘러가게 만들기 위해 static 이용
    static int usingItemRGSIndex;

    //Increase Ghost Price
    [HideInInspector]
    public bool usingItemIGP= false;
    static float timeToUseIGP = 10; //Scene 이동시에도 아이템 사용시간은 흘러가게 만들기 위해 static 이용
    static int usingItemIGPIndex;

    //Shop Class에서 선언하고 사용하려했지만 데이터 저장때문에 여기서 선언
    [HideInInspector]
    public int coin = 0;

    //Purple Ghost와 아이템 창 여는것 관련
    bool controlPurpleGhostAndItem = true;



    static public Item instance;
    private void Awake()
    {
        instance = this;
        LoadCoinData();
        LoadUsingItemRGSData();
        LoadUsingItemIGPData();
        if (SceneManager.GetActiveScene().name == "Main")
        {
            if(usingItemRGS == true)
            {
                GameObject.Find("ItemBtn" + usingItemRGSIndex).GetComponent<Image>().color = orangeColor;
            }

            if(usingItemIGP == true)
            {
                GameObject.Find("ItemBtn" + usingItemIGPIndex).GetComponent<Image>().color = orangeColor;
            }

            for (int i = 0; i < ItemCompartmentBtn.Length; i++)
            {
                ItemCompartmentBtn[i].gameObject.SetActive(false);
            }

            LoadItemData();

            for (int i = 0; i < ItemImg.Length; i++)
            {           
                ItemImg[i].gameObject.GetComponent<Image>().sprite = Resources.Load<Sprite>("Item/"+playerItem[i]);
                ItemImg[i].gameObject.SetActive(false);
            }
            ItemImg[0].gameObject.SetActive(true); //사용중인 아이템 이미지만 띄우기
        }
        else if (SceneManager.GetActiveScene().name == "Shop")
        {
            if(usingItemRGS == true)
            {
                GameObject.Find("ItemBtn" + usingItemRGSIndex).GetComponent<Image>().color = orangeColor;
            }

            if (usingItemIGP == true)
            {
                GameObject.Find("ItemBtn" + usingItemIGPIndex).GetComponent<Image>().color = orangeColor;
            }


            for (int i = 0; i < ItemCompartmentBtn.Length; i++)
            {
                ItemCompartmentBtn[i].gameObject.SetActive(true);
            }

            LoadItemData();

            for (int i = 0; i < ItemImg.Length; i++)
            {
                ItemImg[i].gameObject.GetComponent<Image>().sprite = Resources.Load<Sprite>("Item/"+playerItem[i]);
            }
        }

        itemCompartmentPosX[0] = 320;
        itemCompartmentPosX[1] = 190;
        itemCompartmentPosX[2] = 60;
        itemCompartmentPosX[3] = -70;
        itemCompartmentPosX[4] = -200;

      
    }

    private void Update()
    {
        CalculateTimeToRGS();
        CalculateTimeToIGP();
        OpenItemWhenPurpleGhostStateIsFind();
    }

    public void OpenItemCompartmentBtn() //UsingItem 버튼을 누르면 아이템 창을 연다.
    {
        if(usingItemBtn == false)
        {
            usingItemBtn = true;
            if (itemBtnBV == true) //아이템 창 열기
            {
                itemBtnBV = false;
                //UI는 transform.localPosition으로 위치를 변경한다.
                StartCoroutine(OpenItemComaprtmentEffect());
            }           
            else if (itemBtnBV == false)
            {
                if(Ghost.instance.PurpleGhostObj.transform.position.x >= 3.25 || Ghost.instance.PurpleGhostObj.transform.position.y > -4.05f)
                {
                    itemBtnBV = true;
                    StartCoroutine(CloseItemComaprtmentEffect());
                }
                else
                {
                    usingItemBtn = false;
                }
            }
        }
    }

    //나중에 플레이어 코루틴처럼 바꿔서 더 자연스럽게 열리도록 하기
    IEnumerator OpenItemComaprtmentEffect() //아이템 창을 우->좌로 열리는 효과
    {
        float elapsedTime = 0;
        float timeToMove = 0.1f;

        for (int i = 0; i < 5; i++)
        {
            elapsedTime = 0;
            ItemCompartmentBtn[i].gameObject.SetActive(true);
            ItemImg[i+1].gameObject.SetActive(true);
            while (elapsedTime < timeToMove)
            {
                ItemCompartmentBtn[i].transform.localPosition = Vector3.Lerp(ItemCompartmentBtn[i].transform.localPosition,
                                                   new Vector3(itemCompartmentPosX[i],-870,0),
                                                  (elapsedTime / timeToMove));

                ItemImg[i + 1].transform.localPosition = Vector3.Lerp(ItemImg[i + 1].transform.localPosition,
                                                   new Vector3(itemCompartmentPosX[i], -870, 0),
                                                  (elapsedTime / timeToMove));

                elapsedTime += Time.deltaTime;
                yield return null;
            }
            ItemCompartmentBtn[i].transform.localPosition = new Vector3(itemCompartmentPosX[i], -870, 0);
            ItemImg[i + 1].transform.localPosition = new Vector3(itemCompartmentPosX[i], -870, 0);
        }
        usingItemBtn = false;
        controlPurpleGhostAndItem = true;
    }

    IEnumerator CloseItemComaprtmentEffect() //아이템 창을 좌->우로 닫히는 효과
    {
        float elapsedTime = 0;
        float timeToMove = 0.1f;

        for (int i = 4; i >= 0; i--)
        {
            elapsedTime = 0;

            while (elapsedTime < timeToMove)
            {
                ItemCompartmentBtn[i].transform.localPosition = Vector3.Lerp(ItemCompartmentBtn[i].transform.localPosition,
                                                   new Vector3(itemCompartmentPosX[i] + 130, -870, 0),
                                                  (elapsedTime / timeToMove));

                ItemImg[i + 1].transform.localPosition = Vector3.Lerp(ItemImg[i + 1].transform.localPosition,
                                                   new Vector3(itemCompartmentPosX[i] + 130, -870, 0),
                                                  (elapsedTime / timeToMove));

                elapsedTime += Time.deltaTime;
                yield return null;
            }

            ItemCompartmentBtn[i].transform.localPosition = new Vector3(itemCompartmentPosX[i] + 130, -870, 0);
            ItemImg[i + 1].transform.localPosition = new Vector3(itemCompartmentPosX[i] + 130, -870, 0);

            ItemCompartmentBtn[i].gameObject.SetActive(false);
            ItemImg[i + 1].gameObject.SetActive(false);
        }
        usingItemBtn = false;
    }


    public int ChangeItemStringToInt(string itemName)
    {
        int colorNum;

        switch(itemName)
        {
            case "WhiteWool":
                colorNum = 0;
                break;
            case "RedWool":
                colorNum = 1;
                break;
            case "BlueWool":
                colorNum = 2;
                break;
            case "PurpleWool":
                colorNum = 3;
                break;
            case "BlackWool":
                colorNum = 4;
                break;
            case "YellowMouseWool":
                colorNum = 5;
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
            for(int i=0; i<5; i++)
            {
                if(clickedBtn.name.Contains((i+1).ToString())) //1,2,3,4,5
                {
                    //총알인 아이템과만 바뀌도록.
                    if (ItemImg[i + 1].GetComponent<Image>().sprite.name.Contains("Wool"))
                    {
                        //사운드
                        SoundManager.instance.PlaySound(SoundManager.instance.SelectSound("Click"));

                        //Debug.Log("아이템이 바뀌었습니다.");
                        tmpSprite = ItemImg[i + 1].GetComponent<Image>().sprite;
                        ItemImg[i + 1].GetComponent<Image>().sprite = ItemImg[0].sprite;
                        ItemImg[0].gameObject.GetComponent<Image>().sprite = tmpSprite;

                        tmpItemName = playerItem[i + 1];
                        playerItem[i + 1] = playerItem[0];
                        playerItem[0] = tmpItemName;
                    }            
                }           
            }
        }
    }

    //보라색 유령 Find가 되는 순간 아이템 창을 열어 놓는다.
    void OpenItemWhenPurpleGhostStateIsFind()
    {
        if(Ghost.instance.purpleGhostState == Ghost.PurpleGhostState.Find && controlPurpleGhostAndItem == true)
        {
            if (usingItemBtn == false && itemBtnBV == true)
            {
                if(Ghost.instance.purpleGhostPosIndex != 0) //사용중인 아이템을 보라색 유령이 가져가려고 하는 것이라면 아이템창이 열리지 않도록 한다.
                {                   
                    Debug.Log("보라색 유령이 아이템을 훔쳐가려고 아이템 창을 열었다.");
                    controlPurpleGhostAndItem = false;
                    usingItemBtn = true;
                    StartCoroutine(OpenItemComaprtmentEffect());
                    itemBtnBV = false;
                }
            }     
        }
    }
   

    //ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    //아이템 동작 함수(1.유령 스피드 감소 2.시간 증가 3.힐팩 4.더블 코인)
    void ReduceGhostSpeed() //7초동안 유령의 스피드를 낮춤.
    {
        Debug.Log("Reduce Ghost Speed 사용");
        usingItemRGS = true;
    }

    void CalculateTimeToRGS()
    {
        if (usingItemRGS == true)
        {
            timeToUseRGS -= Time.deltaTime;

            if (timeToUseRGS <= 0)
            {
                usingItemRGS = false;
                timeToUseRGS = 7;
                ItemImg[usingItemRGSIndex].sprite = Resources.Load<Sprite>("Item/empty");
                playerItem[usingItemRGSIndex] = "empty";
                GameObject.Find("ItemBtn" + usingItemRGSIndex).GetComponent<Image>().color = Color.white;
                Debug.Log("Ruduce Ghost Price 사용 종료");
            }
        }
        else
        {
            timeToUseRGS = 7;
        }
        //Debug.Log("RGS Time :" + timeToUseRGS);
    }
    void IncreaseTime()
    {
        Debug.Log("Increase Time");
        TimeController.instance.limitTime += 10;
        ItemImg[usingItemIndex].sprite = Resources.Load<Sprite>("Item/empty");
        playerItem[usingItemIndex] = "empty";
    }
    void IncreaseHp()
    {
        Debug.Log("Heal Pack 사용");
        Player.instance.hp += 1;
        ItemImg[usingItemIndex].sprite = Resources.Load<Sprite>("Item/empty");
        playerItem[usingItemIndex] = "empty";
    }

    void IncreaseGhostPrice()
    {
        Debug.Log("Increase Ghost Price");
        usingItemIGP = true;
    }

    void CalculateTimeToIGP() //IncreaseGhostPrice = IGP
    {
        if (usingItemIGP == true)
        {
            timeToUseIGP -= Time.deltaTime;

            if (timeToUseIGP <= 0)
            {
                usingItemIGP = false;
                timeToUseIGP = 10;
                ItemImg[usingItemIGPIndex].sprite = Resources.Load<Sprite>("Item/empty");
                playerItem[usingItemIGPIndex] = "empty";
                Ghost.instance.ghostPrice = 100;
                GameObject.Find("ItemBtn" + usingItemIGPIndex).GetComponent<Image>().color = Color.white;
                Debug.Log("Increase Ghost price 사용 종료");
            }
        }
        else
        {
            timeToUseIGP = 10;
        }
        //Debug.Log("IGP Time :" + timeToUseIGP);
    }

    public void CheckItemIWantToUse() //총알을 제외한 아이템을 사용하기 위해 해당 아이템의 버튼을 클릭할 경우
    {
        GameObject clickedBtn = EventSystem.current.currentSelectedGameObject;

        if (usingItemBtn == false)
        {
            for (int i =1 ; i <= 5; i++)
            {
                if (clickedBtn.name.Contains(i.ToString())) //1,2,3,4,5
                {
                    usingItemIndex = i;
                    UseItemOtherThanBullet(clickedBtn);
                    break;
                }
            } 
        }
    }

    void UseItemOtherThanBullet(GameObject clickedBtn) //총알을 제외한 아이템을 사용한다.
    {
        switch (ItemImg[usingItemIndex].GetComponent<Image>().sprite.name)
        {
            case "ReduceGhostSpeed":
                if(usingItemRGS == false) //사용중이 아닌 경우
                {
                    //사운드
                    SoundManager.instance.PlaySound(SoundManager.instance.SelectSound("UseItem"));

                    clickedBtn.GetComponent<Image>().color = orangeColor;
                    //사용중인 경우 사용중이라는 Effect 띄우기
                    usingItemRGSIndex = usingItemIndex;
                    ReduceGhostSpeed();
                }

                break;
            case "IncreaseTime":
                //사운드
                SoundManager.instance.PlaySound(SoundManager.instance.SelectSound("UseItem"));

                IncreaseTime();      
                break;
            case "HealPack":
                if (Player.instance.hp <= 2) //Hp가 닳아있는 상태만 HealPack사용가능하게 함.
                {
                    //사운드
                    SoundManager.instance.PlaySound(SoundManager.instance.SelectSound("UseItem"));

                    IncreaseHp();
                }
                break;
            case "DoubleCoin":
                if (usingItemIGP == false) //사용중이 아닌 경우
                {
                    //사운드
                    SoundManager.instance.PlaySound(SoundManager.instance.SelectSound("UseItem"));

                    clickedBtn.GetComponent<Image>().color = orangeColor;
                    usingItemIGPIndex = usingItemIndex;
                    IncreaseGhostPrice();
                }             
                break;
        }
    }

    //ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    //정보 저장 및 로드 함수

    public void SaveCoinData()
    {
        PlayerPrefs.SetInt("Coin", coin);
        PlayerPrefs.Save();
    }

    void LoadCoinData()
    {
        if (!PlayerPrefs.HasKey("Coin"))
        {
            coin = PlayerPrefs.GetInt("Coin", 0);
        }
        else
        {
            coin = PlayerPrefs.GetInt("Coin");
        }
    }

    public void SaveUsingItemRGSData()
    {
        PlayerPrefs.SetString("UsingItemRGS", usingItemRGS.ToString());
        PlayerPrefs.Save();
    }

    void LoadUsingItemRGSData()
    {
        if (!PlayerPrefs.HasKey("UsingItemRGS"))
        {
            //Debug.Log("usingItemRGS 초기화 x");
            usingItemRGS = bool.Parse(PlayerPrefs.GetString("UsingItemRGS", "false"));
        }
        else
        {
            usingItemRGS = bool.Parse(PlayerPrefs.GetString("UsingItemRGS"));
        }
    }

    public void SaveUsingItemIGPData()
    {
        PlayerPrefs.SetString("UsingItemIGP", usingItemIGP.ToString());
        PlayerPrefs.Save();
    }

    void LoadUsingItemIGPData()
    {
        if (!PlayerPrefs.HasKey("UsingItemIGP"))
        {
            usingItemIGP = bool.Parse(PlayerPrefs.GetString("UsingItemIGP", "false"));
        }
        else
        {
            usingItemIGP = bool.Parse(PlayerPrefs.GetString("UsingItemIGP"));
        }
    }




    public void SaveItemData()
    {
        for (int i = 0; i < playerItem.Length; i++)
        {
            //playerItem을 Item[i]에 저장
            //Item0 Item1 Item2 Item3 Item4 Item5
            PlayerPrefs.SetString("Item" + i.ToString(), playerItem[i]);
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


    public void OpneShop()
    {
        if (Ghost.instance.PurpleGhostObj.transform.position.x >= 3.25 || Ghost.instance.PurpleGhostObj.transform.position.x <= -3.25) //Purple Ghost가 나타나 있지 않아야한다.
        {
            //사운드
            SoundManager.instance.PlaySound(SoundManager.instance.SelectSound("Click"));

            //모든 데이터 Shop 이동 전에 저장하기
            Player.instance.SaveHpData();
            TimeController.instance.SaveTimeData();
            SaveCoinData();
            GameManager.instance.SaveGameData();
            SaveItemData();
            SaveUsingItemRGSData();
            SaveUsingItemIGPData();

            Debug.Log("OpenShop");
            Ghost.instance.SaveKilledGhostCntData();

            Invoke("LoadShop", 0.5f);
        }
    }

    void LoadShop()
    {
        SceneManager.LoadScene("Shop");
    }


}//End Class
