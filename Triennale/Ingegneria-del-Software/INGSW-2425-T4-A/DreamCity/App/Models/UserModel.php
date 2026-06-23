<?php

class UserModel
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
    public function createUser($username, $password, $avatarPath)
    {
        $sql = "INSERT INTO Users (username, password, avatar) VALUES ('$username', '$password', '$avatarPath')";
        $res = $this->pdo->query($sql);

        if (!$res) {
            echo $this->pdo . '<br>';
            return;
        }

        return true;
    }

    // Verifica le credenziali dell'utente per il login
    public function authenticateUser($username, $password)
    {
        $sql = "SELECT * FROM Users WHERE username = '$username'";
        $result = $this->pdo->query($sql);

        if ($result->rowCount() > 0) {
            $user = $result->fetch(PDO::FETCH_ASSOC);
            // Verifica la password
            if (password_verify($password, $user['password'])) {
                // Impostiamo la sessione utente
                $_SESSION['id'] = $user['id'];
                $_SESSION['username'] = $user['username'];
                return true;
            }
        }
        return null;  // Se non troviamo l'utente o la password non è corretta
    }

    // Recupera un elenco di utenti
    public function getUsers()
    {
        $userId = $_SESSION['id'];

        $sql = "SELECT * FROM Users WHERE id != $userId";
        $result = $this->pdo->query($sql);

        $users = [];

        if ($result->rowCount() > 0) {
            while ($row = $result->fetch(PDO::FETCH_ASSOC)) {
                $users[] = $row;
            }
            return $users;
        } else {
            return false;
        }
    }

    public function getUserDetails($mapId, $userId, $username)
    {
        $sql = "SELECT (SELECT u.avatar FROM Users u WHERE u.id = $userId) as avatar, r.name, d.budget FROM Roles r, Departments d WHERE r.id = d.Drole_id AND d.user_id = $userId AND d.Dmap_id = $mapId";
        $res = $this->pdo->query($sql);

        if (!$res) {
            return false;
        }

        $role = $res->fetch(PDO::FETCH_ASSOC);

        if (!$role) {
            return false;
        }

        return $role;
    }
}