<?php

use function PHPSTORM_META\type;

include_once (__DIR__ . '/../Models/MessageModel.php');

class MessagePresenter
{
    private $messageModel;

    public function __construct()
    {
        $this->messageModel = new MessageModel();
    }

    public function selectAllMessages()
    {
        if (!isset($_SESSION['id'])) {
            echo json_encode(['success' => false, 'redirect' => '/']);
            exit();
        }

        $messages = $this->messageModel->getAllMessages();

        if ($messages) {
            echo json_encode(['success' => true, 'messages' => $messages]);
            exit();
        } else {
            echo json_encode(['success' => false, 'message' => 'Errore nel recupero dei messaggi']);
            exit();
        }
    }

    public function deleteMessage($messageId)
    {
        $delete = $this->messageModel->deleteMessageID($messageId);

        if ($delete) {
            echo json_encode([
                'success' => true,
                'message' => 'Messaggio cancellato con successo'
            ]);
        } else {
            echo json_encode([
                'success' => false,
                'message' => 'Errore, messaggio non cancellato',
            ]);
        }
    }

    public function insertMessage($messageData)
    {
        if (empty($messageData) || empty($messageData['type']) || empty($messageData['receiver']) || empty($messageData['title']) || empty($messageData['content']) || empty($messageData['mapId'])) {
            echo json_encode(['success' => false, 'message' => 'Tutti i campi devono essere compilati.']);
            exit();
        }

        $type = $messageData['type'];
        $receiver = $messageData['receiver'];
        $title = $messageData['title'];
        $content = $messageData['content'];
        $mapId = $messageData['mapId'];

        $insert = $this->messageModel->insertMessageContent($type, $receiver, $title, $content, $mapId);

        if ($insert) {
            echo json_encode([
                'success' => true,
                'message' => 'Messaggio inviato con successo'
            ]);
        } else {
            echo json_encode([
                'success' => false,
                'message' => 'Errore, messaggio non inviato',
            ]);
        }
    }
}
