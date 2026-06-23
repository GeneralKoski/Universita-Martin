<?php

class ClickModel
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

    // Crea un nuovo utente
    public function insertClick($mapId)
    {
        $userId = $_SESSION['id'];
        $sql = "SELECT * FROM MapClicks WHERE Cmap_id = $mapId AND Cuser_id = $userId";
        $res = $this->pdo->query($sql);

        if ($res->rowCount() > 0) {
            return false;
        } else {
            $sql = "SELECT * FROM Departments d WHERE d.Dmap_id = $mapId AND d.user_id = $userId";
            $res = $this->pdo->query($sql);

            if ($res->rowCount() > 0) {
                $sql = "INSERT INTO MapClicks (Cmap_id, Cuser_id) VALUES ($mapId, $userId)";
                $res = $this->pdo->query($sql);

                if ($res) {
                    return true;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        }
    }

    public function removeClick($mapId)
    {
        $userId = $_SESSION['id'];
        $sql = "SELECT * FROM MapClicks WHERE Cmap_id = $mapId AND Cuser_id = $userId";
        $res = $this->pdo->query($sql);

        if ($res->rowCount() > 0) {
            $sql = "DELETE FROM MapClicks WHERE Cmap_id = $mapId AND Cuser_id = $userId";
            $res = $this->pdo->query($sql);
            if ($res) {
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }
}