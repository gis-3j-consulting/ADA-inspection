window.addEventListener("load", function () {
  var url = "docs/ADAInspectorsGuide.pdf";

  pdfjsLib.GlobalWorkerOptions.workerSrc =
    "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

  var viewer = document.createElement("iframe");
  viewer.src =
    "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/web/viewer.html?file=" +
    encodeURIComponent(url);
  viewer.id = "pdf-viewer";

  document.getElementById("pdf-viewer").replaceWith(viewer);

  window.addEventListener("orientationchange", function () {
    setTimeout(function () {
      viewer.contentWindow.location.reload();
    }, 100);
  });
});
