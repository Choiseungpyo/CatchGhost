using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class EndingSceneManager : MonoBehaviour
{
    public Text KilledGhostCntTxt;
    public Text ReasonWhyGameEndedTxt;

    private void Start()
    {
        GameManager.instance.LoadReasonWhyGameEndedData();
        ViewKilledGhostCnt();
        ReasonWhyGameEndedTxt.text = "끝난 이유 :" + GameManager.instance.reasonWhyGameEnded + System.Environment.NewLine + "(나중에 없앨 텍스트임)";
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
