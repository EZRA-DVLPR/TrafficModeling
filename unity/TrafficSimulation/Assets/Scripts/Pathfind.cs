using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class playerwalk : MonoBehaviour
{
    public Transform goal;
    public NavMeshAgent agent;

    void Start()
    {
        int y = -1;
        agent = GetComponent<NavMeshAgent>();
    }

    void Update()
    {
        agent.destination = goal.position; 
    }
}
