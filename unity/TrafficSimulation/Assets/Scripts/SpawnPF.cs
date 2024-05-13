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
    public GameObject start;
    public GameObject end;
   // public GameObject arrived;

    void Update()
    {
        agent.destination = goal.position;
        if (car.transform.position == goal.transform.position)
        {
            SetGoal();
        }
    }
    private void PathSet_onRestartGame()
    {
        SetGoal();

        car.SetActive(true);
        car.transform.position = start.transform.position;
        agent = GetComponent<NavMeshAgent>();
        Update();
        Debug.Log($"spawned car now active");
    }

    private void SetGoal()
    {
        //set goal transform
        int x = Random.Range(0, 517); //randomizes the street
        GameObject go = road; //sets go of road
        goal = go.transform.GetChild(x); //get random child road
    }

    private void OnEnable()
    {
        PathSet.onRestartGame += PathSet_onRestartGame;
    }
}
