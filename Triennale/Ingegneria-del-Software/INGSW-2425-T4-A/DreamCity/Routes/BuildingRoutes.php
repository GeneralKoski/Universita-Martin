<?php
session_start();
if (!isset($_SESSION['id'])) {
    header('Location: /');
    exit();
}

include_once ('../App/Presenters/BuildingPresenter.php');

// Crea l'istanza del presenter
$buildingPresenter = new BuildingPresenter();

// Ottieni il percorso richiesto
$request = explode('/', trim($_SERVER['REQUEST_URI'], '/'));
if (isset($request[3])) {
    $mapId = $request[3];
}
$request = $request[2];

switch ($request) {
    case 'selectBuildings':
        if ($_SERVER['REQUEST_METHOD'] === 'GET') {
            $buildingPresenter->selectBuildings();
        }
        break;
    case 'selectUserBuildings':
        if ($_SERVER['REQUEST_METHOD'] === 'GET') {
            $buildingPresenter->selectUserBuildings($mapId);
        }
        break;

    default:
        echo json_encode(['success' => false, 'message' => 'Route non trovata per Buildings']);
        break;
}