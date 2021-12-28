using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player : MonoBehaviour
{

    public int hp = 3;

    public GameObject[] HpImg = new GameObject[3];


    static public Player instance;
    private void Awake()
    {
        instance = this;
        Debug.Log("Hp : " + hp);
    }


    private void Update()
    {
        SetPlayerHpUI();
        CheckPlayerHp();       
    }


    void CheckPlayerHp() //플레이어의 Hp 확인
    {
        if (hp <= 0)
        {
            Debug.Log("Hp <=0 : 게임 종료");
        }
    }

    void SetPlayerHpUI()
    {
        for(int i=0; i<3; i++)
        {
            if(hp >=3) //hp 3
            {
                HpImg[i].SetActive(true);
            }
            else if(hp >= 2) //hp 2
            {
                HpImg[i].SetActive(true);
                if (i == 2)
                {
                    HpImg[i].SetActive(false);
                    break;
                }              
            }
            else if(hp >= 1)
            {
                HpImg[i].SetActive(true);
                if (i == 1)
                {
                    HpImg[i].SetActive(false);
                    break;
                }              
            }
            else
            {
                HpImg[i].SetActive(false);
            }
        }
    }


    void ResetData()
    {
        PlayerPrefs.DeleteAll();
        PlayerPrefs.Save();
    }


}//End Class
