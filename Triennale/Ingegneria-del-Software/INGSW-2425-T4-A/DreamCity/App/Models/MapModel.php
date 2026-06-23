<?php

class MapModel
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

    // Crea un nuovo utente
    public function createMap($nome, $descrizione, $avatarPath)
    {
        // Inserisci i dati della mappa nel database
        $sql = "INSERT INTO Maps (name, description, image, happiness) VALUES ('$nome', '$descrizione', '$avatarPath', '0')";
        $res = $this->pdo->query($sql);

        if (!$res) {
            echo 'Errore nel salvataggio della mappa: ' . $this->pdo;
            return false;
        }

        return true;
    }

    // Recupera un elenco di mappe
    public function getMaps()
    {
        $sql = 'SELECT * FROM Maps m LEFT JOIN (SELECT Dmap_id, COUNT(*)  as totalUsers FROM Departments GROUP BY Dmap_id) d ON d.Dmap_id = m.id
                LEFT JOIN (SELECT Cmap_id, COUNT(*) as clickCount FROM MapClicks GROUP BY Cmap_id) mc ON mc.Cmap_id = m.id ORDER BY m.happiness DESC;';
        $result = $this->pdo->query($sql);
        $maps = [];

        if ($result->rowCount() > 0) {
            while ($row = $result->fetch(PDO::FETCH_ASSOC)) {
                $maps[] = $row;
            }
        }

        return json_encode($maps);
    }

    public function updateMap($mapId)
    {
        $sql = "UPDATE Maps SET lastLogin = NOW() WHERE id = $mapId";
        $res = $this->pdo->query($sql);

        if ($res)
            return true;
        return false;
    }

    public function removeMap($mapId)
    {
        $sql = "SELECT image FROM Maps WHERE id = $mapId";
        $result = $this->pdo->query($sql);

        if ($result && $result->rowCount() > 0) {
            $mappa = $result->fetch(PDO::FETCH_ASSOC);
            $imagePath = realpath(__DIR__ . '/../../uploads/') . '/' . $mappa['image'];  // Percorso dell'immagine
            // Rimuovi il file immagine, se esiste
            if (file_exists($imagePath)) {
                unlink($imagePath);  // Elimina il file fisico
            }

            // Ora elimina la mappa dal database
            $deleteSql = "DELETE FROM Maps WHERE id = $mapId";
            $res = $this->pdo->query($deleteSql);

            if ($res) {
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    public function getMapUsers($mapId)
    {
        $userId = $_SESSION['id'];

        $sql = "SELECT d.user_id as id, (SELECT u.username FROM Users u WHERE u.id = d.user_id) as username FROM Departments d WHERE d.user_id != $userId AND d.Dmap_id = $mapId";
        $result = $this->pdo->query($sql);

        if ($result->rowCount() > 0) {
            while ($row = $result->fetch(PDO::FETCH_ASSOC)) {
                $users[] = $row;
            }
            return $users;
        } else {
            return false;
        }
    }

    public function getMapDetails($mapId)
    {
        $sql = "SELECT m.name, m.happiness, m.citizens FROM Maps m WHERE m.id = $mapId";
        $res = $this->pdo->query($sql);

        if ($res) {
            $map = $res->fetch(PDO::FETCH_ASSOC);
            return $map;
        } else {
            return false;
        }
    }

    public function updateCitizens($mapId, $citizens)
    {
        $sql = "UPDATE Maps SET citizens = $citizens WHERE id = $mapId";
        $res = $this->pdo->query($sql);

        if ($res)
            return true;
        return false;
    }

    public function updateHappiness($mapId, $happiness)
    {
        $sql = "UPDATE Maps SET happiness = $happiness WHERE id = $mapId";
        $res = $this->pdo->query($sql);

        if ($res)
            return true;
        return false;
    }
}
