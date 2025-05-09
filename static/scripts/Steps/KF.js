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
    const explanation = document.getElementById(`explanation${blockId}`);
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
            if (explanation.textContent != '') explanation.style.display = 'block';

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