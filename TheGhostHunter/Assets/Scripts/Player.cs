using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;


public class Player : MonoBehaviour
{
    [HideInInspector]
    public int hp = 3;



    public GameObject[] HpImg = new GameObject[3];


    static public Player instance;
    private void Awake()
    {
        instance = this;
        for(int i=0; i<HpImg.Length; i++)
        {
            HpImg[i].SetActive(true);
        }

        LoadHpData();
    }


    private void Update()
    {
        SetPlayerHpUI();
    }

    void SetPlayerHpUI()
    {
        for(int i=0; i<3; i++)
        {
            if(hp == 3) //hp 3
            {
                HpImg[i].GetComponent<Image>().sprite = Resources.Load<Sprite>("Player/FullHp");
            }
            else if(hp == 2) //hp 2
            {
                HpImg[i].GetComponent<Image>().sprite = Resources.Load<Sprite>("Player/FullHp");
                if (i == 2)
                {
                    HpImg[i].GetComponent<Image>().sprite = Resources.Load<Sprite>("Player/WornUpHP");
                    break;
                }              
            }
            else if(hp == 1)
            {
                HpImg[i].GetComponent<Image>().sprite = Resources.Load<Sprite>("Player/FullHp");
                if (i == 1 || i ==2)
                {
                    HpImg[i].GetComponent<Image>().sprite = Resources.Load<Sprite>("Player/WornUpHP");
                }              
            }
            else
            {
                HpImg[i].GetComponent<Image>().sprite = Resources.Load<Sprite>("Player/WornUpHP");
            }
        }
    }

    public void SaveHpData()
    {
        PlayerPrefs.SetInt("Hp", hp);
        PlayerPrefs.Save();
    }

    void LoadHpData()
    {
        if (!PlayerPrefs.HasKey("Hp"))
        {
            hp = PlayerPrefs.GetInt("Hp", 3);
        }
        else
        {
            hp = PlayerPrefs.GetInt("Hp");
        }
    }

   
}//End Class
