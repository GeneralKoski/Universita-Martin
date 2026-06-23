<?php
include_once(__DIR__ . '/../Models/MapModel.php');

class MapPresenter
{
    private $mapModel;

    public function __construct()
    {
        $this->mapModel = new MapModel();
    }

    // Metodo per creare una nuova mappa
    public function createMap()
    {
        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            // Recupera i dati dal form
            $nome = $_POST['nome'];
            $descrizione = $_POST['descrizione'];

            // Gestisci il caricamento dell'immagine
            if (isset($_FILES['immagine']) && $_FILES['immagine']['error'] === UPLOAD_ERR_OK) {
                $fileTmpPath = $_FILES['immagine']['tmp_name'];
                $fileName = $_FILES['immagine']['name'];
                $fileNameCmps = explode('.', $fileName);
                $fileExtension = strtolower(end($fileNameCmps));

                // Estensioni consentite
                $allowedfileExtensions = array('jpg', 'jpeg', 'png');
                if (in_array($fileExtension, $allowedfileExtensions)) {
                    $uploadFileDir = realpath(__DIR__ . '/../../uploads/') . '/';
                    $newFileName = $nome . '_' . time() . '.' . $fileExtension;
                    $dest_path = $uploadFileDir . $newFileName;

                    if (move_uploaded_file($fileTmpPath, $dest_path)) {
                        $avatarPath = $newFileName;
                    } else {
                        echo json_encode(['success' => false, 'message' => 'Errore nel caricamento del file immagine']);
                        return;
                    }
                } else {
                    echo json_encode(['success' => false, 'message' => 'Tipo di file immagine non valido. Solo JPG, JPEG e PNG sono permessi.']);
                    exit();
                }
            }

            // Query SQL per inserire la mappa nel database
            $map = $this->mapModel->createMap($nome, $descrizione, $avatarPath);
            if ($map) {
                // Reindirizza alla pagina di selezione delle mappe
                echo json_encode(['success' => true, 'redirect' => '/mapChoiceView']);
                return;
            } else {
                echo json_encode(['success' => false, 'message' => 'Errore durante la creazione!']);
                return;
            }
        }
    }

    // Metodo per visualizzare tutte le mappe
    public function showMaps()
    {
        // Recupera le mappe dal Model
        $maps = $this->mapModel->getMaps();
        echo $maps;
    }

    public function deleteMap($mapId)
    {
        // Cancella la mappa dal Model
        $delete = $this->mapModel->removeMap($mapId);
        if ($delete) {
            echo json_encode(['success' => true, 'message' => 'Mappa cancellata con successo']);
        } else {
            echo json_encode(['success' => false, 'message' => 'Errore nella cancellazione della mappa']);
        }
    }

    public function updateMapLogin($mapId)
    {
        $update = $this->mapModel->updateMap($mapId);
        if ($update) {
            echo json_encode(['success' => true, 'redirect' => "/mapView/$mapId"]);
        } else {
            echo json_encode(['success' => false, 'message' => 'Errore nella cancellazione della mappa']);
        }
    }

    public function mapUsers($mapId)
    {
        $users = $this->mapModel->getMapUsers($mapId);
        if ($users) {
            echo json_encode(['success' => true, 'users' => $users]);
        } else {
            echo json_encode(['success' => false, 'message' => 'Errore nel recupero degli utenti']);
        }
    }

    public function mapDetails($mapId)
    {
        $map = $this->mapModel->getMapDetails($mapId);
        if ($map) {
            echo json_encode(['success' => true, 'map' => $map]);
        } else {
            echo json_encode(['success' => false, 'message' => 'Errore nel recupero dettagli della mappa', 'redirect' => '/mapChoiceView']);
        }
    }

    public function updateCitizens($mapId, $citizens)
    {
        $update = $this->mapModel->updateCitizens($mapId, $citizens);
        if ($update) {
            echo json_encode(['success' => true, 'message' => 'Cittadini aggiornati con successo']);
        } else {
            echo json_encode(['success' => false, 'message' => "Errore nell'aggiornamento dei cittadini"]);
        }
    }

    public function updateHappiness($mapId, $happiness)
    {
        $update = $this->mapModel->updateHappiness($mapId, $happiness);
        if ($update) {
            echo json_encode(['success' => true, 'message' => 'Felicità aggiornata con successo', 'happiness' => $happiness]);
        } else {
            echo json_encode(['success' => false, 'message' => "Errore nell'aggiornamento della felicità"]);
        }
    }
}
