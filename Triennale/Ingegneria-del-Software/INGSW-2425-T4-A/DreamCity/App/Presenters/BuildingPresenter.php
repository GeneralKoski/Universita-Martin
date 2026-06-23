<?php
include_once (__DIR__ . '/../Models/BuildingModel.php');

class BuildingPresenter
{
    private $buildingModel;

    public function __construct()
    {
        $this->buildingModel = new BuildingModel();
    }

    public function selectBuildings()
    {
        // Cancella la mappa dal Model
        $buildings = $this->buildingModel->selectBuildings();
        if ($buildings) {
            echo json_encode($buildings);
        } else {
            echo json_encode(['success' => false, 'message' => 'Errore nel recupero degli edifici']);
        }
    }

    public function selectUserBuildings($mapId)
    {
        // Cancella la mappa dal Model
        $userBuildings = $this->buildingModel->selectUserBuildings($mapId);
        if ($userBuildings) {
            echo json_encode($userBuildings);
        } else {
            echo json_encode(['success' => false, 'message' => 'Errore nel recupero degli edifici']);
        }
    }
}