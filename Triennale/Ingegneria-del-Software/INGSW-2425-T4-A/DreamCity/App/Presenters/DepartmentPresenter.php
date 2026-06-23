<?php
include_once (__DIR__ . '/../Models/DepartmentModel.php');

class DepartmentPresenter
{
    private $departmentModel;

    public function __construct()
    {
        $this->departmentModel = new DepartmentModel();
    }

    public function updateBudgets($mapId, $budget, $selectedUser)
    {
        // Cancella la mappa dal Model
        $update = $this->departmentModel->updateBudgets($mapId, $budget, $selectedUser);
        if ($update) {
            echo json_encode(['success' => true, 'message' => 'Budget aggiornati con successo']);
        } else {
            echo json_encode(['success' => false, 'message' => "Errore nell'aggiornamento dei budget"]);
        }
    }

    public function updateBudget($mapId, $budget)
    {
        // Cancella la mappa dal Model
        $update = $this->departmentModel->updateBudget($mapId, $budget);
        if ($update) {
            echo json_encode(['success' => true, 'message' => 'Budget utente aggiornato con successo']);
        } else {
            echo json_encode(['success' => false, 'message' => "Errore nell'aggiornamento del budget dell'utente"]);
        }
    }
}