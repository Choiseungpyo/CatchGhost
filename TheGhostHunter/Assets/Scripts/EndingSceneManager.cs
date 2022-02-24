using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class EndingSceneManager : MonoBehaviour
{
    public Text totalKilledGhostTxt;
    public Text reasonWhyGameEndedTxt;
    public Text[] killedGhostCntTxt = new Text[9]; //하얀색기본, 빨간색기본, 파란색기본,하얀색부우부우, 빨간색부우부우, 파란색부우부우, 보라색, 검정색네온, 노란색 

    private void Start()
    {
        GameManager.instance.LoadReasonWhyGameEndedData();
        ViewKilledGhostCnt();
        reasonWhyGameEndedTxt.text = "끝난 이유 :" + GameManager.instance.reasonWhyGameEnded + System.Environment.NewLine + "(나중에 없앨 텍스트임)";
    }

    //Replay Button 클릭 시
    public void Replay()
    {
        //사운드
        SoundManager.instance.PlaySound(SoundManager.instance.SelectSound("Click"));

        Invoke("LoadStartGame", 0.5f);
    }

    //Title Button 클릭 시
    public void GoTitle()
    {
        //사운드
        SoundManager.instance.PlaySound(SoundManager.instance.SelectSound("Click"));

        Invoke("LoadTitle", 0.5f);
    }

    void ViewKilledGhostCnt()
    {
        int[] killedGhost = Ghost.instance.killedGhostCnt;

        //Debug.Log(Ghost.instance.totalKilledGhostCnt);
        totalKilledGhostTxt.text = "Killed Ghost : " + Ghost.instance.totalKilledGhostCnt.ToString(); 

        for(int i=0; i < killedGhost.Length; i++)
        {
            killedGhostCntTxt[i].text = ": " + killedGhost[i].ToString();
        }
    }

    void LoadTitle()
    {
        SceneManager.LoadScene("Title");
    }

    void LoadStartGame()
    {
        SceneManager.LoadScene("Main");
    }

}//End Class
