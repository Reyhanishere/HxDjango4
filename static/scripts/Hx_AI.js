function AddCCAI() {
    const targetDiv = document.getElementById("div_id_cc");
    const textElement = document.createElement("p");
    textElement.textContent = "دکمه را بزنید تا به کمک هوش مصنوعی شکایت بیمار به مدیکال ترمینولوژی تبدیل شود.";
    textElement.id = "cc_ai_p";
    textElement.className = "ai_p";
    const buttonElement = document.createElement("div");
    // const buttonElement = document.createElement("button");
    buttonElement.className = "aiBtn";
    buttonElement.onclick = "CCtoT()";
    const rightDiv = document.createElement("div");
    rightDiv.className = "rlAI rightAI";
    const AIBtnTxt = document.createElement("span");
    AIBtnTxt.textContent = 'AI';
    AIBtnTxt.className = "textAIBtn"
    rightDiv.appendChild(AIBtnTxt);
    const leftDiv = document.createElement("div");
    leftDiv.className = "rlAI leftAI";
    buttonElement.appendChild(rightDiv);
    buttonElement.appendChild(leftDiv);
    // buttonElement.addEventListener('click', CCtoT);
    buttonElement.onclick = CCtoT
    const textboxElement = document.createElement("input");
    textboxElement.type = "text";
    textboxElement.placeholder = "Enter CC Terminology OR Press AI!";
    textboxElement.id = 'cc_terminology_input';
    textboxElement.dir = "ltr";
    textboxElement.maxLength = '48'
    const ccAIBtnOutputDiv = document.createElement("div");
    ccAIBtnOutputDiv.id = "cc_ai_btn_output_div";
    ccAIBtnOutputDiv.appendChild(buttonElement)
    ccAIBtnOutputDiv.appendChild(textboxElement)

    targetDiv.appendChild(textElement);
    targetDiv.appendChild(ccAIBtnOutputDiv);

};

function CCtoT() {
    const cc = document.getElementById('id_cc').value;
    document.getElementById('cc_terminology_input').style.color = '#EEE';

    const formData = new FormData();
    formData.append('cc_fa', cc);

    const csrfToken = document.getElementById('csrf_token').value;

    fetch('cc_tot_ai/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken,
            },
        })
        .then(response => response.json())
        .then(data => {
            const cc_terminology_input = document.getElementById('cc_terminology_input')
            if (data.cct_ai_response) {
                cc_terminology_input.value = data.cct_ai_response;
                cc_terminology_input.placeholder = "Enter CC Terminology OR Press AI!"
                cc_terminology_input.style.color = '#444';
            } else {
                cc_terminology_input.placeholder = "Error: " + data.error;
                cc_terminology_input.value = "";

                cc_terminology_input.style.color = '#444';
            }
        })
        .catch(error => {
            cc_terminology_input.style.color = '#444';
            cc_terminology_input.placeholder = "Connection Failed /:";
            cc_terminology_input.value = "";

        });
}

function CreatePullUp() {
    const mainContent = document.getElementById("mainContent");
    const floatingDiv = document.createElement("div");
    floatingDiv.id = "floatingDiv";
    floatingDiv.dir = "ltr"
    const pullUpBar = document.createElement("div");
    pullUpBar.id = "pullUpBar";
    const pullText = document.createElement("p");
    pullText.id = "pullText";
    pullText.textContent = "Click For AI";
    const aiResponse = document.createElement("div");
    aiResponse.id = "aiResponse";
    const aiDescription = document.createElement("div");
    aiDescription.id = "aiDescription";
    aiDescription.innerHTML = "Your chat history won't be stored!<br/>Powered by: OpenAI, Metis, Medepartout";
    aiResponse.appendChild(aiDescription);

    pullUpBar.appendChild(pullText);
    floatingDiv.appendChild(pullUpBar);
    floatingDiv.appendChild(aiResponse);
    mainContent.parentNode.appendChild(floatingDiv);
    let isExpanded = false;


    pullUpBar.addEventListener("click", () => {
        const edel = document.getElementById("edel");
        isExpanded = !isExpanded;
        // floatingDiv.classList.toggle("open");
        floatingDiv.style.transform = isExpanded ? "translateY(-50vh)" : "translateY(-80px)";
        pullText.textContent = isExpanded ? "Click to minimize" : "Click to open";
        if (isExpanded == True) {
            edel.style.display = "none";
        } else {
            edel.style.display = "block";

        }
    });
};


