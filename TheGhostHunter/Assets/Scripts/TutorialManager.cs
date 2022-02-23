using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using UnityEngine.SceneManagement;

public class TutorialManager : MonoBehaviour
{
    public GameObject[] Content = new GameObject[5];
    public GameObject[] ContentCompartment = new GameObject[5];

    public GameObject[] GhostImg = new GameObject[3]; //유령 이미지
    public Text[] GhostInformationTxt = new Text[3]; //유령 이미지

    //현재 페이지
    int currentPage = 1;

    string ghostContent = "";

    //규칙 1 page
    //유령 2~4 page
    //양털 5 page
    //아이템 6 page
    //크레딧 7 page

    private void Start()
    {
        for (int i = 0; i < Content.Length; i++)
        {
            Content[i].SetActive(false);
        }
        Content[0].SetActive(true);
        ContentCompartment[0].GetComponent<Image>().color = new Vector4(110 / 255f, 160 / 255f, 220 / 255f, 255 / 255f);
    }

    public void MovePage()
    {
       
        if(EventSystem.current.currentSelectedGameObject.name.Contains("next"))
        {
            currentPage += 1;
        }
        else
        {
            currentPage -= 1;
        }

        if(currentPage <= 0 || currentPage >= 8)
        {
            SceneManager.LoadScene("Title");
        }


        switch (currentPage)
        {
            //규칙
            case 1:
                for (int i = 0; i < Content.Length; i++)
                {
                    Content[i].SetActive(false);
                    ContentCompartment[i].GetComponent<Image>().color = Color.white;
                }
                ContentCompartment[0].GetComponent<Image>().color = new Vector4(110 / 255f, 160 / 255f, 220 / 255f, 255 / 255f);
                Content[0].SetActive(true);
                break;

            //유령
            case 2:
            case 3:
            case 4:
                for (int i = 0; i < Content.Length; i++)
                {
                    Content[i].SetActive(false);
                    ContentCompartment[i].GetComponent<Image>().color = Color.white;
                }
                ContentCompartment[1].GetComponent<Image>().color = new Vector4(110 / 255f, 160 / 255f, 220 / 255f, 255 / 255f);
                Content[1].SetActive(true);
                SetGhostContetnt();
                break;

            //양털
            case 5:
                for (int i = 0; i < Content.Length; i++)
                {
                    Content[i].SetActive(false);
                    ContentCompartment[i].GetComponent<Image>().color = Color.white;
                }
                ContentCompartment[2].GetComponent<Image>().color = new Vector4(110 / 255f, 160 / 255f, 220 / 255f, 255 / 255f);
                Content[2].SetActive(true);
                break;
            
            //아이템
            case 6:
                for (int i = 0; i < Content.Length; i++)
                {
                    Content[i].SetActive(false);
                    ContentCompartment[i].GetComponent<Image>().color = Color.white;
                }
                ContentCompartment[3].GetComponent<Image>().color = new Vector4(110 / 255f, 160 / 255f, 220 / 255f, 255 / 255f);
                Content[3].SetActive(true);
                break;
            
            //크레딧
            case 7:
                for (int i = 0; i < Content.Length; i++)
                {
                    Content[i].SetActive(false);
                    ContentCompartment[i].GetComponent<Image>().color = Color.white;
                }
                ContentCompartment[4].GetComponent<Image>().color = new Vector4(110 / 255f, 160 / 255f, 220 / 255f, 255 / 255f);
                Content[4].SetActive(true);
                break;
        }
    }

    void SetGhostContetnt()
    {
        //정보, 색깔, 위치, 가격

        switch(currentPage)
        {
            case 2:   //기본 하얀색 유령
                ghostContent = "정보 : 웃음 많은 유령\n" +
                                "색깔 : 하얀색\n" +
                                "장소 : 공중\n" +
                                "가격 : 100~300";
                GhostInformationTxt[0].text = ghostContent;
                GhostImg[0].GetComponent<Image>().sprite= Resources.Load<Sprite>("Ghost/White_DefaultGhost");


                //기본 빨간색 유령
                ghostContent = "정보 : 화나있는 유령\n" +
                               "색깔 : 빨간색\n" +
                               "장소 : 공중\n" +
                               "가격 : 100~300";
                GhostInformationTxt[1].text = ghostContent;
                GhostImg[1].GetComponent<Image>().sprite = Resources.Load<Sprite>("Ghost/Red_DefaultGhost");

                //기본 파란색 유령
                ghostContent = "정보 : 우울해있는 유령\n" +
                              "색깔 : 파란색\n" +
                              "장소 : 공중\n" +
                              "가격 : 100~300";
                GhostInformationTxt[2].text = ghostContent;
                GhostImg[2].GetComponent<Image>().sprite = Resources.Load<Sprite>("Ghost/Blue_DefaultGhost");
                break;

            case 3:
                //부우부우 하얀색 유령
                ghostContent = "정보 : 놀리는 것을 \n          좋아하는 유령\n" +
                              "색깔 : 하얀색\n" +
                              "장소 : 공중\n" +
                              "가격 : 100~300";
                GhostInformationTxt[0].text = ghostContent;
                GhostImg[0].GetComponent<Image>().sprite = Resources.Load<Sprite>("Ghost/White_BooBooGhost");

                //부우부우 빨간색 유령
                ghostContent = "정보 : 놀리는 것을 \n          좋아하는 유령\n" +
                              "색깔 : 빨간색\n" +
                              "장소 : 공중\n" +
                              "가격 : 100~300";
                GhostInformationTxt[1].text = ghostContent;
                GhostImg[1].GetComponent<Image>().sprite = Resources.Load<Sprite>("Ghost/Red_BooBooGhost");

                //부우부우 파란색 유령
                ghostContent = "정보 : 놀리는 것을 \n          좋아하는 유령\n" +
                              "색깔 : 파란색\n" +
                              "장소 : 공중\n" +
                              "가격 : 100~300";
                GhostInformationTxt[2].text = ghostContent;
                GhostImg[2].GetComponent<Image>().sprite = Resources.Load<Sprite>("Ghost/Blue_BooBooGhost");
                break;

            case 4:
                //보라색 유령
                ghostContent = "정보 : 아이템을 훔쳐가는 \n          유령\n" +
                              "색깔 : 보라색\n" +
                              "장소 : 아이템 창\n" +
                              "가격 : 300";
                GhostInformationTxt[0].text = ghostContent;
                GhostImg[0].GetComponent<Image>().sprite = Resources.Load<Sprite>("Ghost/PurpleGhost");

                //네온 검정 유령
                ghostContent = "정보 : 순식간에 나타났다 \n          사라지는 유령\n" +
                              "색깔 : 검정색\n" +
                              "장소 : 풀숲\n" +
                              "가격 : 700";
                GhostInformationTxt[1].text = ghostContent;
                GhostImg[1].GetComponent<Image>().sprite = Resources.Load<Sprite>("Ghost/BlackNeonGhost_2");

                //노란색 유령
                ghostContent = "정보 : 돈을 많이 \n          좋아하는 유령\n" +
                              "색깔 : 노란색\n" +
                              "장소 : 땅\n" +
                              "가격 : 500";
                GhostInformationTxt[2].text = ghostContent;
                GhostImg[2].GetComponent<Image>().sprite = Resources.Load<Sprite>("Ghost/YellowGhost");
                break;

        }
    }

}//End Class
