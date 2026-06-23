<?php
session_start();

include_once('../App/Presenters/UserPresenter.php');

// Crea l'istanza del presenter
$userPresenter = new UserPresenter();

// Ottieni il percorso richiesto
$request = explode('/', trim($_SERVER['REQUEST_URI'], '/'));
if (isset($request[3])) {
    $mapId = $request[3];
}
$request = $request[2];

if ($request !== 'authenticateUser' && $request !== 'createUser' && !isset($_SESSION['id'])) {
    header('Location: /');
    exit();
}

switch ($request) {
    case 'createUser':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $userPresenter->registerUser();
        }
        break;
    case 'authenticateUser':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $userPresenter->loginUser();
        }
        break;
    case 'deauthenticateUser':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $userPresenter->logoutUser();
        }
        break;
    case 'getUsers':
        if ($_SERVER['REQUEST_METHOD'] === 'GET') {
            $userPresenter->showUsers();
        }
        break;
    case 'detailsUser':
        if ($_SERVER['REQUEST_METHOD'] === 'GET') {
            $userPresenter->userDetails($mapId);
        }
        break;

    default:
        echo json_encode(['success' => false, 'message' => 'Route non trovata per Users']);
        break;
}