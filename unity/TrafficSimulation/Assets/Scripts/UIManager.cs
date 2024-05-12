using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UIManager : MonoBehaviour
{
    public delegate void RestartGame();
    public static event RestartGame onRestartGame; 

    public void ButtonClicked(int id)
    {
        switch(id)
        {
            case 0:
                Debug.Log($"Northridge clicked");
                onRestartGame();
                break;
        }
    }
}
