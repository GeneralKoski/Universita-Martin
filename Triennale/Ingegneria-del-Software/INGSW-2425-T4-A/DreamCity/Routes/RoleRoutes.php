<?php
session_start();
if (!isset($_SESSION['id'])) {
    header('Location: /');
    exit();
}

include_once('../App/Presenters/RolePresenter.php');

// Crea l'istanza del presenter
$rolePresenter = new RolePresenter();

// Ottieni il percorso richiesto
$request = explode('/', trim($_SERVER['REQUEST_URI'], '/'));

if ($request[0] === "selectRoleView" && $_SERVER['REQUEST_METHOD'] === 'GET') {
    include_once('../App/Views/pages/selectRole.html');
    return;
}

$map = $request[3];
$request = $request[2];


switch ($request) {
    case 'availableRoles':
        if ($_SERVER['REQUEST_METHOD'] === 'GET') {
            $rolePresenter->availableRoles($map);
        }
        break;
    case 'addRole':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $role = json_decode(file_get_contents('php://input'), true);
            $rolePresenter->addRole($map, $role);
        }
        break;
    case 'changeRole':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $data = json_decode(file_get_contents('php://input'), true);
            $senderId = $data['sender_id'];
            $messageId = $data['message_id'];
            $rolePresenter->changeRole($map, $senderId, $messageId);
        }
        break;

    default:
        echo json_encode(['success' => false, 'message' => 'Route non trovata per Roles']);
        break;
}