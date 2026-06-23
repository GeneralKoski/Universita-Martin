<?php
session_start();
if (!isset($_SESSION['id'])) {
    header('Location: /');
    exit();
}

include_once ('../App/Presenters/DepartmentPresenter.php');

// Crea l'istanza del presenter
$departmentPresenter = new DepartmentPresenter();

// Ottieni il percorso richiesto
$request = explode('/', trim($_SERVER['REQUEST_URI'], '/'));
if (isset($request[3])) {
    $mapId = $request[3];
}
if (isset($request[4])) {
    $budget = $request[4];
}
if (isset($request[5])) {
    $selectedUser = $request[5];
}
$request = $request[2];

switch ($request) {
    case 'updateBudgets':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $departmentPresenter->updateBudgets($mapId, $budget, $selectedUser);
        }
        break;
    case 'updateBudget':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $departmentPresenter->updateBudget($mapId, $budget);
        }
        break;

    default:
        echo json_encode(['success' => false, 'message' => 'Route non trovata per Departments']);
        break;
}