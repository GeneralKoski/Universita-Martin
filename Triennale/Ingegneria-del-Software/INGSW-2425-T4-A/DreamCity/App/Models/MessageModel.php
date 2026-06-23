<?php

class MessageModel
{
    private $pdo;

    public function __construct()
    {
        include_once (__DIR__ . '/../../Config/config.php');

        $this->pdo = $pdo;

        if (!$this->pdo) {
            die('Connessione fallita: ' . !$this->pdo);
        }
    }

    public function getAllMessages()
    {
        $userId = $_SESSION['id'];
        $sql = "SELECT me.id, me.title, me.content, me.type, (SELECT u.username FROM Users u WHERE u.id = me.sender_id) as sender, me.sender_id,
        (SELECT u.username FROM Users u WHERE u.id = me.receiver_id) as receiver, me.Mmap_id as mapID FROM Messages me WHERE me.receiver_id = $userId ORDER BY me.id DESC";
        $res = $this->pdo->query($sql);

        $messages = [];

        if ($res) {
            while ($row = $res->fetch(PDO::FETCH_ASSOC)) {
                $messages[] = $row;
            }
        }        

        return $messages;
    }

    public function deleteMessageID($messageId)
    {
        $sql = "DELETE FROM Messages WHERE id = $messageId";
        $res = $this->pdo->query($sql);

        if (!$res) {
            echo $this->pdo . '<br>';
            return false;
        }
        return true;
    }

    public function insertMessageContent($type, $receiver, $title, $content, $mapId)
    {
        $userId = $_SESSION['id'];
        $sql = "INSERT INTO Messages (title, content, type, sender_id, receiver_id, Mmap_id) VALUES ('$title', '$content', '$type', $userId, $receiver, $mapId)";
        $res = $this->pdo->query($sql);

        if (!$res) {
            return false;
        } else {
            return true;
        }
    }
}
