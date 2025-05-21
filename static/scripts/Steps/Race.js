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
        window.scrollBy({
            top: 500,
            behavior: 'smooth'
        });
    } else {
        disableContinue();
        const xpBox = document.getElementById("xpBox");
        const scoreInput = document.getElementById("scoreInput")
        xpBox.style.display = 'block';
        if (totalXP > 0) {
            xpBox.textContent = `عالی بود. ${totalXP} امتیاز گرفتی! این پایین اسمت رو بنویس.`
            scoreInput.value = totalXP

        } else {
            xpBox.textContent = 'خوب بود. کلی چیز یاد گرفتی.'
            scoreInput.value = 0

        }
        window.scrollBy({
            top: 200,
            behavior: 'smooth'
        });
        document.getElementById("submitForm").style.display = "flex"
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
        const feedback = blockElement.querySelectorAll('.feedback');

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
        const feedback = blockElement.querySelectorAll('.feedback');

        if (xp > 0) {
            feedback[0].classList.add("fdbkCorrect");
            feedback[0].textContent = `درست است! +${xp} امتیاز`;
            totalXP += parseInt(xp);
        } else {
            feedback[0].classList.add("fdbkNotAnswered");
            feedback[0].textContent = `چون اشتباه‌های زیادی داشتی، امتیاز نمی‌گیری ولی بریم بعدی...`;
        }
        enableContinue();

    };

}

function checkMCQAnswer(correctAnswer, blockID, xp) {
    const thisBlock = document.getElementById(`mcq${blockID}`)
    const selectedOption = thisBlock.querySelector('input[name="option"]:checked');
    const checkBtn = document.getElementById(`checkMCQ${blockID}`)
    const feedback = document.getElementById(`feedback${blockID}`);
    const checkedCount = parseInt(checkBtn.dataset.clicked)

    if (!selectedOption) {
        feedback.textContent = "یکی از گزینه‌ها را انتخاب کنید.";
        feedback.classList.add("fdbkNotAnswered");
        return;
    }

    if (selectedOption.value === correctAnswer) {
        if (checkedCount === 0) {
            feedback.textContent = `درست است! +${xp} امتیاز`;
            totalXP += parseInt(xp);
        } else {
            feedback.textContent = "درست شد (;";
        };
        if (feedback.classList.contains('fdbkNotAnswered')) {
            feedback.classList.remove('fdbkNotAnswered');
        }

        if (feedback.classList.contains('fdbkIncorrect')) {
            feedback.classList.remove('fdbkIncorrect');
        }
        feedback.classList.add("fdbkCorrect");
        checkBtn.style.display = "none";
        enableContinue();

    } else {
        // Get the correct answer text from the options
        var correctText = Array.from(thisBlock.querySelectorAll('.optionSpan'))
            .find(el => el.previousElementSibling.value === correctAnswer).textContent;
        feedback.innerHTML = `نادرست است. پاسخ درست، <b>${correctText}</b> می‌باشد. آن را انتخاب کنید و دوباره دکمۀ چک پاسخ را بزنید.`;
        checkBtn.setAttribute('data-clicked', '1');
        if (feedback.classList.contains('fdbkNotAnswered')) {
            feedback.classList.remove('fdbkNotAnswered');
        }
        feedback.classList.add("fdbkIncorrect");
    }
};
const featureBlocks = {};

function initFeatureBlock(blockId, allFeatures, expectedFeatures, expectedCount) {
    const container = document.getElementById(`feature-options-${blockId}`);
    const featureArea = container.querySelector('.features');
    const shuffled = [...allFeatures].sort(() => 0.5 - Math.random());

    const blockData = {
        expectedSet: new Set(expectedFeatures),
        expectedCount: expectedCount,
        featureArea: featureArea,
    };

    featureBlocks[blockId] = blockData;

    shuffled.forEach(feature => {
        const btn = document.createElement('span');
        btn.className = 'feature';
        btn.innerText = feature;

        btn.onclick = function() {
            if (btn.classList.contains('selected')) {
                btn.classList.remove('selected');
            } else {
                if (featureArea.querySelectorAll('.selected').length >= expectedCount) return;
                btn.classList.add('selected');
            }
        };

        featureArea.appendChild(btn);
    });
}

