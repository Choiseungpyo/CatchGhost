using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{
    [HideInInspector]
    public string gameStart = "true"; //playerPrefs 대신 static을 이용하여 다른씬으로 이동했다 와도 데이터 저장되어 있게함
    static string gameStartCopy = "true";

    static public GameManager instance;
    private void Awake()
    {
        instance = this;
        LoadGameData();
        ResetGame();
    }

    private void Update()
    {
        //게임 오버 조건을 확인하는 함수
        CheckPlayerHp();
        CheckTime();
        CheckCoinAndItem();
    }

    void ResetGame()
    {
        if (gameStartCopy == "true") //게임 시작시 모든 데이터 리셋 
        {
            PlayerPrefs.DeleteAll();
            PlayerPrefs.Save();
            Debug.Log("Reset");
        }
        gameStartCopy = "false";
        gameStart = gameStartCopy;
    }

    public void SaveGameData()
    {
        PlayerPrefs.SetString("GameStart", gameStart);
        PlayerPrefs.Save();
    }

    void LoadGameData()
    {
        if (!PlayerPrefs.HasKey("GameStart"))
        {
            gameStart = PlayerPrefs.GetString("GameStart", "true");
        }
        else
        {
            gameStart = PlayerPrefs.GetString("GameStart");
        }
    }


    //Game Over 조건 확인
    //1. Hp == 0
    //2. Coin으로 총알을 살 돈이 없을 경우 && 총알이 없을 경우
    //3. 제한시간 == 0
    void CheckPlayerHp() //플레이어의 Hp 확인
    {
        if (Player.instance.hp <= 0)
        {
            Debug.Log("Hp <=0 : 게임 종료");
            GameOver();
        }
    }


    void CheckCoinAndItem()
    {
        for(int i=0; i< Item.instance.playerItem.Length; i++)
        {
            if(!Item.instance.playerItem[i].Contains("Bullet")) //유령을 죽일 수 있는 총알을 가지고 있지 않을 경우
            {                
                if (Item.instance.coin < 500) //총알을 구입할 수 있는 최소 금액보다 작은 경우
                {
                    Debug.Log("총알 구매 최소 금액 x && 총알 가지고 있지 않음 : 게임 종료");
                    GameOver();
                    break;
                }
            }
            else
            {
                break;
            }
        }       
    }

    void CheckTime()
    {
        if (TimeController.instance.limitTime <= 0) //제한시간 종료
        {
            Debug.Log("제한 시간 종료");
            GameOver();               
        }
    }

    public void GameOver()
    {
        gameStartCopy = "true";
        Ghost.instance.SaveKilledGhostCntData();
        SceneManager.LoadScene("Ending");
    }

}//End Class
