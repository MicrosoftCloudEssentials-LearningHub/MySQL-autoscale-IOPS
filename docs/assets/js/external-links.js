document.addEventListener("DOMContentLoaded", () => {
  for (const link of document.querySelectorAll("a[href]")) {
    if (link.origin !== window.location.origin) {
      link.target = "_blank";
      link.rel = "noopener noreferrer";
    }
  }
});