using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class SpawnPF : MonoBehaviour
{
    public Transform goal; //goal is a random position of road transform
    public GameObject road; //the road that the car will go towards
    public NavMeshAgent agent;
    public GameObject car;
    public Transform start;
    public Transform end;

    void Update()
    {
        agent.destination = goal.position;
        if (car.transform.position == goal.position)
        {
            SetGoal();
        }
    }
    private void Start()
    {
        SetGoal();
        start = car.transform;

        car.SetActive(true);
        car.transform.position = start.transform.position;
        agent = GetComponent<NavMeshAgent>();
    }

    private void SetGoal()
    {
        //set goal transform
        int x = Random.Range(0, 216); //randomizes the street
        GameObject go = road; //sets go of road
        goal = go.transform.GetChild(x); //get random child road
        end.transform.position = goal.position;


    }

}