function resetKFSelection(blockId) {
    const block = featureBlocks[blockId];
    const buttons = block.featureArea.querySelectorAll('.feature');
    buttons.forEach(btn => btn.classList.remove('correct', 'incorrect', 'missed', 'selected'));

}

function checkKFAnswers(blockId, xp) {
    const block = featureBlocks[blockId];
    const buttons = block.featureArea.querySelectorAll('.feature');
    const selectedBtns = block.featureArea.querySelectorAll('.selected')
    const checkBtn = document.getElementById(`cB${blockId}`);
    const resetBtn = document.getElementById(`rB${blockId}`);
    const checkedCount = parseInt(checkBtn.dataset.clicked)
    const feedback = document.getElementById(`feedback${blockId}`);
    const expectedCount = parseInt(featureBlocks[blockId]['expectedCount'])

    if (selectedBtns.length === expectedCount) {

        let correct = 0;

        const buttons = block.featureArea.querySelectorAll('.feature');
        buttons.forEach(btn => btn.classList.remove('correct', 'incorrect', 'missed'));

        buttons.forEach(btn => {
            if (btn.classList.contains('selected')) {
                if (block.expectedSet.has(btn.innerText)) {
                    btn.classList.add('correct');
                    correct++;
                } else {
                    btn.classList.add('incorrect');
                }
            }
        });

        buttons.forEach(btn => {
            if (!btn.classList.contains('selected') && block.expectedSet.has(btn.innerText)) {
                btn.classList.add('missed');
            }
        });

        if (correct >= expectedCount - 1) {
            feedback.classList.add("fdbkCorrect");

            if (checkedCount === 0) {
                if (correct == expectedCount) {
                    feedback.textContent = `درست است! +${xp} امتیاز`;
                    totalXP += parseInt(xp);
                } else {
                    xp = Math.round(xp * (correct / expectedCount))
                    feedback.textContent = `تقریبا درست است! +${xp} امتیاز`;
                    totalXP += parseInt(xp);
                }

            } else {
                feedback.textContent = "درست شد (;";
            };

            if (feedback.classList.contains('fdbkNotAnswered')) {
                feedback.classList.remove('fdbkNotAnswered');
            }

            if (feedback.classList.contains('fdbkIncorrect')) {
                feedback.classList.remove('fdbkIncorrect');
            }

            enableContinue();
            checkBtn.style.display = "none";
            resetBtn.style.display = "none";

        } else {
            feedback.classList.add('fdbkIncorrect')
            feedback.textContent = "مواردی که اشتباه برگزیده‌اید را پاک کرده و موارد درست را انتخاب کنید و دوباره دکمۀ چک را بزنید.";
            checkBtn.setAttribute('data-clicked', '1');

            if (feedback.classList.contains('fdbkNotAnswered')) {
                feedback.classList.remove('fdbkNotAnswered');
            }
            if (feedback.classList.contains('mcqCorrect')) {
                feedback.classList.remove('mcqCorrect');
            }
        }
    } else {
        feedback.textContent = `باید ${expectedCount} مورد انتخاب کنید.`;
        feedback.classList.add("fdbkNotAnswered");
        if (feedback.classList.contains('mcqCorrect')) {
            feedback.classList.remove('mcqCorrect');
        }

        if (feedback.classList.contains('fdbkIncorrect')) {
            feedback.classList.remove('fdbkIncorrect');
        }
        return;
    }
}

function sendForm(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const submitRespMessage = document.getElementById('submitRespMessage')

    fetch(form.action, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "ok") {
                window.location.href = data.redirect_url;
            } else {
                submitRespMessage.style.display = "block"
                submitRespMessage.innerHTML = data.message;
            }
        })
        .catch(data => {
            submitRespMessage.style.display = "block"
            submitRespMessage.innerHTML = "❌ Submission failed.";
        });
}
