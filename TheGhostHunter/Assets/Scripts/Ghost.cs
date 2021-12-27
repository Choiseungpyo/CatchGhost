using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Ghost : MonoBehaviour
{
    //프리팹
    public GameObject PrefabGhost;

    GameObject[] GhostObj = new GameObject[3];
    float[] ghostSpeed = new float[3];
    bool[] ghostMoving = new bool[3]; //Ghost가 움직일 수 있는지 
    Vector3[] ghostResetPos = new Vector3[3];
    int[] ghostColor = new int[3]; //0:하얀색 1:빨간색 2:파란색

    private void Awake()
    {
        for(int i=0; i<3; i++)
        {
            //유령 오브젝트
            GhostObj[i] = null;

            //유령 움직임 
            ghostMoving[i] = true;

            //유령 색깔
            ghostColor[i] = 0;
        }

        //유령 스피드
        //0.1
        ghostSpeed[0] = 0.05f;
        ghostSpeed[1] = -0.03f;
        ghostSpeed[2] = 0.1f;

        //유령 재생성 위치
        ghostResetPos[0] = new Vector3(-3.5f, 3.5f, 0);
        ghostResetPos[1] = new Vector3(3.5f, 1, 0);
        ghostResetPos[2] = new Vector3(-3.5f, -1.5f, 0);     
    }

    // Start is called before the first frame update
    void Start()
    {
        MakeGhost();
    }

    // Update is called once per frame
    void Update()
    {
        MoveGhost();
        KillGhost();
    }


    void MakeGhost()
    {
        GhostObj[0] = Instantiate(PrefabGhost, new Vector3(-3.5f, 3.5f, 0), Quaternion.identity);
        GhostObj[0].name = "Ghost1";
        GhostObj[0].GetComponent<SpriteRenderer>().flipX = true;

        GhostObj[1] = Instantiate(PrefabGhost, new Vector3(3.5f, 1, 0), Quaternion.identity);
        GhostObj[1].name = "Ghost2";

        GhostObj[2] = Instantiate(PrefabGhost, new Vector3(-3.5f, -1.5f, 0), Quaternion.identity);
        GhostObj[2].name = "Ghost3";
        GhostObj[2].GetComponent<SpriteRenderer>().flipX = true;
    }

    void MoveGhost()
    {
        for(int i=0; i<3; i++)
        {
            if(ghostMoving[i] == true)
            {
                GhostObj[i].transform.position += new Vector3(ghostSpeed[i], 0, 0);
                CheckGhostPos();
            }
        }  
    }

    void CheckGhostPos() //유령이 화면 바깥으로 나갔는지 확인한다.
    {
        for(int i=0; i<3; i++)
        {
            if(i==1)//우->좌로 움직이는 유령
            {
                if (GhostObj[i].transform.position.x <= -3.5)
                {
                    ghostMoving[i] = false; //움직임을 멈춘다.
                    GhostObj[i].GetComponent<SpriteRenderer>().color = SetRandomGhostColor(i);
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
                    GhostObj[i].GetComponent<SpriteRenderer>().color = SetRandomGhostColor(i);
                    GhostObj[i].transform.position = ghostResetPos[i];
                    SetRandomGhostSpeed(i);
                    StartCoroutine(ActivateGhostMoving(i)); 
                }
            }     
        }    
    }

    int SetRandomGhostTimeToAppear() //유령이 나타날 랜덤한 시간을 정한다.
    {
        int ghostRandomTime;
        ghostRandomTime = Random.Range(1, 5); //1~4
        return ghostRandomTime;
    }
    
    IEnumerator ActivateGhostMoving(int ghostNum) //유령의 움직임을 n초 후에 활성화시킨다.
    {
        int ghostRandTime;
        ghostRandTime = SetRandomGhostTimeToAppear();
        //Debug.Log("Ghost" + ghostNum + "이 " + ghostRandTime + "후에 재생성됩니다.");
        yield return new WaitForSeconds(ghostRandTime); 

        ghostMoving[ghostNum] = true; //랜덤한 시간 뒤에 다시 움직일 수 있게 하기
    }


    Color SetRandomGhostColor(int ghostNum) //유령의 색깔 랜덤으로 정하기
    {
        Color ghostRandomColor;
        int ghostColorNum;

        ghostColorNum = Random.Range(0, 3); //0:하얀색 1:빨간색 2:파란색

        switch(ghostColorNum)
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
        
        if(ghostNum ==1)
        {
            ghostSpeed[ghostNum] = -ghostSpeedRandomSet[randomIndex]; //0~7
        }
        else
        {
            ghostSpeed[ghostNum] = ghostSpeedRandomSet[randomIndex]; //0~7
        }
        //Debug.Log("Ghost" + ghostNum + " 스피드: " + ghostSpeed[ghostNum]);
    }


    void KillGhost()
    {
        if(Input.GetMouseButtonDown(0))
        {
            Vector2 pos = Camera.main.ScreenToWorldPoint(Input.mousePosition);
            RaycastHit2D hit = Physics2D.Raycast(pos, transform.forward, 0f);
            if (hit.collider != null)
            {
                int ghostNum;

                ghostNum = returnGhostNum(hit.collider.name);
                //Debug.Log(hit.collider.name);
                if(CompareGhostColorToBullet(ghostNum) == true)
                {
                    Debug.Log(hit.collider.name + "을 죽였습니다.");
                    ResetGhostAttribute(ghostNum);
                }
            }
        }
    }

    bool CompareGhostColorToBullet(int ghostNum)
    {
        if(Item.instance.ChangeItemStringToInt(Item.instance.playerItem[0]) == ghostColor[ghostNum])
        {
            return true;   
        }
        return false;
    }

    int returnGhostNum(string ghostName)
    {
        int ghostNum;
        switch(ghostName)
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
            default:
                ghostNum = -1;
                break;
        }

        return ghostNum;
    }


    void ResetGhostAttribute(int ghostNum) //유령이 죽었을 시 유령의 속성값 변경
    {
        GhostObj[ghostNum].GetComponent<SpriteRenderer>().color = SetRandomGhostColor(ghostNum);
        SetRandomGhostSpeed(ghostNum);
        GhostObj[ghostNum].transform.position = ghostResetPos[ghostNum];
    }
}//End Class