function bounce() {
    const pullText = document.getElementById("pullText");
    const floatingDiv = document.getElementById("floatingDiv");
    if (pullText.textContent === "Click to open") {
        floatingDiv.style.transform = "translateY(-90px)";
        setTimeout(() => {
            floatingDiv.style.transform = "translateY(-75px)";
        }, 700);
    };
}

function PIQueAI() {
    const cc = document.getElementById('cc_terminology_input').value;
    const aiResponse = document.getElementById("aiResponse");

    // Create the request message element
    const aiReqMsg = document.createElement("div");
    aiReqMsg.className = 'aiMsg aiReqMsg';
    const aiReqMsgP = document.createElement("p");
    aiReqMsgP.textContent = "What can I ask for a patient with " + cc + "?";
    aiReqMsg.style.opacity = 0;
    aiReqMsg.appendChild(aiReqMsgP);
    aiResponse.appendChild(aiReqMsg);
    aiReqMsg.style.opacity = 1;
    bounce();

    const loadingIndicator = document.createElement("div");
    loadingIndicator.className = "spinnerCont";
    loadingIndicator.innerHTML = `
        <div class="spinnerLogo"></div>
        <p>Loading...</p>
    `;
    loadingIndicator.style.display = "flex";
    aiResponse.appendChild(loadingIndicator);

    const formData = new FormData();
    formData.append('cc_term', cc);

    const csrfToken = document.getElementById('csrf_token').value;

    fetch('pi_que_ai/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken,
            },
        })
        .then(response => response.json())
        .then(data => {
            loadingIndicator.style.display = "none";

            if (data.piq_ai_response) {
                const mdpi = window.markdownit();
                const htmlContent = mdpi.render(data.piq_ai_response);

                const aiRespMsg = document.createElement("div");
                aiRespMsg.className = 'aiMsg aiRespMsg';
                const aiRespMsgP = document.createElement("p");
                aiRespMsgP.innerHTML = htmlContent;
                aiRespMsg.style.opacity = 0;
                aiRespMsg.appendChild(aiRespMsgP);
                aiResponse.appendChild(aiRespMsg);
                aiRespMsg.style.opacity = 1;
            } else {
                const aiErrorMsg = document.createElement("div");
                aiErrorMsg.className = 'aiErrorMsg';
                const aiErrorMsgP = document.createElement("p");
                aiErrorMsgP.textContent = "Error: " + data.error;
                aiErrorMsg.style.opacity = 0;

                aiErrorMsg.appendChild(aiErrorMsgP);
                aiResponse.appendChild(aiErrorMsg);
                aiErrorMsg.style.opacity = 1;
            }
        })
        .catch(error => {
            loadingIndicator.style.display = "none";

            const aiErrorMsg = document.createElement("div");
            aiErrorMsg.className = 'aiErrorMsg';
            const aiErrorMsgP = document.createElement("p");
            aiErrorMsgP.textContent = "Error: Connection Failed /:";
            aiErrorMsg.style.opacity = 0;
            aiErrorMsg.appendChild(aiErrorMsgP);
            aiResponse.appendChild(aiErrorMsg);
            aiErrorMsg.style.opacity = 1;
        });

    document.getElementById("pullText").textContent = "Show AI Response!";
}



function AddPIAI() {
    const pi_div = document.getElementById("div_id_pi");
    const labelElementPI = pi_div.querySelector('label');
    labelElementPI.insertAdjacentHTML('afterend', `
        <span class="helper-toggle-button" onclick="PIQueAI()">کمکم کن! (AI)</span>`);
}

function createROSAITab(buttonData) {
    const rostab = document.getElementById('ROSTab');

    for (const [key, value] of Object.entries(buttonData)) {
        const button = document.createElement('span');
        button.className = 'tablinks';
        button.innerHTML = value;
        button.setAttribute('onclick', `openROS(event, '${key}')`);
        rostab.appendChild(button);
    }
}

function createPhEAITab(buttonData) {
    const rostab = document.getElementById('PhETab');

    for (const [key, value] of Object.entries(buttonData)) {
        const button = document.createElement('span');
        button.className = 'tablinks';
        button.innerHTML = value;
        button.setAttribute('onclick', `openPhE(event, '${key}_PhE')`);
        rostab.appendChild(button);
    }
}

