async function downloadPDF() {
    const nextObjectId = document.getElementById('nextObjectId').innerText;
    const nsRoad = document.getElementById('ns-road').value;
    const ewRoad = document.getElementById('ew-road').value;
    const selectedOption = document.getElementById('formSelect').selectedOptions[0];
    const filePath = selectedOption.getAttribute('filePath');

    const pdfBytes = await fetch(filePath).then(res => res.arrayBuffer());
    const pdfDoc = await PDFLib.PDFDocument.load(pdfBytes);
    const form = pdfDoc.getForm();

    const nsRoadField = form.getTextField('ADA2_PROJ_NM');
    const ewRoadField = form.getTextField('ADA1_XST_NM');

    nsRoadField.setText(nsRoad);
    ewRoadField.setText(ewRoad);

    const modifiedPdfBytes = await pdfDoc.save();
    const blob = new Blob([modifiedPdfBytes], { type: "application/pdf" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = `${nextObjectId}.pdf`;
    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(url);
}
