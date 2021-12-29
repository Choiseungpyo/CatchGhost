using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class TimeController : MonoBehaviour
{
    public Text TimeText;

    float limitTime = 60;

    static public TimeController instance;
    private void Awake()
    {
        instance = this;

        LoadTimeData();
    }
    // Update is called once per frame
    void Update()
    {
        limitTime -= Time.deltaTime;
        TimeText.text = Mathf.Round(limitTime).ToString();
        CheckTime();
    }


    void CheckTime()
    {
        if(limitTime <=0) //제한시간 종료
        {
            //Debug.Log("제한 시간 종료");
        }
    }

    public void SaveTimeData()
    {
        PlayerPrefs.SetFloat("Time", limitTime);
        PlayerPrefs.Save();
        //Debug.Log("Save Time Data : " + PlayerPrefs.GetFloat("Time"));
    }

    void LoadTimeData()
    {
        if(!PlayerPrefs.HasKey("Time"))
        {
            limitTime = PlayerPrefs.GetFloat("Time",60);
        }
        else
        {
            limitTime = PlayerPrefs.GetFloat("Time");
        }
        
        //Debug.Log("Get Time Data(playerPrefs) : " + PlayerPrefs.GetFloat("Time"));
        //Debug.Log("Get Time Data(limitTime) : " + limitTime);
    }
}//End Class
