function getParam() {
  const url = window.location.pathname;
  const mapId = url.split("/")[3]; // Prende l'ID dalla URL /map/{user}/{map}
  return mapId;
}

const mapId = getParam();

// Funzione per caricare i ruoli dal server
fetch(`http://localhost/Routes/RoleRoutes.php/availableRoles/${mapId}`)
  .then((response) => response.json())
  .then((data) => {
    if (data.success) {
      const roleSelect = document.getElementById("role");

      data["roles"].forEach((role) => {
        const option = document.createElement("option");
        option.value = role;
        option.textContent = role;
        roleSelect.appendChild(option);
      });
    } else {
      window.location.href = data.redirect;
    }
  });

document
  .getElementById("roleForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Impedisce l'invio normale del form

    const role = document.getElementById("role").value;

    fetch(`http://localhost/Routes/RoleRoutes.php/addRole/${mapId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(role), // Invia i dati come JSON
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          window.location.href = data.redirect;
        } else {
          alert(data.message);
        }
      })
      .catch((error) => console.error("Errore nella richiesta:", error));
  });
