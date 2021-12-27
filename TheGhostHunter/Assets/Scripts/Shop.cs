using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Shop : MonoBehaviour
{
  
    public void OpneShop()
    {
        SceneManager.LoadScene("Shop");
    }

    public void CloseShop()
    {
        SceneManager.LoadScene("Main");
    }
}//End Class
