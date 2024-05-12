using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class PathSet : MonoBehaviour
{
    public delegate void RestartGame();
    public static event RestartGame onRestartGame;
    RaycastHit tmpHitHighlight;
    int flag = 0;
    public GameObject startID;
    public GameObject endID;
    public GameObject UI;

    public void ButtonClicked(int id)
    {
        switch (id)
        {
            case 0:
                Debug.Log($"Start selected");
                flag = 0;
                break;

            case 1:
                Debug.Log($"Destination selected");
                flag = 1;
                break;

            case 2:
                if (startID.transform.position !=  new Vector3(-209, 36, 567) && endID.transform.position != new Vector3(-158, 36, 567))
                {
                    Debug.Log($"Move on");
                    onRestartGame();
                    UI.SetActive(false);

                } else { Debug.Log($"Need to set both flags.");  }
                break;

        }
    }

    void Start()
    {
        
    }

    void Update()
    {
        //Debug.Log($"Check");

        Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
        RaycastHit tmpHitHighlight;


        if (Input.GetMouseButton(0)) //left click
        {
            //Debug.Log($"Click"); confirmed that this works

            if (Physics.Raycast(ray, out tmpHitHighlight, 1000)) //clicks on block
            {
                GameObject hitObject = tmpHitHighlight.collider.gameObject;
                if (hitObject.name == "Plane") { Debug.Log($"Invalid Choice"); }
                else
                {
                    switch (flag)
                    {
                        case 0: //starting destination flag
                            startID.transform.position = hitObject.transform.position + new Vector3(0, 1, 0); ;
                            Debug.Log($"Start Set: " + hitObject.name);
                            break;
                        case 1: //ending destination flag
                            endID.transform.position = hitObject.transform.position + new Vector3(0, 1, 0); ;
                            Debug.Log($"Destination Set: " + hitObject.name);
                            break;
                    }
                }

            }
        }
    }
}

