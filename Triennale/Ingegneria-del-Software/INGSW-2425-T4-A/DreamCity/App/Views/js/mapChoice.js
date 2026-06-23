// Effettua la fetch verso allMaps.php
fetch("http://localhost/Routes/MapRoutes.php/getMaps")
  .then((response) => response.json())
  .then((data) => {
    // Ottieni il container dove mettere le mappe
    const grigliaMappa = document.querySelector(".griglia-mappa");

    // Itera sui dati ricevuti
    data.forEach((mappa) => {
      const lastLoginDate = new Date(mappa.lastLogin);
      const currentDate = new Date();
      const oneWeekAgo = new Date(
        currentDate.setDate(currentDate.getDate() - 7)
      );

      // Se la data dell'ultimo accesso è più vecchia di una settimana, chiamo il fetch per eliminare la mappa
      if (lastLoginDate < oneWeekAgo) {
        // Chiamata per eliminare la mappa dal server
        fetch(`http://localhost/Routes/MapRoutes.php/deleteMap/${mappa.id}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              console.log(data.message);
            } else {
              console.error(data.message);
            }
          })
          .catch((error) => {
            console.error("Errore nella richiesta di eliminazione:", error);
          });
        return; // Non procedere oltre per la mappa che è stata eliminata
      }
      // Crea una nuova div per ogni mappa
      const boxMappa = document.createElement("div");
      boxMappa.classList.add("box-mappa");
      boxMappa.style.cursor = "pointer";
      boxMappa.onclick = () => {
        // Faccio il reindirizzamento alla mappa scelta e aggiorno l'ultimo accesso della mappa
        fetch(
          `http://localhost/Routes/MapRoutes.php/refreshLastLogin/${mappa.id}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
          }
        )
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              window.location.href = data.redirect;
            } else {
              console.error("Errore nella risposta:", data.message);
            }
          })
          .catch((error) => {
            console.error(
              "Errore nell'aggiornamento dell'ultimo accesso:",
              error
            );
          });
      };

      // Crea l'immagine
      const immagineMappa = document.createElement("img");
      immagineMappa.classList.add("immagine-mappa");
      immagineMappa.src = "/uploads/" + mappa.image;
      immagineMappa.alt = `Immagine ${mappa.name}`;

      // Crea il titolo
      const titoloMappa = document.createElement("h3");
      titoloMappa.classList.add("titolo-mappa");
      titoloMappa.textContent = mappa.name;

      // Crea la descrizione
      const descrizioneMappa = document.createElement("p");
      descrizioneMappa.classList.add("descrizione-mappa");
      descrizioneMappa.textContent = mappa.description;

      // Crea la descrizione
      const felicitaMappa = document.createElement("p");
      felicitaMappa.classList.add("felicita-mappa");
      felicitaMappa.textContent = "Happiness: " + mappa.happiness;

      // Crea la descrizione
      const abitantiMappa = document.createElement("p");
      abitantiMappa.classList.add("cittadini-mappa");
      abitantiMappa.textContent = "Citizens: " + mappa.citizens;

      // Crea il bottone di eliminazione
      const bottoneElimina = document.createElement("button");
      bottoneElimina.classList.add("delete-button");
      bottoneElimina.textContent =
        (mappa.clickCount ?? 0) + "/" + (mappa.totalUsers ?? 0);

      // Aggiungi un event listener per eliminare la mappa
      bottoneElimina.addEventListener("click", (event) => {
        event.stopPropagation(); // Evita che l'evento click sulla box si attivi

        // Invia la richiesta per registrare il clic (solo se non è stato già fatto)
        fetch(
          `http://localhost/Routes/ClickRoutes.php/registerClick/${mappa.id}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
          }
        )
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              mappa.clickCount = Number(mappa.clickCount) + 1; // Aggiorna il valore

              // Aggiorna il testo del bottone
              bottoneElimina.textContent =
                mappa.clickCount + "/" + mappa.totalUsers;

              if (mappa.clickCount >= mappa.totalUsers) {
                alert(
                  "Tutti hanno votato per eliminare la mappa, ora verrà cancellata!"
                );
                fetch(
                  `http://localhost/Routes/MapRoutes.php/deleteMap/${mappa.id}`,
                  {
                    method: "DELETE",
                    headers: {
                      "Content-Type": "application/json",
                    },
                  }
                )
                  .then((response) => response.json())
                  .then((data) => {
                    if (data.success) {
                      grigliaMappa.removeChild(boxMappa);
                    } else {
                      alert(data.error);
                    }
                  })
                  .catch((error) => {
                    console.error(
                      "Errore nella richiesta di eliminazione:",
                      error
                    );
                  });
                return;
              }
            } else {
              alert(data.message);
            }
          })
          .catch((error) => {
            console.error(
              "Errore nella richiesta di registrazione del clic:",
              error
            );
          });
      });

      const bottoneMantieni = document.createElement("button");
      bottoneMantieni.classList.add("keep-button");
      bottoneMantieni.textContent = "-";

      bottoneMantieni.addEventListener("click", (event) => {
        event.stopPropagation(); // Evita che l'evento click sulla box si attivi

        // Invia la richiesta per registrare il clic (solo se non è stato già fatto)
        fetch(
          `http://localhost/Routes/ClickRoutes.php/deleteClick/${mappa.id}`,
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
            },
          }
        )
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              mappa.clickCount = Number(mappa.clickCount) - 1; // Aggiorna il valore

              // Aggiorna il testo del bottone
              bottoneElimina.textContent =
                mappa.clickCount + "/" + mappa.totalUsers;
            } else {
              alert(data.message);
            }
          })
          .catch((error) => {
            console.error(
              "Errore nella richiesta di eliminazione del clic:",
              error
            );
          });
      });

      // Aggiungi immagine, titolo e descrizione alla box-mappa
      boxMappa.appendChild(immagineMappa);
      boxMappa.appendChild(titoloMappa);
      boxMappa.appendChild(descrizioneMappa);
      boxMappa.appendChild(abitantiMappa);
      boxMappa.appendChild(felicitaMappa);
      boxMappa.appendChild(bottoneElimina);
      boxMappa.appendChild(bottoneMantieni);

      // Aggiungi la nuova mappa alla griglia
      grigliaMappa.appendChild(boxMappa);
    });
  })
  .catch((error) => {
    console.error("Errore nel caricamento delle mappe:", error);
  });
