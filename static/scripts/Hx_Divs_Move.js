function moveElementsToNewDiv(elementIds) {
    // Create a new details element
    const newDiv = document.createElement('details');
    newDiv.id = 'input-id';
    newDiv.className = "spanTwo"

    const summary = document.createElement('summary');
    summary.innerHTML = '<strong>اطلاعات هویتی و غیره</strong>';
    newDiv.appendChild(summary);

    // Append a smaller grid to the new div
    const smallerGrid = document.createElement('div');
    smallerGrid.id = 'smaller-grid';

    newDiv.appendChild(smallerGrid);

    // Move the specified elements inside the smaller grid
    elementIds.forEach(function(id) {
        const element = document.getElementById(id);
        if (element) {
            // Append each element to the smaller grid
            smallerGrid.appendChild(element);
        }
    });

    // Insert the new details element before the cc element
    const cc = document.getElementById('div_id_cc');
    if (cc && cc.parentElement) {
        cc.parentElement.insertBefore(newDiv, cc);
    }
}

const movingDivsIds = ['div_id_gender', 'div_id_job', 'div_id_dwelling', 'div_id_age', 'div_id_marriage', 'div_id_source', 'div_id_reliability', 'div_id_setting'];
