using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Movingtest : MonoBehaviour
{

    //대각선 이동 참고 : http://www.devkorea.co.kr/bbs/board.php?bo_table=m03_qna&wr_id=4097

    //보라색 유령(purple ghost = pg)
    enum PurpleGhostState
    {
        Come, Find, Wait, Go //Come: 왼쪽 아래 대각선 이동 Find:왼쪽으로 이동 Wait: 대기 GO: 왼쪽 위 대각선 이동
    };
    PurpleGhostState purpleGhostState = PurpleGhostState.Come;

    private bool pgMoving = false; 
    private float pgMovingDistance = 3.0f;            // 이동 시키고 싶은 거리를 정해주면 됨
    private Vector2 pgDestinationPos;      // 이동해야할 최종 위치
    private Vector2 pgCurrentPos = new Vector2(4, 0);    // 내 위치 (텍스쳐 그려질 위치)
    bool controlPGFindMoving = true;

    bool isStart = true;  //GameManager의 gameStartCopy 이용하기

    BoxCollider2D[] box = new BoxCollider2D[2];

    private void Awake()
    {
        for(int i=0; i< this.GetComponents<BoxCollider2D>().Length; i++)
        {
            box[i] = this.GetComponents<BoxCollider2D>()[i];
            Debug.Log(box[i].size);
        }
       
    }

    private void Start()
    {
        //Invoke("ChangeMoingFalseToTrue", 3);   
    }

    void Update()
    {
        MovePurpleGhost();
        
        if (Input.GetMouseButtonDown(0))
        {
            int randomTime = 0;

            Vector2 pos = Camera.main.ScreenToWorldPoint(Input.mousePosition);
            RaycastHit2D hit = Physics2D.Raycast(pos, transform.forward, 0f);

            if (hit.collider != null)
            {
                Debug.Log("Ghost 죽이기 완료");
                Debug.Log(hit.collider.name);
                CancelInvoke("ChangeMoingFalseToTrue");
                pgMoving = false;
                purpleGhostState = PurpleGhostState.Go;
                randomTime = SetRandomTime();
                this.gameObject.transform.position = new Vector3(4, 0, 0);
                pgCurrentPos = new Vector2(4, 0);
                controlPGFindMoving = true;
                Invoke("ChangeMoingFalseToTrue", randomTime);              
                Debug.Log(randomTime + "초 후에 활성화");               
            }
        }
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
        gameObject.transform.position = new Vector3(pgCurrentPos[0], pgCurrentPos[1], 0);
    }

    //날아와서 대기(코루틴 위) -> 1.5초 (waitforseconds) -> 날아감(코루틴 아래) 
    //날아와서 대기(move함수) -> 1.5초 (Invoke) -> 날아감(move함수)
    //come -> wait -> go

    Vector2 SetRandomPos()
    {
        float[] ghostRandomPosSet = new float[6];
        int randomIndex;

        ghostRandomPosSet[5] = -0.9f;
        ghostRandomPosSet[4] = -0.25f;
        ghostRandomPosSet[3] = 0.4f;
        ghostRandomPosSet[2] = 1.05f;
        ghostRandomPosSet[1] = 1.7f;
        ghostRandomPosSet[0] = 2.3f;

        randomIndex = Random.Range(0, 6);

        return new Vector2(ghostRandomPosSet[randomIndex], -4.3f);
    }

    void ControlPurpleGhostMoving()
    {
        if(pgMoving == true) //움직이는 중
        {
            if (purpleGhostState == PurpleGhostState.Come)
            {
                //목표 지점 : 사용중인 아이템 위치
                pgDestinationPos = new Vector2(2.3f, -4.3f);
            }
            else if(purpleGhostState == PurpleGhostState.Find)
            {
                //목표 지점 : 랜덤한 아이템 위치
                if (controlPGFindMoving == true) //한번만 동작하도록 
                {
                    controlPGFindMoving = false;
                    pgDestinationPos = SetRandomPos();
                    Debug.Log("랜덤한 아이템 위치 : " + pgDestinationPos);
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
                purpleGhostState = PurpleGhostState.Find;
                //사용중인 아이템 자리에 도착하면 아이템창이 열리도록 하게 하기           
                Invoke("ChangeMoingFalseToTrue", 1);                
            }
            else if(purpleGhostState == PurpleGhostState.Find)
            {
                purpleGhostState = PurpleGhostState.Wait;
                Invoke("ChangeMoingFalseToTrue", 2);
            }
            else if (purpleGhostState == PurpleGhostState.Go)
            {
                pgDestinationPos = new Vector2(4, 0);//처음 위치
                controlPGFindMoving = true;
                Invoke("ChangeMoingFalseToTrue", SetRandomTime());
            }
        }    
    }

    void ChangeMoingFalseToTrue()
    {
        if(isStart == false)
        {
            if (purpleGhostState == PurpleGhostState.Come)
            {
                purpleGhostState = PurpleGhostState.Find;
            }
            else if (purpleGhostState == PurpleGhostState.Wait)
            {
                purpleGhostState = PurpleGhostState.Go;
            }
            else if(purpleGhostState == PurpleGhostState.Go)
            {
                purpleGhostState = PurpleGhostState.Come;
            }
        }
        else
        {
            isStart = false;
        }
       
        pgMoving = true;
    }

    int SetRandomTime()
    {
        int randomTime;
        randomTime = Random.Range(3, 6);

        return randomTime;
    }


    //purple ghost가 Wait인 경우 충돌처리 주의 collider 두개 나눠야 될듯(전체 , 머리부분만)
}//End Class
