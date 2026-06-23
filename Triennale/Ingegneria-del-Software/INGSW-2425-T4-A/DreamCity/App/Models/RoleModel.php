<?php

class RoleModel
{
    private $pdo;

    public function __construct()
    {
        include_once(__DIR__ . '/../../Config/config.php');

        $this->pdo = $pdo;

        if (!$this->pdo) {
            die('Connessione fallita: ' . !$this->pdo);
        }
    }

    public function getAvailableRoles($mapId)
    {
        $sql = "SELECT r.name FROM Roles r WHERE r.id NOT IN (SELECT Drole_id FROM Departments d WHERE Dmap_id = $mapId)";
        $result = $this->pdo->query($sql);

        if ($result->rowCount() > 0) {
            while ($row = $result->fetch(PDO::FETCH_ASSOC)) {
                $roles[] = $row['name'];
            }
            return $roles;
        } else {
            return false;
        }
    }

    public function addRoleUser($mapId, $role)
    {
        $userId = $_SESSION['id'];

        $sql = "SELECT r.id FROM Roles r WHERE r.name = '$role'";
        $res = $this->pdo->query($sql);

        $roleId = $res->fetch(PDO::FETCH_ASSOC);
        $roleId = $roleId['id'];

        $sql = "INSERT INTO Departments (user_id, Dmap_id, Drole_id, budget) VALUES ('$userId', '$mapId', '$roleId', 10000)";
        $res = $this->pdo->query($sql);

        if ($res) {
            return true;
        } else {
            return false;
        }
    }

    public function changeRole($mapId, $senderId, $messageId)
    {
        $userId = $_SESSION['id'];

        // Recupera il Drole_id per l'utente loggato
        $sql = "SELECT Drole_id FROM Departments WHERE Dmap_id = $mapId AND user_id = $userId";
        $res = $this->pdo->query($sql);
        $userRole = $res->fetch(PDO::FETCH_ASSOC)['Drole_id'];

        // Recupera il Drole_id per il sender
        $sql = "SELECT Drole_id FROM Departments WHERE Dmap_id = $mapId AND user_id = $senderId";
        $res = $this->pdo->query($sql);
        $senderRole = $res->fetch(PDO::FETCH_ASSOC)['Drole_id'];

        if (empty($userRole) || empty($senderRole)) {
            return false;
        }

        // Imposta il ruolo del sender per l'utente loggato
        $sql = "UPDATE Departments SET Drole_id = $senderRole WHERE Dmap_id = $mapId AND user_id = $userId";
        $res = $this->pdo->query($sql);
        if (!$res) {
            return false;
        }

        // Imposta il ruolo dell'utente loggato per il sender
        $sql = "UPDATE Departments SET Drole_id = $userRole WHERE Dmap_id = $mapId AND user_id = $senderId";
        $res = $this->pdo->query($sql);
        if (!$res) {
            return false;
        }

        // Cancella il messaggio dalla tabella Message
        $sql = "DELETE FROM Messages WHERE id = $messageId";
        $res = $this->pdo->query($sql);
        if (!$res) {
            return false;
        }

        return true;
    }
}