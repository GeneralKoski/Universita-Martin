<?php

class BuildingModel
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
    public function selectBuildings()
    {
        $sql = 'SELECT b.name, b.color, b.width, b.height, b.happiness, b.cost FROM Buildings b';
        $res = $this->pdo->query($sql);

        if ($res->rowCount() > 0) {
            while ($row = $res->fetch(PDO::FETCH_ASSOC)) {
                $buildings[] = [
                    'name' => $row['name'],
                    'color' => $row['color'],
                    'width' => $row['width'],
                    'height' => $row['height'],
                    'happiness' => $row['happiness'],
                    'cost' => $row['cost'],
                ];
            }
            return $buildings;
        }

        return false;
    }

    public function selectUserBuildings($mapId)
    {
        $userId = $_SESSION['id'];
        $sql = "SELECT d.Drole_id as id FROM Departments d WHERE user_id = $userId AND Dmap_id = $mapId";
        $res = $this->pdo->query($sql);

        if ($res) {
            $roleId = $res->fetch(PDO::FETCH_ASSOC);
            $roleId = $roleId['id'];

            $sql = "SELECT b.name FROM Buildings b WHERE Brole_id = $roleId";
            $res = $this->pdo->query($sql);

            while ($row = $res->fetch(PDO::FETCH_ASSOC)) {
                $userBuildings[] = [
                    'name' => $row['name'],
                ];
            }
            return $userBuildings;
        }

        return false;
    }
}
