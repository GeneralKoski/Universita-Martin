<?php

class MapBuildingModel
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

    public function loadBuilding($mapId)
    {
        $sql = "SELECT (SELECT b.name FROM Buildings b WHERE b.id = mb.MBbuilding_id) as building_type, mb.x_coordinate, mb.y_coordinate, mb.rotated FROM MapBuildings mb WHERE mb.MBmap_id = $mapId";
        $res = $this->pdo->query($sql);

        if ($res) {
            while ($row = $res->fetch(PDO::FETCH_ASSOC)) {
                $buildings[] = $row;
            }
            return $buildings;
        } else {
            return false;
        }
    }

    public function saveBuilding($mapId, $x, $y, $buildingType, $rotated)
    {
        $sql = "SELECT id FROM Buildings WHERE name = '$buildingType'";
        $res = $this->pdo->query($sql);
        if ($res) {
            $id = $res->fetch(PDO::FETCH_ASSOC);
            $buildingId = $id['id'];

            $sql = "INSERT INTO MapBuildings (MBmap_id, MBbuilding_id, x_coordinate, y_coordinate, rotated) 
                    VALUES ($mapId, '$buildingId', $x, $y, '$rotated')";
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

    public function deleteBuilding($mapId, $x, $y)
    {
        $sql = "DELETE FROM MapBuildings WHERE x_coordinate = $x AND y_coordinate = $y AND MBmap_id = $mapId";
        $res = $this->pdo->query($sql);

        if ($res) {
            return true;
        } else {
            return false;
        }
    }
}