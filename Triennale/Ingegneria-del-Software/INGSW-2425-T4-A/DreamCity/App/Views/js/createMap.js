document.getElementById("createMapForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    fetch("http://localhost/Routes/MapRoutes.php/createMap", {
      method: "POST",
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        if (!data.success) {
          alert(data.message);
        } else {
          window.location.href = data.redirect;
        }
      })
      .catch(error => console.error("Errore:", error));
  });