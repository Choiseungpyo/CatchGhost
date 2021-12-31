using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class EndingSceneManager : MonoBehaviour
{
    //Replay Button 클릭 시
    public void Replay()
    {
        SceneManager.LoadScene("Main");
    }

    //Title Button 클릭 시
    public void GoTitle()
    {
        SceneManager.LoadScene("Start");
    }

}//End Class
