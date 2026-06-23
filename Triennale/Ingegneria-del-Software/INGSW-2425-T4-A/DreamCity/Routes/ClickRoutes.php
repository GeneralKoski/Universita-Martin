<?php
session_start();
if (!isset($_SESSION['id'])) {
    header('Location: /');
    exit();
}

include_once ('../App/Presenters/ClickPresenter.php');

// Crea l'istanza del presenter
$clickPresenter = new ClickPresenter();

// Ottieni il percorso richiesto
$request = explode('/', trim($_SERVER['REQUEST_URI'], '/'));
if (isset($request[3])) {
    $mapId = $request[3];
}
$request = $request[2];

switch ($request) {
    case 'registerClick':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $clickPresenter->registerClick($mapId);
        }
        break;
    case 'deleteClick':
        if ($_SERVER['REQUEST_METHOD'] === 'DELETE') {
            $clickPresenter->deleteClick($mapId);
        }
        break;

    default:
        echo json_encode(['success' => false, 'message' => 'Route non trovata per Click']);
        break;
}