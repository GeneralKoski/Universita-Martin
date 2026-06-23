<?php
session_start();
if (!isset($_SESSION['id'])) {
    header('Location: /');
    exit();
}

include_once ('../App/Presenters/MessagePresenter.php');

// Crea l'istanza del presenter
$messagePresenter = new MessagePresenter();

// Ottieni il percorso richiesto
$request = explode('/', trim($_SERVER['REQUEST_URI'], '/'));
if (isset($request[3])) {
    $message = $request[3];
}
$request = $request[2];

switch ($request) {
    case 'getMessages':
        if ($_SERVER['REQUEST_METHOD'] === 'GET') {
            $messagePresenter->selectAllMessages();
        }
        break;
    case 'deleteMessage':
        if ($_SERVER['REQUEST_METHOD'] === 'DELETE') {
            $messagePresenter->deleteMessage($message);
        }
        break;
    case 'insertMessage':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $messageData = json_decode(file_get_contents('php://input'), true);
            $messagePresenter->insertMessage($messageData);
        }
        break;

    default:
        echo json_encode(['success' => false, 'message' => 'Route non trovata per Messages']);
        break;
}