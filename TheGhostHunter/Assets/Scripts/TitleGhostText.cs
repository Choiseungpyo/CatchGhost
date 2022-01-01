using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class TitleGhostText : MonoBehaviour
{
    public Text[] GhostNameTxt = new Text[3];

    private void Update()
    {
        MoveGhostNameTxt();
    }

    void MoveGhostNameTxt()
    {
        for(int i=0; i< GhostNameTxt.Length; i++)
        {
            if(i==1)
            {
                GhostNameTxt[i].transform.position = Camera.main.WorldToScreenPoint
                (Ghost.instance.GhostObj[i].transform.position + new Vector3(-0.2f, 1, 0));
            }
            else
            {
                GhostNameTxt[i].transform.position = Camera.main.WorldToScreenPoint
                (Ghost.instance.GhostObj[i].transform.position + new Vector3(0.2f, 1, 0));
            }          
        }   
    }

}//End Class
