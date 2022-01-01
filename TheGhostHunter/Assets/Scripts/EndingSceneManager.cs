using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class EndingSceneManager : MonoBehaviour
{
    public Text KilledGhostCntTxt;


    private void Start()
    {
        ViewKilledGhostCnt();
    }

    //Replay Button 클릭 시
    public void Replay()
    {
        SceneManager.LoadScene("Main");
    }

    //Title Button 클릭 시
    public void GoTitle()
    {
        SceneManager.LoadScene("Title");
    }

    void ViewKilledGhostCnt()
    {
        KilledGhostCntTxt.text = "Killed Ghost: " + Ghost.instance.killedGhostCnt.ToString(); 
    }

}//End Class