function AddROSAI() {
    const ros_div = document.getElementById("div_id_ros");
    const labelElementROS = ros_div.querySelector('label');
    labelElementROS.insertAdjacentHTML('afterend', `
        <span class="helper-toggle-button" onclick="ROSAI()" id="ROSAIHelp">کمکم کن! (AI)</span>`);
    ros_div.style.display = "grid";
    ros_div.style.justifyItems = "start";
    ros_div.style.lineHeight = "2";
}

function AddPhEAI() {
    const phe_div = document.getElementById("div_id_phe");
    const labelElementPhE = phe_div.querySelector('label');
    labelElementPhE.insertAdjacentHTML('afterend', `
        <span class="helper-toggle-button" onclick="PhEAI()" id="PhEAIHelp">کمکم کن! (AI)</span>`);
    phe_div.style.display = "grid";
    phe_div.style.justifyItems = "start";
    phe_div.style.lineHeight = "2";
}

function ROSAI() {
    const cc = document.getElementById('cc_terminology_input').value;
    const pi = document.getElementById('id_pi').value;
    const pmh = document.getElementById('id_pmh').value;
    const dh = document.getElementById('id_drg').value;
    const fh = document.getElementById('id_fh').value;
    const sh = document.getElementById('id_sh').value;
    const ah = document.getElementById('id_alg').value;

    const aiResponse = document.getElementById("aiResponse");

    const aiReqMsg = document.createElement("div");
    aiReqMsg.className = 'aiMsg aiReqMsg';
    const aiReqMsgP = document.createElement("p");
    aiReqMsgP.textContent = "What are important questions I can ask in Review of Systems according to the Hx I've written till now?";
    // aiReqMsg.style.opacity = 0;
    aiReqMsg.appendChild(aiReqMsgP);
    aiResponse.appendChild(aiReqMsg);

    const loadingIndicator = document.createElement("div");
    loadingIndicator.className = "spinnerCont";
    loadingIndicator.innerHTML = `
        <div class="spinnerLogo"></div>
        <p>Loading...</p>
    `;
    loadingIndicator.style.display = "flex";
    aiResponse.appendChild(loadingIndicator);

    const formData = new FormData();
    formData.append('cc', cc);
    formData.append('pi', pi);
    formData.append('pmh', pmh);
    formData.append('dh', dh);
    formData.append('fh', fh);
    formData.append('sh', sh);
    formData.append('ah', ah);


    const csrfToken = document.getElementById('csrf_token').value;

    fetch('ros_ai/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken,
            },
        })
        .then(response => response.json())
        .then(data => {
            loadingIndicator.style.display = "none";

            if (data.ros_ai_response) {
                const responseAI = data.ros_ai_response;
                const aiRespMsg = document.createElement("div");
                aiRespMsg.className = 'aiMsg aiRespMsg';
                const aiRespMsgP = document.createElement("p");
                aiRespMsgP.textContent = "Check AI Tab in Review of Systems Helper!";
                aiRespMsg.style.opacity = 0;
                aiRespMsg.appendChild(aiRespMsgP);
                aiResponse.appendChild(aiRespMsg);
                aiRespMsg.style.opacity = 1;
                var rosList = responseAI.split('  ');
                rosList.pop()
                const AIBtnData = { "AI": "&#129302; AI &#129504;", }
                createROSAITab(AIBtnData);
                createTabs({ "AI": rosList });
                toggleROSTab()
                    // const ROSAIHelp = document.getElementById("ROSAIHelp");
                    // ROSAIHelp.removeAttribute('onclick');
                    // setTimeout(() => {
                    //     ROSAIHelp.onclick = "ROSAI()";
                    // }, 10000);

            } else {
                const aiErrorMsg = document.createElement("div");
                aiErrorMsg.className = 'aiErrorMsg';
                const aiErrorMsgP = document.createElement("p");
                aiErrorMsgP.textContent = "Error: " + data.error;
                aiErrorMsg.style.opacity = 0;

                aiErrorMsg.appendChild(aiErrorMsgP);
                aiResponse.appendChild(aiErrorMsg);
                aiErrorMsg.style.opacity = 1;
            }
        })
        .catch(error => {
            loadingIndicator.style.display = "none";

            const aiErrorMsg = document.createElement("div");
            aiErrorMsg.className = 'aiErrorMsg';
            const aiErrorMsgP = document.createElement("p");
            aiErrorMsgP.textContent = "Error: Connection Failed /:";
            aiErrorMsg.style.opacity = 0;
            aiErrorMsg.appendChild(aiErrorMsgP);
            aiResponse.appendChild(aiErrorMsg);
            aiErrorMsg.style.opacity = 1;
        });

    document.getElementById("pullText").textContent = "Show AI Response!";
}

