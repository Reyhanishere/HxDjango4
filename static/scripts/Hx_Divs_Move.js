function moveElementsToNewDiv(elementIds) {
    const newDiv = document.createElement('details');
    newDiv.id = 'input-id';
    newDiv.className = "spanTwo"

    const summary = document.createElement('summary');
    summary.innerHTML = '<strong>اطلاعات هویتی و غیره &#128100;</strong>';
    newDiv.appendChild(summary);

    const smallerGrid = document.createElement('div');
    smallerGrid.id = 'smaller-grid';

    newDiv.appendChild(smallerGrid);

    elementIds.forEach(function(id) {
        const element = document.getElementById(id);
        if (element) {
            smallerGrid.appendChild(element);
        }
    });

    const cc = document.getElementById('div_id_cc');
    if (cc && cc.parentElement) {
        cc.parentElement.insertBefore(newDiv, cc);
    }
}

const movingDivsIds = ['div_id_gender', 'div_id_job', 'div_id_dwelling', 'div_id_age', 'div_id_age_m', 'div_id_marriage', 'div_id_source', 'div_id_reliability', 'div_id_setting', 'div_id_born_city'];