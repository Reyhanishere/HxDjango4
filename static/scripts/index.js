function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

function addMarkdown(type) {
    const textarea = document.getElementById('picasso-text-editor');
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
    const textarea = document.getElementById('picasso-text-editor');
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
    const textarea = document.getElementById('picasso-text-editor');
    const position = textarea.selectionStart;
    const footnoteNumber = textarea.value.match(/\[\^\d+\]/g);
    const nextFootnoteNumber = footnoteNumber ? footnoteNumber.length + 1 : 1;
    const newText = `[^${nextFootnoteNumber}]`;
    textarea.value = textarea.value.substring(0, position) + newText + textarea.value.substring(position) + `\n\n[^${nextFootnoteNumber}]: `;
    textarea.focus();
}
