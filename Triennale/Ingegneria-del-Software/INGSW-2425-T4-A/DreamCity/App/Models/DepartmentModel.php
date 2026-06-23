<?php

class DepartmentModel
{
    private $pdo;

    public function __construct()
    {
        include_once(__DIR__ . '/../../Config/config.php');

        $this->pdo = $pdo;

        if (!$this->pdo) {
            die('Connessione fallita: ' . !$this->pdo);
        }
    }

    // Crea un nuovo utente
    public function updateBudgets($mapId, $budget, $selectedUser)
    {
        $getOtherBudget = "SELECT budget FROM Departments d WHERE d.Dmap_id = $mapId AND d.user_id = $selectedUser";
        $budgetResult = $this->pdo->query($getOtherBudget);

        if ($budgetResult->rowCount() > 0) {
            $row = $budgetResult->fetch(PDO::FETCH_ASSOC);
            $newBudget = $row['budget'] + $budget;

            $updateOtherUser = "UPDATE Departments SET budget = $newBudget WHERE Dmap_id = $mapId AND user_id = $selectedUser";
            $res = $this->pdo->query($updateOtherUser);

            if ($res) {
                return true;
            }
            return false;
        }
        return false;
    }

    public function updateBudget($mapId, $budget)
    {
        $userId = $_SESSION['id'];

        $sql = "UPDATE Departments SET budget = $budget WHERE Dmap_id = $mapId AND user_id = $userId";
        $res = $this->pdo->query($sql);

        if ($res) {
            return true;
        }
        return false;
    }
}
