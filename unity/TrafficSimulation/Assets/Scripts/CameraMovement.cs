using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraMovement : MonoBehaviour
{
    // Start is called before the first frame update
    public GameObject player;
    private Vector3 offset;


    void Start()
    {
        offset = new Vector3(0, 50, 0); //sets how far camera is
    }

    // Update is called once per frame
    void Update()
    {
        if (player.activeSelf == true) { transform.position = player.transform.position + offset; }

    }
}
