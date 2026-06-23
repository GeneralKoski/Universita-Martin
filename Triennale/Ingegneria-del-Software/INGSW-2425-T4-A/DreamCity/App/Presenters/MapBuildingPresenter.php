<?php
include_once (__DIR__ . '/../Models/MapBuildingModel.php');

class MapBuildingPresenter
{
    private $mapBuildingModel;

    public function __construct()
    {
        $this->mapBuildingModel = new MapBuildingModel();
    }

    public function loadMapBuilding($mapId)
    {
        $buildings = $this->mapBuildingModel->loadBuilding($mapId);
        if ($buildings) {
            echo json_encode(['success' => true, 'message' => 'Strutture caricate con successo', 'buildings' => $buildings]);
        } else {
            echo json_encode(['success' => false, 'message' => 'Errore nel caricamento delle strutture']);
        }
    }

    public function saveMapBuilding($mapId, $x, $y, $buildingType, $rotated)
    {
        $save = $this->mapBuildingModel->saveBuilding($mapId, $x, $y, $buildingType, $rotated);
        if ($save) {
            echo json_encode(['success' => true, 'message' => 'Struttura salvata con successo', 'x' => $x, 'y' => $y]);
        } else {
            echo json_encode(['success' => false, 'message' => 'Errore nel salvataggio della struttura']);
        }
    }

    public function deleteMapBuilding($mapId, $x, $y)
    {
        $delete = $this->mapBuildingModel->deleteBuilding($mapId, $x, $y);
        if ($delete) {
            echo json_encode(['success' => true, 'message' => 'Struttura cancellata con successo']);
        } else {
            echo json_encode(['success' => false, 'message' => 'Errore nella cancellazione della struttura']);
        }
    }
}
