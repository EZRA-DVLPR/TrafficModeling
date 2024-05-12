using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class PathFind : MonoBehaviour
{
    public Transform goal;
    public NavMeshAgent agent;
    public GameObject Sedan;
    public GameObject start;
    public GameObject end;
    public GameObject arrived;

    void Start()
    {
       // Sedan.SetActive(false);
        agent = GetComponent<NavMeshAgent>();
    }

    void Update()
    {
        agent.destination = goal.position; 
    }

    public void OnTriggerEnter(Collider collision)
    {
        if (collision.tag == "end")
        {
            arrived.SetActive(true);
            Debug.Log($"Arrived");
        }
    }
    private void PathSet_onRestartGame()
    {
        Sedan.SetActive(true);
        Sedan.transform.position = start.transform.position;
        agent = GetComponent<NavMeshAgent>();
        Update();
        Debug.Log($"sedan now active");
    }

    private void OnEnable()
    {
        PathSet.onRestartGame += PathSet_onRestartGame;
    }
}
