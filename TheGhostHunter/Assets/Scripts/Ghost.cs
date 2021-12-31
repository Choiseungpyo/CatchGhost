using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Ghost : MonoBehaviour
{

    public GameObject[] GhostObj = new GameObject[3];
    public GameObject PurpleGhostObj;
    public GameObject PurpleGhostAppearEffect;

    float[] ghostSpeed = new float[3];
    bool[] ghostMoving = new bool[3]; //Ghost가 움직일 수 있는지 

    Vector3[] ghostResetPos = new Vector3[3];
    int[] ghostColor = new int[4]; //0:하얀색 1:빨간색 2:파란색 3:보라색

    //보라색 유령
    bool purpleGhostIsDead = false;

    //유령 가격
    [HideInInspector]
    public int ghostPrice = 100;

    static public Ghost instance;
    private void Awake()
    {
        instance = this;

        for (int i = 0; i < 3; i++)
        {
            //유령 움직임 
            ghostMoving[i] = true;

            //유령 색깔
            if (TimeController.instance.limitTime >= 55)
            {
                ghostColor[i] = 0;
            }
            else
            {
                GhostObj[i].GetComponent<SpriteRenderer>().color = SetRandomGhostColor(i);
            }
            ghostColor[3] = 3; //보라색 유령
        }

        //이미지 좌우 반전
        GhostObj[0].GetComponent<SpriteRenderer>().flipX = true;
        GhostObj[2].GetComponent<SpriteRenderer>().flipX = true;


        //유령 스피드
        //0.1
        ghostSpeed[0] = 0.05f;
        ghostSpeed[1] = -0.03f;
        ghostSpeed[2] = 0.1f;

        //유령 재생성 위치
        ghostResetPos[0] = new Vector3(-3.5f, 3.5f, 0);
        ghostResetPos[1] = new Vector3(3.5f, 1, 0);
        ghostResetPos[2] = new Vector3(-3.5f, -1.5f, 0);

        //보라색 유령 초기 위치
        PurpleGhostObj.transform.position = new Vector3(0, -5.5f, 0);

        //보라색 유령 나타날 시 Effect
        PurpleGhostAppearEffect.SetActive(false);
    }

    private void Start()
    {
        //Invoke("PurpleGhostAppearForTheFirstTime", 5); //게임 시작후 10초뒤 보라색 유령이 나오게 설정
    }

    // Update is called once per frame
    void Update()
    {
        MoveGhost();
        ViewPurpleGhostWhtenItemCompartmentIsOpen();
        KillGhost();
        StopPurpleGhostCoroutine();
    }

    void MoveGhost()
    {
        for (int i = 0; i < 3; i++)
        {
            if (ghostMoving[i] == true)
            {
                if(Item.instance.usingItemRGS == true) //유령의 스피드 감소 아이템 사용중인 경우
                {
                    if(i==1)
                    {
                        ghostSpeed[i] = -0.01f;
                    }
                    else
                    {
                        ghostSpeed[i] = 0.01f;
                    }
                    
                }
                GhostObj[i].transform.position += new Vector3(ghostSpeed[i], 0, 0);
                CheckGhostPos();
            }
        }
    }

    void CheckGhostPos() //유령이 화면 바깥으로 나갔는지 확인한다.
    {
        for (int i = 0; i < 3; i++)
        {
            if (i == 1)//우->좌로 움직이는 유령
            {
                if (GhostObj[i].transform.position.x <= -3.5)
                {
                    ghostMoving[i] = false; //움직임을 멈춘다.
                    if (TimeController.instance.limitTime <= 55)
                    {
                        GhostObj[i].GetComponent<SpriteRenderer>().color = SetRandomGhostColor(i);
                    }

                    GhostObj[i].transform.position = ghostResetPos[i];
                    SetRandomGhostSpeed(i);
                    StartCoroutine(ActivateGhostMoving(i));
                }
            }
            else //좌->우로 움직이는 유령
            {
                if (GhostObj[i].transform.position.x >= 3.5)
                {
                    ghostMoving[i] = false; //움직임을 멈춘다.
                    if (TimeController.instance.limitTime <= 55)
                    {
                        GhostObj[i].GetComponent<SpriteRenderer>().color = SetRandomGhostColor(i);
                    }
                    GhostObj[i].transform.position = ghostResetPos[i];
                    SetRandomGhostSpeed(i);
                    StartCoroutine(ActivateGhostMoving(i));
                }
            }
        }
    }

    int SetGhostRandomTimeToAppear() //유령이 나타날 랜덤한 시간을 정한다.
    {
        int ghostRandomTime;
        ghostRandomTime = Random.Range(1, 5); //1~4
        return ghostRandomTime;
    }

    IEnumerator ActivateGhostMoving(int ghostNum) //유령의 움직임을 n초 후에 활성화시킨다.
    {
        int ghostRandTime;
        ghostRandTime = SetGhostRandomTimeToAppear();
        //Debug.Log("Ghost" + ghostNum + "이 " + ghostRandTime + "후에 재생성됩니다.");
        yield return new WaitForSeconds(ghostRandTime);

        ghostMoving[ghostNum] = true; //랜덤한 시간 뒤에 다시 움직일 수 있게 하기
    }


    Color SetRandomGhostColor(int ghostNum) //유령의 색깔 랜덤으로 정하기
    {
        Color ghostRandomColor;
        int ghostColorNum;

        ghostColorNum = Random.Range(0, 3); //0:하얀색 1:빨간색 2:파란색

        switch (ghostColorNum)
        {
            case 0:
                ghostRandomColor = Color.white;
                ghostColor[ghostNum] = 0;
                break;
            case 1:
                ghostRandomColor = Color.red;
                ghostColor[ghostNum] = 1;
                break;
            case 2:
                ghostRandomColor = Color.blue;
                ghostColor[ghostNum] = 2;
                break;
            default:
                ghostRandomColor = Color.white;
                ghostColor[ghostNum] = 0;
                break;
        }

        return ghostRandomColor;
    }

    void SetRandomGhostSpeed(int ghostNum)
    {
        float[] ghostSpeedRandomSet = new float[8];
        int randomIndex;

        ghostSpeedRandomSet[0] = 0.01f;
        ghostSpeedRandomSet[1] = 0.03f;
        ghostSpeedRandomSet[2] = 0.05f;
        ghostSpeedRandomSet[3] = 0.07f;
        ghostSpeedRandomSet[4] = 0.1f;
        ghostSpeedRandomSet[5] = 0.15f;
        ghostSpeedRandomSet[6] = 0.2f;
        ghostSpeedRandomSet[7] = 0.5f;

        randomIndex = Random.Range(0, 8);

        if(Item.instance.usingItemRGS == true) //유령 스피드 감소 아이템 사용중인 경우
        {
            if (ghostNum == 1)
            {
                ghostSpeed[ghostNum] = -0.01f; //0~7
            }
            else
            {
                ghostSpeed[ghostNum] = 0.01f; //0~7
            }
        }
        else
        {
            if (ghostNum == 1)
            {
                ghostSpeed[ghostNum] = -ghostSpeedRandomSet[randomIndex]; //0~7
            }
            else
            {
                ghostSpeed[ghostNum] = ghostSpeedRandomSet[randomIndex]; //0~7
            }
        }
        //Debug.Log("Ghost" + ghostNum + " 스피드: " + ghostSpeed[ghostNum]);
    }


    void KillGhost()
    {
        if (Input.GetMouseButtonDown(0))
        {
            Vector2 pos = Camera.main.ScreenToWorldPoint(Input.mousePosition);
            RaycastHit2D hit = Physics2D.Raycast(pos, transform.forward, 0f);
            if (hit.collider != null)
            {
                int ghostNum;

                ghostNum = returnGhostNum(hit.collider.name);
                //Debug.Log(hit.collider.name);
                if (CompareGhostColorToBullet(ghostNum) == true) //총알과 유령이 색깔이 같을 경우
                {
                    Item.instance.coin += ghostPrice;
                    Debug.Log("Coin :" + Item.instance.coin);
                    Debug.Log(hit.collider.name + "을 죽였습니다.");
                    ResetGhostAttribute(ghostNum);
                }
                else //총알과 유령의 색깔이 다를 경우 -> Hp 1 감소
                {
                    Player.instance.hp -= 1;
                    Debug.Log("Hp :" + Player.instance.hp);
                }
            }
        }
    }

    bool CompareGhostColorToBullet(int ghostNum)
    {
        if (Item.instance.ChangeItemStringToInt(Item.instance.playerItem[0]) == ghostColor[ghostNum])
        {
            return true;
        }
        return false;
    }

    int returnGhostNum(string ghostName)
    {
        int ghostNum;
        switch (ghostName)
        {
            case "Ghost1":
                ghostNum = 0;
                break;
            case "Ghost2":
                ghostNum = 1;
                break;
            case "Ghost3":
                ghostNum = 2;
                break;
            case "PurpleGhost":
                ghostNum = 3;
                break;
            default:
                ghostNum = -1;
                break;
        }

        return ghostNum;
    }


    void ResetGhostAttribute(int ghostNum) //유령이 죽었을 시 유령의 속성값 변경
    {
        if (ghostNum == 3) //Purple Ghost
        {
            purpleGhostIsDead = true;
            PurpleGhostAppearEffect.SetActive(false);
            PurpleGhostObj.transform.position = new Vector3(0, -5.5f, 0); //화면 바깥으로 사라지도록 한다.
        }
        else
        {
            if (TimeController.instance.limitTime <= 55)
            {
                GhostObj[ghostNum].GetComponent<SpriteRenderer>().color = SetRandomGhostColor(ghostNum);
            }

            SetRandomGhostSpeed(ghostNum);
            GhostObj[ghostNum].transform.position = ghostResetPos[ghostNum];
        }
    }

    //Purple Ghost - 플레이어의 아이템을 뺏는 유령
    //플레이어가 아이템 창을 열어놓을 경우 - 모든 아이템 창에서 나타남 -> 일단 구현 완료
    //플레이어가 아이템 창을 닫아 놓을 경우 - 사용중인 아이템 주변에 보라색 빛이 발생 -> 이후 랜덤 아이템 위치 칸에 등장.
    //Item.instance.usingItemBtn 을 통해 열렸을 경우를 확인한다.

    int SetPurpleGhostRandomPos()
    {
        int randomIndex;
        float[] ghostRandomPosSet = new float[6];

        ghostRandomPosSet[5] = -1.15f;
        ghostRandomPosSet[4] = -0.45f;
        ghostRandomPosSet[3] = 0.3f;
        ghostRandomPosSet[2] = 1f;
        ghostRandomPosSet[1] = 1.7f;
        ghostRandomPosSet[0] = 2.4f;


        randomIndex = Random.Range(0, 6); //0~5
        for(int i=0; i< Item.instance.playerItem.Length; i++)
        {
            if(Item.instance.playerItem[i] != "empty")
            {
                break;
            }
            else
            {
                if(i==5) //아이템이 전부 비어있을 경우
                {
                    Debug.Log("아이템이 전부 비어있습니다");
                    return -1;                 
                }
            }
        }

        while (Item.instance.playerItem[randomIndex] == "empty") //아이템이 존재하는 칸에만 Purple Ghost가 나타나게 함.
        {
            //아이템이 모두 없을시 여기서 무한루프 걸려 unity가 멈추었음
            //위 for문에서 이를 해결함.
            randomIndex = Random.Range(0, 6);
        }

        if (Item.instance.itemBtnBV == true && randomIndex != 0) //아이템 창이 닫혀있을 경우
        {
            //아이템 창이 닫혀있는 경우에만 보라색 이펙트 사용
            ViewPurpleGhostAppearEffect(true);
            PurpleGhostObj.SetActive(false);
        }

        PurpleGhostObj.transform.position = new Vector3(ghostRandomPosSet[randomIndex], -4.3f, 0);
        return randomIndex;
    }

    void PurpleGhostAppearForTheFirstTime()
    {
        StartCoroutine("AppearPurpleGhost");
    }

    IEnumerator AppearPurpleGhost() //게임이 종료될때까지 계속 코루틴이 돌아가도록 한다
    {
        int randomPosIndex;
        Debug.Log("AppearPurpleGhost 코루틴 동작 시작");
        randomPosIndex = SetPurpleGhostRandomPos();

        yield return new WaitForSeconds(2); //Purple Ghost가 2초후에 모습이 사라지도록 한다.

        ViewPurpleGhostAppearEffect(false);
        StealItem(randomPosIndex);
        PurpleGhostObj.transform.position = new Vector3(0, -5.5f, 0); //화면 바깥으로 사라지도록 한다.
        //Debug.Log("AppearPurpleGhost 코루틴 동작 끝");
        StartCoroutine("SetPurpleGhostRandomTimeToAppear");
    }

    IEnumerator SetPurpleGhostRandomTimeToAppear() //Purple Ghost가 나타나는 랜덤한 시간 관리
    {
        //Debug.Log("SetPurpleGhostRandomTimeToAppear 코루틴 동작 시작");
        int ghostRandomTime;
        ghostRandomTime = Random.Range(3, 5); //5~10
        Debug.Log(ghostRandomTime + "초 뒤에 Purple Ghost 출현");

        yield return new WaitForSeconds(ghostRandomTime);

        //Debug.Log("SetPurpleGhostRandomTimeToAppear 코루틴 동작 끝");
        StartCoroutine("AppearPurpleGhost");
    }

    void ViewPurpleGhostAppearEffect(bool PurpleGhostAppearBV) //파라미터 : PurpleGHostAppear Bool Value
    {
        PurpleGhostAppearEffect.SetActive(PurpleGhostAppearBV);
    }

    void StopPurpleGhostCoroutine()
    {
        int ghostRandomTime;

        if (purpleGhostIsDead == true)
        {
            //stopCououtine은 String으로 호출하면 String으로 멈춰야한다.
            //함수호출하듯이 코루틴을 호출했을 경우 코루틴 멈추지 않아 string으로 호출로 진행함.
            StopCoroutine("AppearPurpleGhost");
            StopCoroutine("SetPurpleGhostRandomTimeToAppear");
            purpleGhostIsDead = false;
            Debug.Log("보라색 유령 사망");
            ghostRandomTime = Random.Range(3, 5);
            Invoke("PurpleGhostAppearForTheFirstTime", ghostRandomTime);
        }
    }

    void StealItem(int posIndex)
    {
        if(posIndex != -1) //아이템이 전부 비어있지 않은 경우만
        {
            Item.instance.ItemImg[posIndex].sprite = Resources.Load("empty", typeof(Sprite)) as Sprite;
            Item.instance.playerItem[posIndex] = "empty";

        }     
    }

    void ViewPurpleGhostWhtenItemCompartmentIsOpen() //아이템 창이 열려있을때 PurpleGhost를 보여준다.
    {
        //아이템 창이 열려있을 경우 + Purple Ghost가 아이템 창에 나타나있을경우
        if (Item.instance.itemBtnBV == false && PurpleGhostObj.transform.position.y > -5)
        {
            //Debug.Log("아이템 창이 열려있을 경우 + Purple Ghost가 아이템 창에 나타나있을경우");
            PurpleGhostObj.SetActive(true);
        }
        //1. 아이템 창이 닫혀있는 상태에서 보라색 유령 등장 이펙트 뜸
        //2. 이후 아이템 창을 열음
        //3. 보라색 유령을 죽이거나 사라질때까지 아이템 창을 닫지 못하게 함.
        //이를 item Class에서 제어함
    }

}//End Class