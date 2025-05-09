function checkMCQAnswer(correctAnswer, blockID, xp) {
    const thisBlock = document.getElementById(`mcq${blockID}`)
    const selectedOption = thisBlock.querySelector('input[name="option"]:checked');
    const checkBtn = document.getElementById(`checkMCQ${blockID}`)
    const feedback = document.getElementById(`feedback${blockID}`);
    const explanation = document.getElementById(`explanation${blockID}`);
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
        if (explanation.textContent != '') explanation.style.display = 'block';
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