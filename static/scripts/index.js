function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

function addMarkdown(type) {
    const textBox = document.getElementById('picasso_text_editor');
    const start = textBox.selectionStart;
    const end = textBox.selectionEnd;
    const selectedText = textBox.value.substring(start, end);
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

        textBox.value = textBox.value.substring(0, start) + newText + textBox.value.substring(end);
    }
    textBox.focus();
}

function addLink() {
    const textBox = document.getElementById('picasso_text_editor');
    const start = textBox.selectionStart;
    const end = textBox.selectionEnd;
    const selectedText = textBox.value.substring(start, end);
    let linkTitle = selectedText;
    if (selectedText.length === 0) {
        linkTitle = prompt('Enter the title of the link:');
    }
    const linkURL = prompt('Enter the URL:');
    if (linkURL) {
        const newText = `[${linkTitle}](${linkURL})`;
        textBox.value = textBox.value.substring(0, start) + newText + textBox.value.substring(end);
    }
    textBox.focus();
}

function addFootnote() {
    const textBox = document.getElementById('picasso_text_editor');
    const position = textBox.selectionStart;
    const footnoteNumber = textBox.value.match(/\[\^\d+\]/g);
    const nextFootnoteNumber = footnoteNumber ? footnoteNumber.length + 1 : 1;
    const newText = `[^${(nextFootnoteNumber+1)/2}]`;
    textBox.value = textBox.value.substring(0, position) + newText + textBox.value.substring(position) + `\n\n[^${(nextFootnoteNumber+1)/2}]: `;
    textBox.focus();
}
