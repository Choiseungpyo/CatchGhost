using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class Ghost : MonoBehaviour
{
    //프리팹
    public GameObject White_DefaultGhost_Prefabs;
    public GameObject[] BooBooGhost_Prefabs = new GameObject[3];//0,1,2 :White,Red,Blue


    //오브젝트
    [HideInInspector]
    public GameObject[] GhostObj = new GameObject[3];
    public GameObject PurpleGhostObj;
    public GameObject HitEffect;
    public GameObject ItemPurpleGhostStole;

    //죽인 유령 수
    [HideInInspector]
    public int killedGhostCnt = 0;

    //유령 제어
    float[] ghostSpeed = new float[3];
    bool[] ghostMoving = new bool[3]; //Ghost가 움직일 수 있는지 
    Vector3[] ghostResetPos = new Vector3[3];
    int[] ghostColor = new int[4]; //0:하얀색 1:빨간색 2:파란색 3:보라색

    //보라색 유령(purple ghost = pg)
    [HideInInspector]
    public enum PurpleGhostState
    {
        Come, Find, Wait, Go //Come: 왼쪽 아래 대각선 이동 Find:왼쪽으로 이동 Wait: 대기 GO: 왼쪽 위 대각선 이동
    };
    [HideInInspector]
    public PurpleGhostState purpleGhostState = PurpleGhostState.Come;

    private bool pgMoving = false;
    private float pgMovingDistance = 3.0f;            // 이동 시키고 싶은 거리를 정해주면 됨
    private Vector2 pgDestinationPos;      // 이동해야할 최종 위치
    private Vector2 pgCurrentPos = new Vector2(4, 0);    // 내 위치 (텍스쳐 그려질 위치)
    bool controlPGFindMoving = true;
    [HideInInspector]
    public int purpleGhostPosIndex;



    //유령 가격
    [HideInInspector]
    public int ghostPrice = 100;


    static public Ghost instance;
    private void Awake()
    {
        instance = this;
        LoadKilledGhostCntData();

        if (SceneManager.GetActiveScene().name == "Main")
        {
            ItemPurpleGhostStole.GetComponent<SpriteRenderer>().sprite = Resources.Load<Sprite>("Item/empty");
            PurpleGhostObj.GetComponents<BoxCollider2D>()[0].enabled = true; 
            PurpleGhostObj.GetComponents<BoxCollider2D>()[1].enabled = false; 

            HitEffect.SetActive(false);
            //유령 재생성 위치
            ghostResetPos[0] = new Vector3(-3.5f, 2.5f, 0);
            ghostResetPos[1] = new Vector3(3.5f, 0, 0);
            ghostResetPos[2] = new Vector3(-3.5f, -2.5f, 0);

            for (int i = 0; i < 3; i++)
            {
                //유령 움직임 
                ghostMoving[i] = true;

                //유령 색깔
                if (TimeController.instance.limitTime >= 50)
                {
                    ghostColor[i] = 0;
                    GhostObj[i] = Instantiate(White_DefaultGhost_Prefabs, ghostResetPos[i], Quaternion.identity, transform);               
                }
                else
                {
                    GhostObj[i] = Instantiate(SetRandomGhostColor(i), ghostResetPos[i], Quaternion.identity, transform);
                }
                GhostObj[i].name = "Ghost" + (i + 1).ToString();

                //유령 크기
                ChangeGhostScale(i);
            }
            ghostColor[3] = 3; //보라색 유령

            //이미지 좌우 반전
            GhostObj[0].GetComponent<SpriteRenderer>().flipX = true;
            GhostObj[2].GetComponent<SpriteRenderer>().flipX = true;

            //유령 스피드
            //0.1
            ghostSpeed[0] = 0.05f;
            ghostSpeed[1] = -0.03f;
            ghostSpeed[2] = 0.1f;        

            //보라색 유령 초기 위치
            PurpleGhostObj.transform.position = new Vector3(4, 0, 0);
        }
        else if(SceneManager.GetActiveScene().name == "Ending")
        {
            for (int i = 0; i < 3; i++)
            {
                //유령 오브젝트
                GhostObj[i] = null;

                //유령 움직임 
                ghostMoving[i] = true;

                //유령 색깔
                ghostColor[i] = 0;

                //유령 스피드
                ghostSpeed[i] = 0;

                //유령 재생성 위치
                ghostResetPos[i] =Vector3.zero;
            }
            ghostColor[3] = 3; //보라색 유령

            PurpleGhostObj = null;
            HitEffect = null;
        }
        else if (SceneManager.GetActiveScene().name == "Title")
        {
            //유령 재생성 위치
            ghostResetPos[0] = new Vector3(-3.5f, 2.5f, 0);
            ghostResetPos[1] = new Vector3(3.5f, 0, 0);
            ghostResetPos[2] = new Vector3(-3.5f, -2.5f, 0);

            for (int i = 0; i < 3; i++)
            {
                switch(i)
                {
                    case 0:
                        GhostObj[i] = Instantiate(BooBooGhost_Prefabs[0], ghostResetPos[i], Quaternion.identity, transform);                       
                        break;
                    case 1:
                        GhostObj[i] = Instantiate(BooBooGhost_Prefabs[1], ghostResetPos[i], Quaternion.identity, transform);
                        break;
                    case 2:
                        GhostObj[i] = Instantiate(BooBooGhost_Prefabs[2], ghostResetPos[i], Quaternion.identity, transform);
                        break;
                }
                GhostObj[i].name = "Ghost" + (i + 1).ToString();

                //유령 크기
                ChangeGhostScale(i);

                //유령 움직임 
                ghostMoving[i] = true;

                //유령 색깔
                ghostColor[i] =i; //하얀색, 빨간색, 파란색 유령 순으로 Title에서 색깔 고정하도록 함.
            }
            
            ghostColor[3] = 3; //보라색 유령

            //이미지 좌우 반전
            GhostObj[0].GetComponent<SpriteRenderer>().flipX = true;
            GhostObj[2].GetComponent<SpriteRenderer>().flipX = true;

            //유령 스피드
            ghostSpeed[0] = 0.01f;
            ghostSpeed[1] = -0.01f;
            ghostSpeed[2] = 0.01f;

            PurpleGhostObj = null;
            HitEffect = null;
        }
    }

    private void Start()
    {
        if (SceneManager.GetActiveScene().name == "Main")
        {
            //보라색 유령 처음에 10초후에 등장시키기
            Invoke("FirstPurpleGhost", 3);
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (SceneManager.GetActiveScene().name == "Main" || SceneManager.GetActiveScene().name == "Title")
        {
            MoveGhost(); 
            MovePurpleGhost();
            ChangePurpleGhostCollider();
            KillGhost();
        }
    }

    void MoveGhost()
    {
        for (int i = 0; i < 3; i++)
        {
            if (ghostMoving[i] == true)
            {
                if(SceneManager.GetActiveScene().name == "Main")
                {
                    if (Item.instance.usingItemRGS == true) //유령의 스피드 감소 아이템 사용중인 경우
                    {
                        if (i == 1)
                        {
                            ghostSpeed[i] = -0.01f;
                        }
                        else
                        {
                            ghostSpeed[i] = 0.01f;
                        }
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
                    if(SceneManager.GetActiveScene().name == "Main")
                    {
                        if (TimeController.instance.limitTime <= 50)
                        {
                            //Main Scene에서만 랜덤 색깔로 바뀌게
                            //Title Scene에서는 색깔 고정
                            Destroy(GhostObj[i]);
                            GhostObj[i] = Instantiate(SetRandomGhostColor(i), ghostResetPos[i],Quaternion.identity, transform);
                            GhostObj[i].name = "Ghost" + (i + 1);

                            ChangeGhostScale(i);

                            SetRandomGhostSpeed(i);
                            StartCoroutine(ActivateGhostMoving(i));
                        }
                        else
                        {
                            SetRandomGhostSpeed(i);
                            GhostObj[i].transform.position = ghostResetPos[i];
                            StartCoroutine(ActivateGhostMoving(i));
                        }
                    }  
                    else if(SceneManager.GetActiveScene().name == "Title")
                    {
                        GhostObj[i].transform.position = ghostResetPos[i];
                        ghostMoving[i] = true;
                    }                     
                }
            }
            else //좌->우로 움직이는 유령
            {
                if (GhostObj[i].transform.position.x >= 3.5)
                {
                    ghostMoving[i] = false; //움직임을 멈춘다.

                    if (SceneManager.GetActiveScene().name == "Main")
                    {
                        if (TimeController.instance.limitTime <= 50)
                        {
                            Destroy(GhostObj[i]);
                            GhostObj[i] = Instantiate(SetRandomGhostColor(i), ghostResetPos[i], Quaternion.identity, transform);
                            GhostObj[i].name = "Ghost" + (i+1);

                            ChangeGhostScale(i);

                            GhostObj[i].GetComponent<SpriteRenderer>().flipX = true;

                            SetRandomGhostSpeed(i);
                            StartCoroutine(ActivateGhostMoving(i));
                        }
                        else
                        {
                            SetRandomGhostSpeed(i);
                            GhostObj[i].transform.position = ghostResetPos[i];
                            StartCoroutine(ActivateGhostMoving(i));
                        }
                    }
                    else if(SceneManager.GetActiveScene().name == "Title")
                    {
                        GhostObj[i].transform.position = ghostResetPos[i];
                        ghostMoving[i] = true;
                    }         
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


    GameObject SetRandomGhostColor(int ghostNum) //유령의 색깔 랜덤으로 정하기
    {
        Color ghostRandomColor;
        GameObject randomGhostObjrColor = null;
        int ghostColorNum;

        ghostColorNum = Random.Range(0, 3); //0:하얀색 1:빨간색 2:파란색

        switch (ghostColorNum)
        {
            case 0:
                randomGhostObjrColor = BooBooGhost_Prefabs[0];
                ghostRandomColor = Color.white;
                ghostColor[ghostNum] = 0;
                break;
            case 1:
                randomGhostObjrColor = BooBooGhost_Prefabs[1];
                ghostRandomColor = Color.red;
                ghostColor[ghostNum] = 1;
                break;
            case 2:
                randomGhostObjrColor = BooBooGhost_Prefabs[2];
                ghostRandomColor = Color.blue;
                ghostColor[ghostNum] = 2;
                break;
            default:
                randomGhostObjrColor = BooBooGhost_Prefabs[0];
                ghostRandomColor = Color.white;
                ghostColor[ghostNum] = 0;
                break;
        }

        return randomGhostObjrColor;
    }

    void SetRandomGhostSpeed(int ghostNum)
    {
        float[] ghostSpeedRandomSet = new float[8];
        int randomIndex;

        //스피드가 너무 빨라 변경
        //원래 : 0.01f 0.03f 0.05f 0.07f 0.1f 0.15f 0.2f 0.5f

        ghostSpeedRandomSet[0] = 0.01f;
        ghostSpeedRandomSet[1] = 0.02f;
        ghostSpeedRandomSet[2] = 0.03f;
        ghostSpeedRandomSet[3] = 0.04f;
        ghostSpeedRandomSet[4] = 0.05f;
        ghostSpeedRandomSet[5] = 0.06f;
        ghostSpeedRandomSet[6] = 0.07f;
        ghostSpeedRandomSet[7] = 0.08f;

        randomIndex = Random.Range(0, 8);

        if (Item.instance.usingItemRGS == true) //유령 스피드 감소 아이템 사용중인 경우
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
        //if (Input.GetMouseButtonDown(0))
        //{
        //    Vector2 pos = Camera.main.ScreenToWorldPoint(Input.mousePosition);
        //    RaycastHit2D hit = Physics2D.Raycast(pos, transform.forward, 0f);
        //    if (hit.collider != null)
        //    {
        //        int ghostNum;
        //        //Debug.Log("클릭한 오브젝트 이름 : " + hit.collider.name);
        //        ghostNum = returnGhostNum(hit.collider.name);
        //        if (SceneManager.GetActiveScene().name == "Title") //Title에서는 총알 색깔 상관없이 유령 쏘면 죽도록 함.
        //        {
        //            if (hit.collider.gameObject.name == "Ghost1")
        //            {
        //                Debug.Log("Main Scene 이동");
        //                SceneManager.LoadScene("Main");
        //                return;
        //            }
        //            else if (hit.collider.gameObject.name == "Ghost2")
        //            {
        //                Debug.Log("Tutorial Scene 이동");
        //                SceneManager.LoadScene("Tutorial");
        //                return;
        //            }
        //            else if (hit.collider.gameObject.name == "Ghost3")
        //            {
        //                Debug.Log("게임 종료");
        //                Application.Quit();
        //                return;
        //            }
        //        }
        //        //Debug.Log(hit.collider.name);
        //        if (CompareGhostColorToBullet(ghostNum) == true) //총알과 유령이 색깔이 같을 경우
        //        {
        //            killedGhostCnt += 1;
        //            Item.instance.coin += CheckKilledGhostPrice(ghostNum);
        //            //Debug.Log("Coin :" + Item.instance.coin);
        //            //Debug.Log(hit.collider.name + "을 죽였습니다.");
        //            ResetGhostAttribute(ghostNum);
        //        }
        //        else //총알과 유령의 색깔이 다를 경우 -> Hp 1 감소
        //        {
        //            StartCoroutine("ViewHitEffect");
        //            Player.instance.hp -= 1;
        //            //Debug.Log("Hp :" + Player.instance.hp);
        //        }
        //    }
        //}


        //모바일 터치 
        if (Input.touchCount > 0)
        {
            Touch touch = Input.GetTouch(0);

            if (touch.phase == TouchPhase.Began)
            {
                Vector2 touchPos = Camera.main.ScreenToWorldPoint(Input.mousePosition);
                RaycastHit2D hit = Physics2D.Raycast(touchPos, Vector2.zero, 0f, LayerMask.GetMask("Ghost"));

                if (hit.collider != null)
                {
                    int ghostNum;

                    ghostNum = returnGhostNum(hit.collider.name);
                    if (SceneManager.GetActiveScene().name == "Title") //Title에서는 총알 색깔 상관없이 유령 쏘면 죽도록 함.
                    {
                        if (hit.collider.gameObject.name == "Ghost1")
                        {
                            Debug.Log("Main Scene 이동");
                            SceneManager.LoadScene("Main");
                            return;
                        }
                        else if (hit.collider.gameObject.name == "Ghost2")
                        {
                            Debug.Log("Tutorial Scene 이동");
                            SceneManager.LoadScene("Tutorial");
                            return;
                        }
                        else if (hit.collider.gameObject.name == "Ghost3")
                        {
                            Debug.Log("게임 종료");
                            Application.Quit();
                            return;
                        }
                    }
                    //Debug.Log(hit.collider.name);
                    if (CompareGhostColorToBullet(ghostNum) == true) //총알과 유령이 색깔이 같을 경우
                    {
                        killedGhostCnt += 1;
                        Item.instance.coin += ghostPrice;
                        //Debug.Log("Coin :" + Item.instance.coin);
                        //Debug.Log(hit.collider.name + "을 죽였습니다.");
                        ResetGhostAttribute(ghostNum);
                    }
                    else //총알과 유령의 색깔이 다를 경우 -> Hp 1 감소
                    {
                        Player.instance.hp -= 1;
                        //Debug.Log("Hp :" + Player.instance.hp);
                    }
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
            CancelInvoke("ChangeMoingFalseToTrue");
            pgMoving = false;
            purpleGhostState = PurpleGhostState.Go;
            PurpleGhostObj.transform.position = new Vector3(4, 0, 0);
            pgCurrentPos = new Vector2(4, 0);
            controlPGFindMoving = true;
            ItemPurpleGhostStole.GetComponent<SpriteRenderer>().sprite = Resources.Load<Sprite>("Item/empty");
            Invoke("ChangeMoingFalseToTrue", SetPurpleGhostRandomTimeToAppear());
        }
        else
        {
            if (TimeController.instance.limitTime <= 50)
            {
                Destroy(GhostObj[ghostNum]);
                GhostObj[ghostNum] = Instantiate(SetRandomGhostColor(ghostNum), ghostResetPos[ghostNum], Quaternion.identity, transform);
                GhostObj[ghostNum].name = "Ghost" + (ghostNum+1);

                SetRandomGhostSpeed(ghostNum);
                ChangeGhostScale(ghostNum);

                if (ghostNum != 1)
                {
                    GhostObj[ghostNum].GetComponent<SpriteRenderer>().flipX = true;
                }
            }
            else
            {
                SetRandomGhostSpeed(ghostNum);
                GhostObj[ghostNum].transform.position = ghostResetPos[ghostNum];
            }   
        }
    }

    void ChangeGhostScale(int ghostNum) //유령의 크기를 조절한다.(상단에 있는 유령일수록 멀리 있어보이게 크기를 줄인다.);
    {
        switch(ghostNum)
        {
            case 0:
                GhostObj[ghostNum].transform.localScale = new Vector3(0.25f, 0.25f, 1);
                break;
            case 1:
                GhostObj[ghostNum].transform.localScale = new Vector3(0.3f, 0.3f, 1);
                break;
            case 2:
                GhostObj[ghostNum].transform.localScale = new Vector3(0.35f, 0.35f, 1);
                break;
        }
    }

    int CheckKilledGhostPrice(int ghostNum) //죽인 유령의 가격을 확인한다.
    {
        int ghostPriceContent = 100;
        switch(ghostNum)
        {
            case 0://제일 상단에 있는 유령인 경우
                ghostPriceContent = 300;
                break;
            case 1:
                ghostPriceContent = 200;
                break;
            case 2://제일 하단에 있는 유령인 경우
                ghostPriceContent = 100;
                break;
            default:
                ghostPriceContent = 100;
                break;
        }

        return ghostPriceContent;
    }

    //Purple Ghost - 플레이어의 아이템을 뺏는 유령
    //플레이어가 아이템 창을 열어놓을 경우 - 모든 아이템 창에서 나타남 -> 일단 구현 완료
    //플레이어가 아이템 창을 닫아 놓을 경우 - 사용중인 아이템 주변에 보라색 빛이 발생 -> 이후 랜덤 아이템 위치 칸에 등장.
    //Item.instance.usingItemBtn 을 통해 열렸을 경우를 확인한다.

    Vector2 SetPurpleGhostRandomPos()
    {
        int randomIndex;
        float[] ghostRandomPosSet = new float[6];

        ghostRandomPosSet[5] = -0.9f;
        ghostRandomPosSet[4] = -0.25f;
        ghostRandomPosSet[3] = 0.4f;
        ghostRandomPosSet[2] = 1.05f;
        ghostRandomPosSet[1] = 1.7f;
        ghostRandomPosSet[0] = 2.3f;


        randomIndex = Random.Range(0, 6); //0~5

        while (Item.instance.playerItem[randomIndex] == "empty") //아이템이 존재하는 칸에만 Purple Ghost가 나타나게 함.
        {
            randomIndex = Random.Range(0, 6);
        }

        purpleGhostPosIndex = randomIndex;

        return new Vector2(ghostRandomPosSet[randomIndex], -4.05f); //-4.3f
    }


    void MovePurpleGhost()
    {
        if (pgMoving == false)
            return;

        ControlPurpleGhostMoving();


        // 내 위치에서 가야 할 위치에 대한 방향을 구한다.
        Vector2 vec2Dir = pgDestinationPos - pgCurrentPos;
        vec2Dir.Normalize();        // 단위 벡터를 만든다.

        // 가야할 방에 시간 값을 곱해서 조금씩 이동하게 한다.
        // (시간값 * 이동 거리 = 한 프레임당 이동하고 싶은 간격)
        Vector2 vec2Temp = vec2Dir * (Time.deltaTime * pgMovingDistance);

        // 내 위치에서 이동해야할 방향 값을 더하면 조금 이동했을 때의 위치값이 나온다.
        vec2Temp = pgCurrentPos + vec2Temp;

        // 현재 내 위치로부터 계산되서 나온 다음 위치까지의 거리를 구한다.
        float fNowDistance = Vector2.Distance(vec2Temp, pgCurrentPos);

        // 내 위치로부터 최종 목적지로 설정된 위치까지의 거리를 구한다.
        float fDestDistance = Vector2.Distance(pgDestinationPos, pgCurrentPos);

        // 두 위치 값을 비교해서 목적 위치를 지나쳤는지 검사한다.
        // 현재 예상 거리 값이 최종 거리 값을 넘기거나 같으면 더이상 이동 할 필요 없음
        if (fNowDistance >= fDestDistance)
        {
            pgMoving = false;
            // 현재 위치 값을 최종 위치 값으로 설정
            ControlPurpleGhostMoving();
            pgCurrentPos = pgDestinationPos;
        }
        else
        {
            pgCurrentPos = vec2Temp;
        }
        PurpleGhostObj.transform.position = new Vector3(pgCurrentPos[0], pgCurrentPos[1], 0);
    }

    //날아와서 대기(코루틴 위) -> 1.5초 (waitforseconds) -> 날아감(코루틴 아래) 
    //날아와서 대기(move함수) -> 1.5초 (Invoke) -> 날아감(move함수)
    //come -> wait -> go

    void ControlPurpleGhostMoving()
    {
        if (pgMoving == true) //움직이는 중
        {
            if (purpleGhostState == PurpleGhostState.Come)
            {
                if (CheckIfAllTheItemsAreEmpty() == false) //아이템이 하나라도 있을경우 보라색 유령을 움직이게 한다.
                {
                    //목표 지점 : 사용중인 아이템 위치
                    pgDestinationPos = new Vector2(2.3f, -4.05f); //-4.3f
                }
            }
            else if (purpleGhostState == PurpleGhostState.Find)
            {
                //목표 지점 : 랜덤한 아이템 위치
                if (controlPGFindMoving == true) //한번만 동작하도록 
                {
                    controlPGFindMoving = false;
                    pgDestinationPos = SetPurpleGhostRandomPos();
                    //Debug.Log("랜덤한 아이템 위치 : " + pgDestinationPos);
                }
            }
            else if (purpleGhostState == PurpleGhostState.Go)
            {
                //목표 지점 : 왼쪽 화면 바깥
                pgDestinationPos = new Vector2(-4, 0);
            }

        }//움직임을 멈춤.
        else
        {
            if (purpleGhostState == PurpleGhostState.Come)
            { 
                if (CheckIfAllTheItemsAreEmpty() == false) //아이템이 하나라도 있을경우 보라색 유령을 움직이게 한다.
                {
                    //사용중인 아이템 자리에 도착하면 아이템창이 열리도록 하게 하기           
                    Invoke("ChangeMoingFalseToTrue", 0.5f);
                }
            }
            else if (purpleGhostState == PurpleGhostState.Find)
            {
                purpleGhostState = PurpleGhostState.Wait;
                Invoke("ChangeMoingFalseToTrue", 2);
            }
            else if (purpleGhostState == PurpleGhostState.Go)
            {
                pgDestinationPos = new Vector2(4, 0);//처음 위치
                controlPGFindMoving = true;
                Invoke("ChangeMoingFalseToTrue", SetPurpleGhostRandomTimeToAppear());       
            }
        }     
    }

    void ChangeMoingFalseToTrue()
    {
        if (purpleGhostState == PurpleGhostState.Come)
        {
            purpleGhostState = PurpleGhostState.Find;
        }
        else if (purpleGhostState == PurpleGhostState.Wait)
        {
            StealItem();
            purpleGhostState = PurpleGhostState.Go;
        }
        else if (purpleGhostState == PurpleGhostState.Go)
        {
            ItemPurpleGhostStole.GetComponent<SpriteRenderer>().sprite = Resources.Load<Sprite>("Item/empty");
            purpleGhostState = PurpleGhostState.Come;
        }

        pgMoving = true;
    }

    int SetPurpleGhostRandomTimeToAppear()
    {
        int randomTime;
        randomTime = Random.Range(3, 6);

        return randomTime;
    }

    void FirstPurpleGhost() //보라색 유령 처음에 나왔을때만 동작하는 함수
    {
        pgMoving = true;
    }

    void StealItem()
    {
        if (Item.instance.usingItemIGP == true && purpleGhostPosIndex != 0) //아이템을 사용중인 경우에 아이템을 뺏을 경우 아이템 사용 중단 
        {
            ghostPrice = 100;
            Item.instance.usingItemIGP = false;
            GameObject.Find("ItemBtn" + purpleGhostPosIndex).GetComponent<Image>().color = Color.white;
        }
        else if (Item.instance.usingItemRGS == true && purpleGhostPosIndex != 0)//아이템을 사용중인 경우에 아이템을 뺏을 경우 아이템 사용 중단
        {
            Item.instance.usingItemRGS = false;
            GameObject.Find("ItemBtn" + purpleGhostPosIndex).GetComponent<Image>().color = Color.white;
        }

        //리소스에 따라 크기가 일정하지 않아서 나중에 수정하기
        ItemPurpleGhostStole.GetComponent<SpriteRenderer>().sprite = Resources.Load<Sprite>("Item/"+Item.instance.playerItem[purpleGhostPosIndex]);


        Item.instance.ItemImg[purpleGhostPosIndex].sprite = Resources.Load<Sprite>("Item/empty");
        Item.instance.playerItem[purpleGhostPosIndex] = "empty";
    }

    bool CheckIfAllTheItemsAreEmpty()
    {
        for (int i = 0; i < Item.instance.playerItem.Length; i++)
        {
            if (Item.instance.playerItem[i] != "empty")
            {
                break;
            }
            else
            {
                if (i == 5) //아이템이 전부 비어있을 경우
                {
                    Debug.Log("아이템이 전부 비어있습니다");
                    return true;
                }
            }
        }
        return false;
    }


    IEnumerator ViewHitEffect()
    {
        HitEffect.SetActive(true);

        yield return new WaitForSeconds(0.3f);

        HitEffect.SetActive(false);
    }


    void ChangePurpleGhostCollider()
    {
        if (!(SceneManager.GetActiveScene().name == "Main"))
            return;

            if (PurpleGhostObj.transform.position.y > -4.05f) //-4.3f
        {
            //Collider변경 - 배열 순서는 인스펙터창 순서대로이다.
            PurpleGhostObj.GetComponents<BoxCollider2D>()[0].enabled = true; //콜라이더 범위 : Purple Ghost 전체
            PurpleGhostObj.GetComponents<BoxCollider2D>()[1].enabled = false; //콜라이더 범위 : Purple Ghost 머리부분만
        }
        else
        {
            PurpleGhostObj.GetComponents<BoxCollider2D>()[0].enabled = false;
            PurpleGhostObj.GetComponents<BoxCollider2D>()[1].enabled = true;
        }
    }

    //ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    //데이터 저장 및 로드 
    public void SaveKilledGhostCntData()
    {
        PlayerPrefs.SetInt("KilledGhostCnt", killedGhostCnt);
        PlayerPrefs.Save();
    }

    void LoadKilledGhostCntData()
    {
        if (!PlayerPrefs.HasKey("GameStart"))
        {
            killedGhostCnt = PlayerPrefs.GetInt("KilledGhostCnt", 0);
        }
        else
        {
            killedGhostCnt = PlayerPrefs.GetInt("KilledGhostCnt");
        }
    }



    }//End Class