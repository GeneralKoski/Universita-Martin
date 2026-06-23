<?php
include_once (__DIR__ . '/../Models/ClickModel.php');

class ClickPresenter
{
    private $clickModel;

    public function __construct()
    {
        $this->clickModel = new ClickModel();
    }

    public function registerClick($mapId)
    {
        // Cancella la mappa dal Model
        $register = $this->clickModel->insertClick($mapId);
        if ($register) {
            echo json_encode(['success' => true, 'message' => 'Voto registrato con successo']);
        } else {
            echo json_encode(['success' => false, 'message' => 'Errore nella registrazione del voto']);
        }
    }

    public function deleteClick($mapId)
    {
        // Cancella la mappa dal Model
        $delete = $this->clickModel->removeClick($mapId);
        if ($delete) {
            echo json_encode(['success' => true, 'message' => 'Voto cancellato con successo']);
        } else {
            echo json_encode(['success' => false, 'message' => 'Errore nella cancellazione del voto']);
        }
    }
}