function autoPFupper(valueFieldId, passFailId, threshold) {
    return function() {
        const valueInput = document.getElementById(valueFieldId);
        const passFailSelect = document.getElementById(passFailId);
        const value = parseFloat(valueInput.value);

        if (!isNaN(value)) {
            if (value <= threshold) {
                passFailSelect.value = 'pass';
            } else {
                passFailSelect.value = 'fail';
            }
        } else {
            passFailSelect.value = ''; 
        }
    };
}

function autoPFlower(valueFieldId, passFailId, threshold) {
    return function() {
        const valueInput = document.getElementById(valueFieldId);
        const passFailSelect = document.getElementById(passFailId);
        const value = parseFloat(valueInput.value);

        if (!isNaN(value)) {
            if (value >= threshold) {
                passFailSelect.value = 'pass';
            } else {
                passFailSelect.value = 'fail';
            }
        } else {
            passFailSelect.value = ''; 
        }
    };
}

function autosetParallel(valueFieldId, valueFieldId2) {
    return function() {
        const valueFieldInput = document.getElementById(valueFieldId);
        const valueFieldInput2 = document.getElementById(valueFieldId2);
        const value = parseFloat(valueFieldInput.value);

        if (!isNaN(value)) {
            valueFieldInput2.value = value; 
        } else {
            valueFieldInput2.value = '';
        }
    }
}

function autoMidblock(valueFieldId, commentsId) {
    return function() {
        const valueInput = document.getElementById(valueFieldId);
        const commentsBox = document.getElementById(commentsId);
    
        valueInput.addEventListener('change', function() {
            if (this.value === 'midblock') {
                if (!commentsBox.value.startsWith("Mid-block")) {
                    commentsBox.value = "Mid-block " + commentsBox.value; 
                }
            } else {
                commentsBox.value = commentsBox.value.replace("Mid-block ", "");
            }
        });

    }
}

function addEventListeners(fieldId, passFailId, threshold, targetFieldId, logic = 'upper') {
    const inputField = document.getElementById(fieldId);
    const passFailField = document.getElementById(passFailId);

    if (logic === 'midblock') {
        if (inputField && passFailField) {
            inputField.addEventListener('input', autoMidblock(fieldId, passFailId));
            console.log(`Logic added to watch for Midblock placement`);
        } else {
            console.log(`Something went wrong while establishing midblock logic`)
        }
        return;
    }

    if (inputField && passFailField) {
        const passFailFunction = logic === 'upper' ? autoPFupper(fieldId, passFailId, threshold) : autoPFlower(fieldId, passFailId, threshold);
        inputField.addEventListener('input', passFailFunction);
        console.log(`Event listener added for ${fieldId}`);
    } else {
        console.log(`${fieldId} input or ${passFailId} pass/fail select not found`);
    }

    if (targetFieldId) {
        const targetField = document.getElementById(targetFieldId);
        if (inputField && targetField) {
            inputField.addEventListener('input', autosetParallel(fieldId, targetFieldId));
            console.log(`Event listener added to sync ${fieldId} with ${targetFieldId}`);
        } else {
            console.log(`${fieldId} input or ${targetFieldId} not found`);
        }
    }
}

window.addEventListener('DOMContentLoaded', (event) => {
    console.log("DOM fully loaded and parsed");

    addEventListeners('runslope-1', 'runslope-1-pf', 2, 'slopey');
    addEventListeners('cross-slope1', 'cross-slope1-pf', 2, 'slopex');
    addEventListeners('cross-slope2', 'cross-slope2-pf', 2);
    addEventListeners('cross-slope3', 'cross-slope3-pf', 2);
    addEventListeners('runslope-2', 'runslope-2-pf', 8.3);
    addEventListeners('runslope-3', 'runslope-3-pf', 8.3);
    addEventListeners('widthx', 'widthx-pf', 4, null, 'lower');
    addEventListeners('lengthy', 'lengthy-pf', 4, null, 'lower');
    addEventListeners('clear-width', 'clearwidth-pf', 4, null, 'lower');
    addEventListeners('slopex', 'slopex-pf', 2);
    addEventListeners('slopey', 'slopey-pf', 2);
    addEventListeners('curb-slope', 'curb-slope-pf', 8.3);
    addEventListeners('counter-slope', 'counter-slope-pf', 5);
    addEventListeners('corner-position', 'comments-box', null, 'comments-box', 'midblock');

    const today = new Date().toISOString().split('T')[0];
    document.getElementById('cal-date').value = today;
    document.getElementById('inspection-date').value = today;
});

