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

function addEventListeners(fieldId, passFailId, threshold, targetFieldId, logic = 'upper') {
    const inputField = document.getElementById(fieldId);
    const passFailField = document.getElementById(passFailId);

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

    addEventListeners('runslope-1', 'runslope-1-pf', 8.3);
    addEventListeners('cross-slope1', 'cross-slope1-pf', 2);
    addEventListeners('cross-slope2', 'cross-slope2-pf', 2);
    addEventListeners('cross-slope3', 'cross-slope3-pf', 2);
    addEventListeners('runslope-2', 'runslope-2-pf', 8.3);
    addEventListeners('runslope-3', 'runslope-3-pf', 8.3);
    addEventListeners('widthx', 'widthx-pf', 4, null, 'lower');
    addEventListeners('lengthy', 'lengthy-pf', 4, null, 'lower');
    addEventListeners('clear-width', 'clearwidth-pf', 4, null, 'lower');
    addEventListeners('slopex', 'slopex-pf', 2);
    addEventListeners('slopey', 'slopey-pf', 2);
    addEventListeners('flare-slope1', 'flare-slope1-pf', 10);
    addEventListeners('flare-slope2', 'flare-slope2-pf', 10);
    addEventListeners('curb-slope', 'curb-slope-pf', 8.3);
    addEventListeners('counter-slope', 'counter-slope-pf', 5);

    const today = new Date().toISOString().split('T')[0];
    document.getElementById('cal-date').value = today;
    document.getElementById('inspection-dat').value = today;
});
