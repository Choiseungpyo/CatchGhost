using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class Player : MonoBehaviour
{
    [HideInInspector]
    public int hp = 3;

    public GameObject[] HpImg = new GameObject[3];


    static public Player instance;
    private void Awake()
    {
        instance = this;

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
                HpImg[i].SetActive(true);
            }
            else if(hp == 2) //hp 2
            {
                HpImg[i].SetActive(true);
                if (i == 2)
                {
                    HpImg[i].SetActive(false);
                    break;
                }              
            }
            else if(hp == 1)
            {
                HpImg[i].SetActive(true);
                if (i == 1 || i ==2)
                {
                    HpImg[i].SetActive(false);
                }              
            }
            else
            {
                HpImg[i].SetActive(false);
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
