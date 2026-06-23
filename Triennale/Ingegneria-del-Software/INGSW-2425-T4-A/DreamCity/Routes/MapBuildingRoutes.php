<?php
session_start();
if (!isset($_SESSION['id'])) {
    header('Location: /');
    exit();
}

include_once ('../App/Presenters/MapBuildingPresenter.php');

// Crea l'istanza del presenter
$mapBuildingPresenter = new MapBuildingPresenter();

// Ottieni il percorso richiesto
$request = explode('/', trim($_SERVER['REQUEST_URI'], '/'));

$mapId = $request[3];

$request = $request[2];

switch ($request) {
    case 'loadBuildings':
        if ($_SERVER['REQUEST_METHOD'] === 'GET') {
            $mapBuildingPresenter->loadMapBuilding($mapId);
        }
        break;
    case 'saveBuilding':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $data = json_decode(file_get_contents('php://input'), true);
            $mapBuildingPresenter->saveMapBuilding($mapId, $data['x'], $data['y'], $data['building_type'], $data['rotated']);
        }
        break;
    case 'deleteBuilding':
        if ($_SERVER['REQUEST_METHOD'] === 'DELETE') {
            $data = json_decode(file_get_contents('php://input'), true);
            $mapBuildingPresenter->deleteMapBuilding($mapId, $data['x'], $data['y']);
        }
        break;

    default:
        echo json_encode(['success' => false, 'message' => 'Route non trovata per MapBuilding']);
        break;
}
