function genderSwitch(buttonId) {
    const genderSwitchBtn = document.getElementById(buttonId);
    if (!genderSwitchBtn) return;

    genderSwitchBtn.addEventListener('click', () => {
        if (genderSwitchBtn.textContent == 'Male') {
            genderSwitchBtn.textContent = 'Female';
            genderSwitchBtn.classList.add('female');
        } else {
            genderSwitchBtn.textContent = 'Male';
            genderSwitchBtn.classList.remove('female');
        }
    });
}

function showGraph(zScore) {
    zScore = Math.max(-4, Math.min(4, zScore));
    const marker = document.getElementById('valueMarker');
    const highlightOverlay = document.getElementById('highlightOverlay');
    const container = document.getElementById('chartContainer');
    container.style.display = 'block';
    const containerWidth = container.offsetWidth;

    const position = ((zScore + 4) / 8) * 100;
    marker.style.left = `${position}%`;
    highlightOverlay.style.width = `${position}%`;
    // var colooor = 'green'
    // if (position < 20) { colooor = 'red' }
    // highlightOverlay.style.background = colooor

}

function likeCalculi(likeBtn, likeUrl, csrfToken) {
    likeBtn.addEventListener('click', function() {
        const calculink = likeBtn.dataset.calculink;
        const action = likeBtn.dataset.action;

        fetch(likeUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `calculink=${calculink}&action=${action}`
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'ok') {

                    const newAction = action === 'like' ? 'unlike' : 'like';
                    likeBtn.dataset.action = newAction;

                    likeBtn.classList.toggle('liked', newAction === 'unlike');
                    likeBtn.classList.toggle('unliked', newAction === 'like');

                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
}


function calculateHCZScore() {
    const copyBtn = document.getElementById('copy-btn');
    const copyBtnAll = document.getElementById('copy-btn-all');
    copyBtn.style.display = 'none'
    copyBtnAll.style.display = 'none'
    const genderSwitchBtn = document.getElementById('gender-switch-btn');
    var genderTxt = genderSwitchBtn.textContent.toLowerCase();
    var gender = 1;
    if (genderTxt == 'male') {
        gender = 1
    } else {
        gender = 2
    };
    var years = parseInt(document.getElementById('years').value);
    var months = parseFloat(document.getElementById('months').value);
    var hc = parseFloat(document.getElementById('hc').value);
    var totalAgeMonths = years * 12 + months;

    if (isNaN(years) || isNaN(months) || isNaN(hc)) {
        resultElement.textContent = 'Error: Please enter valid numbers for age and head circumference.';
        resultElement.style.background = '#8e0000c7';
        resultElement.style.color = 'white';
        resultElement.style.display = 'inline-block';
        resultElement.style.gridColumn = 'span 2';
        return;
    };

    fetch(`../pedi_hc_zscore/?gender=${gender}&age_months=${totalAgeMonths}&hc=${hc}`)


    .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(`${errorData.error}`);
                });
            }
            return response.json();
        })
        .then(data => {
            resultElement.textContent = `Z-Score: ${data.z_score}\nPercentile: ${data.percentile}`;
            resultElement.style.background = 'linear-gradient(45deg, rgba(176, 176, 176, 0.2), rgba(233, 233, 233, 0.3))';
            resultElement.style.display = 'inline-block';
            resultElement.style.gridColumn = 'span 1';
            resultElement.style.color = 'black';
            copyBtn.style.display = 'block'
            copyBtnAll.style.display = 'block'
            zScore = data.z_score;
            showGraph(data.z_score);
        })
        .catch(error => {
            resultElement.textContent = `Error: ${error.message}`;
            resultElement.style.background = '#8e0000c7';
            resultElement.style.color = 'white';
            resultElement.style.display = 'inline-block';
            resultElement.style.gridColumn = 'span 2';
        })
        .finally(() => {
            calculateBtn.style.pointerEvents = 'auto';
            calculateBtn.style.opacity = '1';
            calculateBtn.style.zIndex = '3';
        });
}

