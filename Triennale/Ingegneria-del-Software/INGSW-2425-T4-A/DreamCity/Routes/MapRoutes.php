<?php
session_start();
if (!isset($_SESSION['id'])) {
    header('Location: /');
    exit();
}

if ($_SERVER['REQUEST_URI'] === "/mapChoiceView" && $_SERVER['REQUEST_METHOD'] === 'GET') {
    include_once('../App/Views/pages/mapChoice.html');
    return;
}
if ($_SERVER['REQUEST_URI'] === "/createMapView" && $_SERVER['REQUEST_METHOD'] === 'GET') {
    include_once('../App/Views/pages/createMap.html');
    return;
}

include_once('../App/Presenters/MapPresenter.php');

// Crea l'istanza del presenter
$mapPresenter = new MapPresenter();

// Ottieni il percorso richiesto
$request = explode('/', trim($_SERVER['REQUEST_URI'], '/'));

if ($request[0] === "mapView" && $_SERVER['REQUEST_METHOD'] === 'GET') {
    include_once('../App/Views/pages/map.html');
    return;
}

if (isset($request[3])) {
    $mapId = $request[3];
}
if (isset($request[4])) {
    $value = $request[4];
}
$request = $request[2];

switch ($request) {
    case 'createMap':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $mapPresenter->createMap();
        }
        break;
    case 'getMaps':
        if ($_SERVER['REQUEST_METHOD'] === 'GET') {
            $mapPresenter->showMaps();
        }
        break;
    case 'deleteMap':
        if ($_SERVER['REQUEST_METHOD'] === 'DELETE') {
            $mapPresenter->deleteMap($mapId);
        }
        break;
    case 'refreshLastLogin':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $mapPresenter->updateMapLogin($mapId);
        }
        break;
    case 'mapUsers':
        if ($_SERVER['REQUEST_METHOD'] === 'GET') {
            $mapPresenter->mapUsers($mapId);
        }
        break;
    case 'mapDetails':
        if ($_SERVER['REQUEST_METHOD'] === 'GET') {
            $mapPresenter->mapDetails($mapId);
        }
        break;
    case 'updateCitizens':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $mapPresenter->updateCitizens($mapId, $value);
        }
        break;
    case 'updateHappiness':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $mapPresenter->updateHappiness($mapId, $value);
        }
        break;

    default:
        echo json_encode(['success' => false, 'message' => 'Route non trovata per Maps']);
        break;
}
