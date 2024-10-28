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

    // Get CSRF token from hidden input
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
            if (data.cct_ai_response) {
                document.getElementById('cc_terminology_input').value = data.cct_ai_response;
                document.getElementById('cc_terminology_input').placeholder = "Enter CC Terminology OR Press AI!"
                document.getElementById('cc_terminology_input').style.color = '#444';
            } else {
                document.getElementById('cc_terminology_input').placeholder = "Error: " + data.error;
                document.getElementById('cc_terminology_input').value = "";

                document.getElementById('cc_terminology_input').style.color = '#444';
            }
        })
        .catch(error => {
            document.getElementById('cc_terminology_input').style.color = '#444';
            document.getElementById('cc_terminology_input').placeholder = "Connection Failed );";
            document.getElementById('cc_terminology_input').value = "";

        });
}
