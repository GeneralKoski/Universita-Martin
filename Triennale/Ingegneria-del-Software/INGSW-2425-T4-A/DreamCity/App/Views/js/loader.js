setTimeout(() => {
  document.querySelector(".loader").classList.add("loader--hidden");
}, 750);

setTimeout(() => {
  document.body.removeChild(document.querySelector(".loader"));
}, 1500);