function calculateLZScore() {
    const copyBtn = document.getElementById('copy-btn');
    const copyBtnAll = document.getElementById('copy-btn-all');
    copyBtn.style.display = 'none'
    copyBtnAll.style.display = 'none'
    const genderSwitchBtn = document.getElementById('gender-switch-btn');
    var genderTxt = genderSwitchBtn.textContent.toLowerCase();
    var gender = 1;
    if (genderTxt == 'male') {
        gender = 1
    } else {
        gender = 2
    };
    var years = parseInt(document.getElementById('years').value);
    var months = parseFloat(document.getElementById('months').value);
    var length = parseFloat(document.getElementById('length').value);
    var totalAgeMonths = years * 12 + months;

    if (isNaN(years) || isNaN(months) || isNaN(length)) {
        resultElement.textContent = 'Error: Please enter valid numbers for age and length.';
        resultElement.style.background = '#8e0000c7';
        resultElement.style.color = 'white';
        resultElement.style.display = 'inline-block';
        resultElement.style.gridColumn = 'span 2';
        return;
    };

    fetch(`../pedi_l_zscore/?gender=${gender}&age_months=${totalAgeMonths}&length=${length}`)


    .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(`${errorData.error}`);
                });
            }
            return response.json();
        })
        .then(data => {
            resultElement.textContent = `Z-Score: ${data.z_score}\nPercentile: ${data.percentile}`;
            resultElement.style.background = 'linear-gradient(45deg, rgba(176, 176, 176, 0.2), rgba(233, 233, 233, 0.3))';
            resultElement.style.display = 'inline-block';
            resultElement.style.gridColumn = 'span 1';
            resultElement.style.color = 'black';
            copyBtn.style.display = 'block'
            copyBtnAll.style.display = 'block'
            zScore = data.z_score;
            showGraph(data.z_score);
        })
        .catch(error => {
            resultElement.textContent = `Error: ${error.message}`;
            resultElement.style.background = '#8e0000c7';
            resultElement.style.color = 'white';
            resultElement.style.display = 'inline-block';
            resultElement.style.gridColumn = 'span 2';
        })
        .finally(() => {
            calculateBtn.style.pointerEvents = 'auto';
            calculateBtn.style.opacity = '1';
            calculateBtn.style.zIndex = '3';
        });
}

function calculateWZScore() {
    const copyBtn = document.getElementById('copy-btn');
    const copyBtnAll = document.getElementById('copy-btn-all');
    copyBtn.style.display = 'none'
    copyBtnAll.style.display = 'none'
    const genderSwitchBtn = document.getElementById('gender-switch-btn');
    var genderTxt = genderSwitchBtn.textContent.toLowerCase();
    var gender = 1;
    if (genderTxt == 'male') {
        gender = 1
    } else {
        gender = 2
    };
    var years = parseInt(document.getElementById('years').value);
    var months = parseFloat(document.getElementById('months').value);
    var weight = parseFloat(document.getElementById('weight').value);
    var totalAgeMonths = years * 12 + months;

    if (isNaN(years) || isNaN(months) || isNaN(weight)) {
        resultElement.textContent = 'Error: Please enter valid numbers for age and weight.';
        resultElement.style.background = '#8e0000c7';
        resultElement.style.color = 'white';
        resultElement.style.display = 'inline-block';
        resultElement.style.gridColumn = 'span 2';
        return;
    };

    fetch(`../pedi_w_zscore/?gender=${gender}&age_months=${totalAgeMonths}&weight=${weight}`)


    .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(`${errorData.error}`);
                });
            }
            return response.json();
        })
        .then(data => {
            resultElement.textContent = `Z-Score: ${data.z_score}\nPercentile: ${data.percentile}`;
            resultElement.style.background = 'linear-gradient(45deg, rgba(176, 176, 176, 0.2), rgba(233, 233, 233, 0.3))';
            resultElement.style.display = 'inline-block';
            resultElement.style.gridColumn = 'span 1';
            resultElement.style.color = 'black';
            copyBtn.style.display = 'block'
            copyBtnAll.style.display = 'block'
            zScore = data.z_score;
            showGraph(data.z_score);
        })
        .catch(error => {
            resultElement.textContent = `Error: ${error.message}`;
            resultElement.style.background = '#8e0000c7';
            resultElement.style.color = 'white';
            resultElement.style.display = 'inline-block';
            resultElement.style.gridColumn = 'span 2';
        })
        .finally(() => {
            calculateBtn.style.pointerEvents = 'auto';
            calculateBtn.style.opacity = '1';
            calculateBtn.style.zIndex = '3';

        });
};

