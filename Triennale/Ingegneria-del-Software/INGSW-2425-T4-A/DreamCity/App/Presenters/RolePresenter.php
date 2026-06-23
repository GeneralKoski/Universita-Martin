<?php
include_once(__DIR__ . '/../Models/RoleModel.php');

class RolePresenter
{
    private $roleModel;

    public function __construct()
    {
        $this->roleModel = new RoleModel();
    }

    public function availableRoles($mapId)
    {
        $roles = $this->roleModel->getAvailableRoles($mapId);

        if ($roles) {
            echo json_encode(['success' => true, 'roles' => $roles]);
        } else {
            echo json_encode(['success' => false, 'message' => 'Questa mappa è già piena!', 'redirect' => '/mapChoiceView']);
        }
    }

    public function addRole($mapId, $role)
    {
        $added = $this->roleModel->addRoleUser($mapId, $role);

        if ($added) {
            echo json_encode(['success' => true, 'message' => 'Ruolo aggiunto con successo', 'redirect' => "/mapView/$mapId"]);
        } else {
            echo json_encode(['success' => false, 'message' => "Errore durante l'assegnazione del ruolo", 'redirect' => '/mapChoiceView']);
        }
    }

    public function changeRole($mapId, $senderId, $messageId)
    {
        if (empty($mapId) || empty($senderId) || empty($messageId)) {
            echo json_encode(['success' => false, 'message' => 'Manca qualche dato!']);
            exit();
        }

        $changed = $this->roleModel->changeRole($mapId, $senderId, $messageId);

        if ($changed) {
            echo json_encode(['success' => true, 'message' => 'Ruoli cambiati e messaggio cancellato con successo', 'redirect' => "/mapView/$mapId"]);
        } else {
            echo json_encode(['success' => false, 'message' => "Errore durante lo scambio dei ruoli o cancellazione dei messaggi"]);
        }
    }

}