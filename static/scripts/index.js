function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

function addMarkdown(type) {
    const textarea = document.getElementById('md_text_editor');
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selectedText = textarea.value.substring(start, end);
    let newText;

    if (selectedText.length !== 0) {
        switch (type) {
            case 'bold':
                newText = `**${selectedText}**`;
                break;
            case 'italic':
                newText = `*${selectedText}*`;
                break;
            case 'underline':
                newText = `<u>${selectedText}</u>`;
                break;
            default:
                return;
        }

        textarea.value = textarea.value.substring(0, start) + newText + textarea.value.substring(end);
    }
    textarea.focus();
}

function addLink() {
    const textarea = document.getElementById('md_text_editor');
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selectedText = textarea.value.substring(start, end);
    let linkTitle = selectedText;
    if (selectedText.length === 0) {
        linkTitle = prompt('Enter the title of the link:');
    }
    const linkURL = prompt('Enter the URL:');
    if (linkURL) {
        const newText = `[${linkTitle}](${linkURL})`;
        textarea.value = textarea.value.substring(0, start) + newText + textarea.value.substring(end);
    }
    textarea.focus();
}

function addFootnote() {
    const textBox = document.getElementById('md_text_editor');
    const position = textBox.selectionStart;
    const footnoteNumber = textBox.value.match(/\[\^\d+\]/g);
    const nextFootnoteNumber = footnoteNumber ? footnoteNumber.length + 1 : 1;
    const newText = `[^${(nextFootnoteNumber+1)/2}]`;
    textBox.value = textBox.value.substring(0, position) + newText + textBox.value.substring(position) + `\n\n[^${(nextFootnoteNumber+1)/2}]: `;
    textBox.focus();
}

function createMarkdownButtons(divName) {
    const markdownTextDiv = document.getElementById(divName);

    // Markdown button labels and their respective functions
    const markdownButtons = [
        { label: 'Bold', onclick: "addMarkdown('bold')" },
        { label: 'Italic', onclick: "addMarkdown('italic')" },
        { label: 'Underline', onclick: "addMarkdown('underline')" },
        { label: 'Link', onclick: "addLink()" },
        { label: 'Footnote', onclick: "addFootnote()" }
    ];

    // Create buttons and append them to the container
    markdownButtons.forEach(buttonInfo => {
        const button = document.createElement('button');
        button.textContent = buttonInfo.label;
        button.setAttribute('onclick', buttonInfo.onclick);
        button.setAttribute('class', buttonInfo.class);

        const btnsDiv = document.createElement('div');
        btnsDiv.setAttribute('class', 'markdown-buttons');
        btnsDiv.setAttribute('id', 'buttons-div');
        markdownTextDiv.insertBefore(button, markdownTextDiv.firstChild);
        const markdownButtonsContainer = document.getElementById("buttons-div");
        markdownButtonsContainer.appendChild(button);
    });
}
