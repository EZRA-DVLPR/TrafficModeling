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

    private void Start()
    {

        GameObject go = roadT;
        GameObject go2 = roadL;

        int x = Random.Range(0, 277);

        for (int i = 0; i < 50; i++)
         {
            randomCar();
            car.SetActive(true);

            //get random position on gameobject road 
            pos = go.transform.GetChild(x);
            var newCar = Instantiate(car);

            newCar.transform.position = pos.transform.position + new Vector3(0, 2, 0);
            x = Random.Range(0, 277);
        }
    }

    public void randomCar()
    {
        GameObject[] cars = GameObject.FindGameObjectsWithTag("car");
        int carx = Random.Range(0, 4);
        car = cars[carx];
    }

}
