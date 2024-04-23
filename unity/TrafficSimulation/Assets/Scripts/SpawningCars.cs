using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UIElements;

public class SpawningCars : MonoBehaviour
{
    public GameObject car;


    // Start is called before the first frame update
    void Start()
    {
        var go = GameObject.Instantiate(car, Vector3.zero, Quaternion.identity);
        var position = transform.position;

        for (int i = 0; i < 5; i++)
        {
            go.transform.position = position;
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
