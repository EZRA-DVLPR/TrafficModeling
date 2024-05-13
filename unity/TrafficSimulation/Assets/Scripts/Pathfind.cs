using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class PathFind : MonoBehaviour
{
    public Transform goal;
    public NavMeshAgent agent;
    public GameObject Sedan;
    public Transform start;
    public GameObject end;
    public GameObject arrived;
    private PathSet startcar;

    void Update()
    {
        agent.destination = goal.position; 
        if (Sedan.transform.position == goal.position) {
            arrived.SetActive(true);
            Debug.Log($"Arrived");
        }
    }

    private void Start()
    {
        Sedan.SetActive(false);
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

        //get car position from pathset
        startcar = start.GetComponent<PathSet>();
        //start.transform.position = startcar.carstart.position;
        Debug.Log($"start.transform.position" + start.transform.position);

        Sedan.transform.position = start.transform.position;
        agent = GetComponent<NavMeshAgent>();

        Update();

        Debug.Log($"sedan now active");
    }

    private void OnEnable()
    {
        PathSet.OnStartGame += PathSet_onRestartGame;
    }
}
