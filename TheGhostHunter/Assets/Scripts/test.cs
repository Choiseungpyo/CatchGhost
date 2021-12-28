using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

//PlayerPrefs 공부하기 위한 스크립트

public class test : MonoBehaviour
{
    [HideInInspector]
    public int[] cakeCnt = new int[5];

    static public test instance;
    private void Awake()
    {
        instance = this;
    }

    private void Start()
    {
        //Debug.Log("SaveData 전 cakeCnt : " + cakeCnt);
        if (SceneManager.GetActiveScene().name == "Main")
        {
            SaveData();
            Debug.Log("Main : Save Data");
            for (int i = 0; i < 5; i++)
            {
                Debug.Log("Main : cakeCnt : " + cakeCnt[i]);
            }       
        }
        
        //Debug.Log("SavaData 후 LoadData 전 cakeCnt : " + cakeCnt);

        if (SceneManager.GetActiveScene().name == "Shop")
        {
            LoadData();
            Debug.Log("Shop : Get Data");
            for (int i = 0; i < 5; i++)
            {
                Debug.Log("Main : cakeCnt : " + cakeCnt[i]);
            }
            
        }
           
        
    }

    void SaveData()
    {
        //Debug.Log("저장되어있던 cake:" + PlayerPrefs.GetInt("cake"));
        for(int i=0; i<5; i++)
        {
            PlayerPrefs.SetInt("cake"+i.ToString(), cakeCnt[i]);
        }
        
        PlayerPrefs.Save();
    }

    void LoadData()
    {
        for(int i=0; i<5; i++)
        {
            cakeCnt[i] = PlayerPrefs.GetInt("cake"+i.ToString());
        }
           
    }
}//End Class
