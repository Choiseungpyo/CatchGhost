using System.Collections;
using System.Collections.Generic;
using UnityEngine;

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
        Debug.Log("GameStart : " + gameStart);
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
    }//End Class