function PhEAI() {
    const cc = document.getElementById('cc_terminology_input').value;
    const pi = document.getElementById('id_pi').value;
    const pmh = document.getElementById('id_pmh').value;
    const dh = document.getElementById('id_drg').value;
    const fh = document.getElementById('id_fh').value;
    const sh = document.getElementById('id_sh').value;
    const ah = document.getElementById('id_alg').value;

    const aiResponse = document.getElementById("aiResponse");

    const aiReqMsg = document.createElement("div");
    aiReqMsg.className = 'aiMsg aiReqMsg';
    const aiReqMsgP = document.createElement("p");
    aiReqMsgP.textContent = "What are important Physical Exams I can do according to the Hx I've written till now?";
    // aiReqMsg.style.opacity = 0;
    aiReqMsg.appendChild(aiReqMsgP);
    aiResponse.appendChild(aiReqMsg);

    const loadingIndicator = document.createElement("div");
    loadingIndicator.className = "spinnerCont";
    loadingIndicator.innerHTML = `
        <div class="spinnerLogo"></div>
        <p>Loading...</p>
    `;
    loadingIndicator.style.display = "flex";
    aiResponse.appendChild(loadingIndicator);

    const formData = new FormData();
    formData.append('cc', cc);
    formData.append('pi', pi);
    formData.append('pmh', pmh);
    formData.append('dh', dh);
    formData.append('fh', fh);
    formData.append('sh', sh);
    formData.append('ah', ah);


    const csrfToken = document.getElementById('csrf_token').value;

    fetch('phe_ai/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken,
            },
        })
        .then(response => response.json())
        .then(data => {
            loadingIndicator.style.display = "none";

            if (data.phe_ai_response) {
                const responseAI = data.phe_ai_response;
                const aiRespMsg = document.createElement("div");
                aiRespMsg.className = 'aiMsg aiRespMsg';
                const aiRespMsgP = document.createElement("p");
                aiRespMsgP.textContent = "Check AI Tab in Physical Examination Helper!";
                // aiRespMsgP.textContent = responseAI;
                aiRespMsg.style.opacity = 0;
                aiRespMsg.appendChild(aiRespMsgP);
                aiResponse.appendChild(aiRespMsg);
                aiRespMsg.style.opacity = 1;
                // var pheList = responseAI.split('  ');
                const AIBtnData = { "AI": "&#129302; AI &#129504;", }
                createPhEAITab(AIBtnData);
                createPhETabs({ "AI": JSON.parse(responseAI) });
                togglePhETab()
                    // const ROSAIHelp = document.getElementById("ROSAIHelp");
                    // ROSAIHelp.removeAttribute('onclick');
                    // setTimeout(() => {
                    //     ROSAIHelp.onclick = "ROSAI()";
                    // }, 10000);

            } else {
                const aiErrorMsg = document.createElement("div");
                aiErrorMsg.className = 'aiErrorMsg';
                const aiErrorMsgP = document.createElement("p");
                aiErrorMsgP.textContent = "Error: " + data.error;
                aiErrorMsg.style.opacity = 0;

                aiErrorMsg.appendChild(aiErrorMsgP);
                aiResponse.appendChild(aiErrorMsg);
                aiErrorMsg.style.opacity = 1;
            }
        })
        .catch(error => {
            loadingIndicator.style.display = "none";

            const aiErrorMsg = document.createElement("div");
            aiErrorMsg.className = 'aiErrorMsg';
            const aiErrorMsgP = document.createElement("p");
            aiErrorMsgP.textContent = "Error: Connection Failed /:";
            aiErrorMsg.style.opacity = 0;
            aiErrorMsg.appendChild(aiErrorMsgP);
            aiResponse.appendChild(aiErrorMsg);
            aiErrorMsg.style.opacity = 1;
        });

    document.getElementById("pullText").textContent = "Show AI Response!";
}
