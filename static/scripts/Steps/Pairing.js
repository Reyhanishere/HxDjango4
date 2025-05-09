function enableContinue() {
    const continueBtn = document.getElementById("continue");
    if (continueBtn) continueBtn.disabled = false;
    if (continueBtn) continueBtn.style.display = 'block';
    continueBtn.click()

}

function disableContinue() {
    const continueBtn = document.getElementById("continue")
    if (continueBtn) continueBtn.disabled = true;
    if (continueBtn) continueBtn.style.display = 'none';
}

let currentBlockIndex = 1;

function showNextBlock() {
    const nextBlock = document.getElementById('block-' + (currentBlockIndex + 1));

    if (nextBlock) {
        nextBlock.classList.add('active');
        currentBlockIndex++;

        if (nextBlock.dataset.model === "textblock") {
            enableContinue();
        } else {
            disableContinue();
        }
    } else {
        disableContinue();
        const xpBox = document.getElementById("xpBox");
        xpBox.style.display = 'block';
        if (totalXP > 0) {
            xpBox.textContent = `عالی بود. ${totalXP} امتیاز گرفتی!`
        } else {
            xpBox.textContent = 'خوب بود. کلی چیز یاد گرفتی.'
        }
    }
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

function checkAllAnsweredAndEnableContinue(blockElement, xp) {
    const keys = blockElement.querySelectorAll('.pairing-key');
    const allAnswered = Array.from(keys).every(key => key.classList.contains('answered'));
    if (allAnswered) {
        enableContinue();
        const explanation = blockElement.querySelectorAll(`.explanation`);
        const feedback = blockElement.querySelectorAll('.feedback');

        explanation[0].style.display = 'block';
        feedback[0].classList.add("fdbkCorrect");
        feedback[0].style.margin = "1rem";
        feedback[0].textContent = `درست است! +${xp} امتیاز`;
    };

}

// Function to handle the pairing logic
function handlePairing() {
    const pairingDivs = document.querySelectorAll('.pairingDiv');

    pairingDivs.forEach(div => {

        const keys = div.querySelectorAll('.pairing-key');
        const values = div.querySelectorAll('.pairing-value');

        div.dataset.mistakes = '0';
        div.dataset.itemsCount = keys.length;

        const shuffledKeys = Array.from(keys);
        const shuffledValues = Array.from(values);

        shuffleArray(shuffledKeys);
        shuffleArray(shuffledValues);

        const keyContainer = div.querySelector('.key-container');
        const valueContainer = div.querySelector('.value-container');

        keyContainer.innerHTML = '';
        valueContainer.innerHTML = '';

        shuffledKeys.forEach((key) => {
            keyContainer.appendChild(key);
        });
        shuffledValues.forEach((value) => {
            valueContainer.appendChild(value);
        });

        let firstSelected = null;
        let secondSelected = null;

        // const blockElement = document.getElementById(`block-${currentBlockIndex}`)
        // xpPerItem = parseInt(blockElement.dataset.xp)/keys.length
        var minusXP = 0;

        keys.forEach((key) => {
            key.addEventListener('click', function() {
                if (firstSelected && secondSelected) return;

                // Remove .selected class from all keys before selecting new one
                div.querySelectorAll('.pairing-key.selected').forEach(el => el.classList.remove('selected'));

                if (!key.classList.contains("answered") && !key.classList.contains("selected")) {
                    key.classList.add('selected');
                    firstSelected = key;
                } else {
                    firstSelected = null
                    key.classList.remove("selected");

                }
                if (secondSelected && firstSelected.getAttribute('data-pair-id') === secondSelected.getAttribute('data-pair-id')) {
                    setCorrectPair(firstSelected, secondSelected);
                } else if (secondSelected) {
                    setIncorrectPair(firstSelected, secondSelected);
                }
            });
        });

        values.forEach((value) => {
            value.addEventListener('click', function() {
                if (firstSelected && secondSelected) return;

                // Remove .selected class from all values before selecting new one
                div.querySelectorAll('.pairing-value.selected').forEach(el => el.classList.remove('selected'));
                if (!value.classList.contains("answered")) {
                    value.classList.add('selected');
                    secondSelected = value;
                } else {
                    secondSelected = null
                };

                if (firstSelected && firstSelected.getAttribute('data-pair-id') === value.getAttribute('data-pair-id')) {
                    setCorrectPair(firstSelected, value);
                } else if (firstSelected) {
                    setIncorrectPair(firstSelected, value);
                }
            });
        });


        // Function to handle a correct pair
        function setCorrectPair(key, value) {
            key.classList.add('correct');
            value.classList.add('correct');
            key.disabled = true;
            value.disabled = true;

            // Temporarily disable interactions for a short time
            setTimeout(function() {
                key.classList.remove('selected', 'correct');
                value.classList.remove('selected', 'correct');
                key.classList.add('answered');
                value.classList.add('answered');
                firstSelected = null;
                secondSelected = null;
                const blockElement = document.getElementById(`block-${currentBlockIndex}`)
                blockXP = parseInt(blockElement.dataset.xp)
                minusXP = blockXP * parseInt(div.dataset.mistakes) / parseInt(div.dataset.itemsCount)
                blockXP -= minusXP
                checkAllPairedAndEnableContinue(blockElement, blockXP);
            }, 250);

        }

        // Function to handle an incorrect pair
        function setIncorrectPair(key, value) {
            key.classList.add('incorrect');
            value.classList.add('incorrect');
            key.disabled = true;
            value.disabled = true;
            div.dataset.mistakes = parseInt(div.dataset.mistakes) + 1;

            setTimeout(function() {
                key.classList.remove('selected', 'incorrect');
                value.classList.remove('selected', 'incorrect');
                firstSelected = null;
                secondSelected = null;
            }, 250);
        }
    })
};

function checkAllPairedAndEnableContinue(blockElement, xp) {
    const keys = blockElement.querySelectorAll('.pairing-key');
    const allAnswered = Array.from(keys).every(key => key.classList.contains('answered'));
    if (allAnswered) {
        enableContinue();
        const explanation = blockElement.querySelectorAll(`.explanation`);
        const feedback = blockElement.querySelectorAll('.feedback');

        explanation[0].style.display = 'block';
        if (xp > 0) {
            feedback[0].classList.add("fdbkCorrect");
            feedback[0].textContent = `درست است! +${xp} امتیاز`;
            totalXP += parseInt(xp);
        } else {
            feedback[0].classList.add("fdbkNotAnswered");
            feedback[0].textContent = `چون اشتباه‌های زیادی داشتی، امتیاز نمی‌گیری ولی بریم بعدی...`;
        }

    };

}