function calculateBMIZScore() {
    const copyBtnAll = document.getElementById('copy-btn-all');
    copyBtnAll.style.display = 'none'
    const genderSwitchBtn = document.getElementById('gender-switch-btn');
    var genderTxt = genderSwitchBtn.textContent.toLowerCase();
    var gender = 1;
    if (genderTxt == 'male') {
        gender = 1
    } else {
        gender = 2
    };
    var years = parseInt(document.getElementById('years').value);
    var months = parseFloat(document.getElementById('months').value);
    var weight = parseFloat(document.getElementById('weightB').value);
    var length = parseFloat(document.getElementById('length').value);

    var totalAgeMonths = years * 12 + months;

    if (isNaN(years) || isNaN(months) || isNaN(weight) || isNaN(length)) {
        resultElement.textContent = 'Error: Please enter valid numbers for age, weight and length.';
        resultElement.style.background = '#8e0000c7';
        resultElement.style.color = 'white';
        resultElement.style.display = 'inline-block';
        resultElement.style.gridColumn = 'span 2';
        return;
    };

    fetch(`../pedi_bmi_zscore/?gender=${gender}&age_months=${totalAgeMonths}&weight=${weight}&length=${length}`)


    .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(`${errorData.error}`);
                });
            }
            return response.json();
        })
        .then(data => {
            resultElement.textContent = `BMI: ${data.value}\nZ-Score: ${data.z_score}\nPercentile: ${data.percentile}`;
            resultElement.style.background = 'linear-gradient(45deg, rgba(176, 176, 176, 0.2), rgba(233, 233, 233, 0.3))';
            resultElement.style.display = 'inline-block';
            resultElement.style.gridColumn = 'span 1';
            resultElement.style.color = 'black';
            copyBtnAll.style.display = 'block'
            zScore = data.z_score;
            resultElement.style.transform = 'translate(0 px, 0 px)';
            showGraph(data.z_score);

        })
        .catch(error => {
            resultElement.textContent = `Error: ${error.message}`;
            resultElement.style.background = '#8e0000c7';
            resultElement.style.color = 'white';
            resultElement.style.display = 'inline-block';
            resultElement.style.gridColumn = 'span 2';
            resultElement.style.transform = 'translate(0 px, -10 px)';
        })
        .finally(() => {
            calculateBtn.style.pointerEvents = 'auto';
            calculateBtn.style.opacity = '1';
            calculateBtn.style.zIndex = '3';

        });
}

function copyZScoreBMIPecentile() {
    const text = `${resultElement.innerText}`;
    const copyBtnAll = document.getElementById('copy-btn-all');
    navigator.clipboard.writeText(text)
        .then(() => {
            copyBtnAll.innerText = "Copied!";
            setTimeout(() => {
                copyBtnAll.innerText = "Copy";
            }, 2000);
        })
        .catch((err) => {
            console.error("Failed to copy text: ", err);
        });
}

function copyZScore() {
    // const text = `Weight: ${weight.value} kg\n(${resultElement.innerText})`;
    const text = resultElement.innerText;
    const copyBtn = document.getElementById('copy-btn');
    navigator.clipboard.writeText(text)
        .then(() => {
            copyBtn.innerText = "Copied!";
            setTimeout(() => {
                copyBtn.innerText = "Copy Z&P";
            }, 2000);
        })
        .catch((err) => {
            console.error("Failed to copy text: ", err);
        });
}

function copyZScoreHCPecentile() {
    var hc = parseFloat(document.getElementById('hc').value);
    const text = `Head Circumference: ${hc} cm\n(${resultElement.innerText})`;
    const copyBtnAll = document.getElementById('copy-btn-all');
    navigator.clipboard.writeText(text)
        .then(() => {
            copyBtnAll.innerText = "Copied!";
            setTimeout(() => {
                copyBtnAll.innerText = "Copy All";
            }, 2000);
        })
        .catch((err) => {
            console.error("Failed to copy text: ", err);
        });
}

function copyZScoreLengthPecentile() {
    var length = parseFloat(document.getElementById('length').value);
    const text = `Length: ${length} cm\n(${resultElement.innerText})`;
    const copyBtnAll = document.getElementById('copy-btn-all');
    navigator.clipboard.writeText(text)
        .then(() => {
            copyBtnAll.innerText = "Copied!";
            setTimeout(() => {
                copyBtnAll.innerText = "Copy All";
            }, 2000);
        })
        .catch((err) => {
            console.error("Failed to copy text: ", err);
        });
}

function copyZScoreWeightPecentile() {
    const text = `Weight: ${weight.value} kg\n(${resultElement.innerText})`;
    const copyBtnAll = document.getElementById('copy-btn-all');
    navigator.clipboard.writeText(text)
        .then(() => {
            copyBtnAll.innerText = "Copied!";
            setTimeout(() => {
                copyBtnAll.innerText = "Copy All";
            }, 2000);
        })
        .catch((err) => {
            console.error("Failed to copy text: ", err);
        });
}
