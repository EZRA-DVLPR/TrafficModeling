using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class playerwalk : MonoBehaviour
{
    public Transform goal;
    public NavMeshAgent agent;
    public GameObject Menu;
    public GameObject Sedan;

    void Start()
    {
        Sedan.SetActive(false);
        agent = GetComponent<NavMeshAgent>();
    }

    void Update()
    {
        agent.destination = goal.position; 
    }

    private void UIManager_onRestartGame()
    {
        Sedan.SetActive(true);
    }

    private void OnEnable()
    {
        UIManager.onRestartGame += UIManager_onRestartGame;
    }
}
