using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class PathFind : MonoBehaviour
{
    public Transform goal;
    public NavMeshAgent agent;
    //public GameObject Menu;
    public GameObject Sedan;
    public GameObject start;
    public GameObject end;

    void Start()
    {
        Sedan.SetActive(false);
        agent = GetComponent<NavMeshAgent>();
    }

    void Update()
    {
        agent.destination = goal.position; 
    }

    private void PathSet_onRestartGame()
    {
        Sedan.SetActive(true);
        Sedan.transform.position = start.transform.position + new Vector3(0, 1, 0);
        Debug.Log($"sedan now active");
    }

    private void OnEnable()
    {
        PathSet.onRestartGame += PathSet_onRestartGame;
    }
}
