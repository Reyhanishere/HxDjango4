function openROS(evt, part) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(part).style.display = "block";
    evt.currentTarget.className += " active";
    document.getElementById("ROSTab").style.borderRadius = "10px 10px 0 0";
}

function closeROSOpenTab(event) {
    event.target.parentElement.style.display = 'none';
    document.getElementById('ROSTab').style.borderRadius = '10px';
}

function addToROSText(button, symbol) {
    const phrase = button.parentElement.querySelector('span').textContent;
    const ROSTextArea = document.getElementById('id_ros');
    ROSTextArea.value += `${phrase} ${symbol}\n`;
}

function toggleROSTab() {
    const rostab = document.getElementById('ROSTab');
    if (rostab.style.display === 'none' || rostab.style.display === '') {
        rostab.style.display = 'block';
    } else {
        rostab.style.display = 'none';
        const allTabs = document.querySelectorAll('.tabcontent');
        allTabs.forEach(tab => {
            tab.style.display = 'none';
        });
    }
}

function toggleROSTab() {
    const rostab = document.getElementById('ROSTab');
    if (rostab.style.display === 'none' || rostab.style.display === '') {
        rostab.style.display = 'block';
    } else {
        rostab.style.display = 'none';
        const allTabs = document.querySelectorAll('.tabcontent');
        allTabs.forEach(tab => {
            tab.style.display = 'none';
        });
    }
}

function createTabs(data) {
    const container = document.getElementById('tabs-container');

    for (const [key, phrases] of Object.entries(data)) {
        const tabDiv = document.createElement('div');
        tabDiv.id = key;
        tabDiv.className = 'tabcontent';
        const phraseTitle = document.createElement('div');
        phraseTitle.className = "phraseTitle"
        const title = document.createElement('h3');
        title.textContent = key + ":";
        title.className = "tabTitle"
        phraseTitle.appendChild(title);

        // const closeButton = document.createElement('span');
        // closeButton.textContent = '×';
        // closeButton.onclick = closeROSOpenTab;
        // closeButton.className = "helperCloseBtn";

        // phraseTitle.appendChild(closeButton);

        const phraseContAll = document.createElement('div');
        phraseContAll.className = "twoColumnar"
        phrases.forEach(phrase => {
            const phraseContainer = document.createElement('div');
            phraseContainer.className = 'phrase-container';

            const span = document.createElement('span');
            span.textContent = phrase;
            span.className = "phraseText";

            phraseContainer.appendChild(span);

            const addButton = document.createElement('span');
            addButton.innerHTML = '&#10133;';
            addButton.className = "pn"
            addButton.onclick = function() {
                addToROSText(this, '➕');
            };
            phraseContainer.appendChild(addButton);

            const removeButton = document.createElement('span');
            removeButton.innerHTML = '&#10134;';
            removeButton.className = "pn"
            removeButton.onclick = function() {
                addToROSText(this, '➖');
            };
            phraseContainer.appendChild(removeButton);

            phraseContAll.appendChild(phraseContainer);
        });
        tabDiv.appendChild(phraseTitle);
        tabDiv.appendChild(phraseContAll);
        container.appendChild(tabDiv);
    }
}

function createButtons(buttonData) {
    const rostab = document.getElementById('ROSTab');

    for (const [key, value] of Object.entries(buttonData)) {
        const button = document.createElement('span');
        button.className = 'tablinks';
        button.innerHTML = value;
        button.setAttribute('onclick', `openROS(event, '${key}')`);
        rostab.appendChild(button);
    }
}

var ROSButtonData = {
    "General": "General &#128512;",
    "Skin": "Skin &#127773;",
    // "Skull": "Skull &#128128;",
    "Ear": "Ear &#128066;",
    "Eye": "Eye &#128065;",
    "Nose": "Nose &#128067;",
    "Mouth": "Mouth &#128068; &#129463;",
    // "Throat": "Throat &#127908;",
    // "Neck": "Neck",
    // "Lymph": "Lymph Nodes &#129440;",
    "Chest": "Chest &#129659;",
    "Breast": "Breast &#128089;",
    "Heart": "Heart &#129728;",
    "Lungs": "Lungs &#129729;",
    // "Vesseles": "Vesseles &#129656;",
    "Abdomen": "Abdomen &#129328;",
    "Genitals": "Genitals &#129650;",
    "Anus": "Anus &#128701;",
    "Nerves": "Nerves &#129504;",
    "Limbs": "Limbs &#128170; &#129462;",
    "Muscuoskletal": "Muscuoskletal &#129470; &#129471;"
};

var ROSData = {
    "General": ["کاهش وزن", "افزایش وزن", "تب", "تعریق شبانه", "ضعف و بی‌حالی"],
    "Skin": ["خشکی پوست", "رطوبت پوست", "زخم", "افزایش رویش مو", "ریزش مو", "دانه", "لکه", "ترک", "زردی", "رنگ‌پریدگی"],
    "Eye": ["خشکی چشم", "درد چشم", "قرمزی چشم", "کاهش قدرت بینایی", ],
    "Ear": ["کاهش قدرت شنوایی", "گوش درد", "خروج ترشحات از گوش", ],
    "Nose": ["آبریزش بینی", "خون‌ریزی از بینی", "سینوزیت", ],
    "Mouth": ["زخم دهانی", "آفت دهان", "دندان مصنوعی", "گلودرد"],
    "Chest": ["درد قفسۀ سینه", "شکستگی دنده", ],
    "Breast": ["ترشح از نوک پستان", "فرورفتگی پستان", "برآمدگی در پستان", "قرمزی پوست پستان"],
    "Heart": ["تنگی نفس فعالیتی", "ارتوپنه", "PND", "ادم", "تپش قلب", "وضعیت سه‌پایه", ],
    "Lungs": ["درد پلورتیک", "سرفه", "ترشحات تنفسی", "سیانوز مرکزی"],
    // "Heart": ["dyspnea", "edema"],
    "Abdomen": ["درد شکم", "سیری زودرس", "سوزش سر دل", "دیس‌فاژی", "بی‌اشتهایی"],
    "Genitals": ["بی‌اختیاری", "سوزش ادرار", "تکرر ادرار",
        "قطره‌قطره آمدن ادرار", "ترشحات واژینال",
        "منس نامنظم", "سوزش ادرار"
    ],
    "Anus": ["خون‌ریزی از مقعد", "درد هنگام مدفوع کردن", ],
    "Nerves": ["گزگز انتهاها", "درد تیرکشنده به پا", "درد تیرکشنده به دست", "عدم احساس گرما و سرما"],
    "Limbs": ["سیانوز محیطی", "ادم انتهاها", ],
    "Muscuoskletal": ["درد دست", "درد پا", "درد کمر", "درد شانه", "ضعف عضلات", ],

};
