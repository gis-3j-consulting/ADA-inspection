window.addEventListener('message', function(event) {
        if (event.origin !== window.location.origin) {
            return;
        }

        const { nextObjectId } = event.data;
        const fileNameInput = document.getElementById('fileName');
        fileNameInput.value = `${nextObjectId}`;

        if (event.data === 'refreshIframe') {
            const iframe = document.getElementById('formIframe');
            iframe.src = iframe.src;
        }
    });

function resetForm() {
    if (confirm('Are you sure you would like to reset the form?')) {
      const inputs = document.querySelectorAll('input[type="text"], input[type="number"], select');
      
      inputs.forEach(input => {
        input.value = input.defaultValue;
      });

      document.getElementById('fileName1').textContent = 'No file chosen';
      document.getElementById('fileName2').textContent = 'No file chosen';
      document.getElementById('fileName3').textContent = 'No file chosen';

      setTimeout(() => {
        window.parent.location.reload();
    }, 1000);
  }
}

function resetFormNoIntersections() {
    if (confirm('Are you sure you would like to reset the form?')) {
        const inputs = document.querySelectorAll('input[type="text"], input[type="number"], select');
        
        inputs.forEach(input => {
            if (input.id != "ew-road" && input.id != "ns-road") {
                input.value = input.defaultValue;
            } else {
                console.log("Intersection fields remain in place");
            }
        });
        
        document.getElementById('fileName1').textContent = 'No file chosen';
        document.getElementById('fileName2').textContent = 'No file chosen';
        document.getElementById('fileName3').textContent = 'No file chosen';

        setTimeout(() => {
            window.parent.location.reload();
        }, 1000);
    }
}

['1', '2', '3'].forEach(num => {
    document.getElementById(`photoButton${num}`).addEventListener('click', function() {
        document.getElementById(`fileInput${num}`).click();
    });

    document.getElementById(`fileInput${num}`).addEventListener('change', function() {
        const fileName = this.files[0].name;
        if (fileName === 'image.jpg') {
            document.getElementById(`fileName${num}`).textContent = 'image.jpg file rejected. Choose a photo from library.';
            document.getElementById(`fileName${num}`).style = 'color: red;';
        } else {
            document.getElementById(`fileName${num}`).textContent = fileName;
        }
    });
});

// Create autosave file, cleared when downloading or hitting reset button
function autoSave() {
    const inputs = document.querySelectorAll('input[type="text"], input[type="number"], select');
    const formData = {};

    inputs.forEach(input => {
        formData[input.name] = input.value;
    });

    localStorage.setItem('formData', JSON.stringify(formData));
}

function restoreData() {
    const savedData = localStorage.getItem('formData');
    if (savedData) {
        const formData = JSON.parse(savedData);
        Object.keys(formData).forEach(key => {
            const input = document.querySelector(`[name="${key}"]`);
            if (input) {
                input.value = formData[key];
            }
        });
    }
}

document.getElementById('curb-avg-button').addEventListener('click', function() {
    document.getElementById('tableModal').style.display = 'block';
});

document.querySelector('.close').addEventListener('click', function() {
    document.getElementById('tableModal').style.display = 'none';
});

document.getElementById('calculateAverage').addEventListener('click', function() {
    let numbers = [];
    let total = 0;
    let count = 0;

    for (let i = 1; i <= 10; i++) {
        let value = parseFloat(document.getElementById(`tablenum${i}`).value);
        if(!isNaN(value)) {
            numbers.push(value);
            total += value;
            count++;
        } 
    }

    if (count > 0) {
        let average = total / count;
        document.getElementById('curb-slope').value = average.toFixed(2);
    } else {
        alert('No valid numbers found');
    }

    document.getElementById('tableModal').style.display = 'none';
});

setInterval(autoSave, 500);

window.addEventListener('load', restoreData);