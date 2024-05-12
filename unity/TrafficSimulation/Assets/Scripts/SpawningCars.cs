using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.UIElements;

public class SpawningCars : MonoBehaviour
{
    public GameObject car;
    public GameObject roadT;
    public GameObject roadL;
    public Transform pos;

    private void PathSet_onRestartGame()
    {
        car.SetActive(true);

        GameObject go = roadT;
        //Debug.Log(go.name + " has " + go.transform.childCount + " children");
        GameObject go2 = roadL;
        //Debug.Log(go2.name + " has " + go2.transform.childCount + " children");

        int x = Random.Range(0, 277);
        int y = Random.Range(0, 517);

        for (int i = 0; i < 20; i++)
         {
            //get random position on gameobject road 
            pos = go.transform.GetChild(x);
            var newCar = Instantiate(car);

            newCar.transform.position = pos.transform.position + new Vector3(0, 2, 0);
            Debug.Log($"Made car at: " + pos);
            x = Random.Range(0, 277);

            
        }
    }

    public void Update()
    {
        //if car made it to destination
            //make new destination
    }

    private void OnEnable()
    {
        PathSet.onRestartGame += PathSet_onRestartGame;
    }
}
