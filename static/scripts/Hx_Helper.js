function AddROSSection() {

    const divIdRos = document.getElementById('div_id_ros');
    const labelElement = divIdRos.querySelector('label');

    if (labelElement) {
        labelElement.insertAdjacentHTML('afterend', `
            <span class="helper-toggle-button" onclick="toggleROSTab()">کمکم کن!</span>
            <div class="ROSTab" id="ROSTab"></div>
            <div id="tabs-container"></div>
        `);

        // Initialize ROS buttons and tabs after injecting the container elements
        createButtons(ROSButtonData);
        createTabs(ROSData);
    };
}

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
        phraseContAll.className = "twoColumnar txtAlgnR"
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
// ----------------------------------------------------



function AddPhESection() {
    const divIdPhE = document.getElementById('div_id_phe');
    const labelElement = divIdPhE.querySelector('label');

    if (labelElement) {
        labelElement.insertAdjacentHTML('afterend', `
            <span class="helper-toggle-button" onclick="togglePhETab()">کمکم کن!</span>
            <div class="ROSTab" id="PhETab"></div>
            <div id="PhE-container"></div>
        `);

        createPhEButtons(PhEButtonData);
        createPhETabs(PhEData);
    };
}

function togglePhETab() {
    const phETab = document.getElementById('PhETab');
    if (phETab.style.display === 'none' || !phETab.style.display) {
        phETab.style.display = 'block';
    } else {
        phETab.style.display = 'none';
    }
}

function createPhETabs(data) {
    const container = document.getElementById('PhE-container');

    for (const [primary, secondaryObj] of Object.entries(data)) {
        const tabDiv = document.createElement('div');
        tabDiv.id = primary + "_PhE";
        tabDiv.className = 'tabcontent';


        const phraseTitle = document.createElement('div');
        phraseTitle.className = "phraseTitle";

        const title = document.createElement('h3');
        title.textContent = primary + ":";
        title.className = "tabTitle";
        phraseTitle.appendChild(title);

        const phraseContAll = document.createElement('div');
        phraseContAll.className = "twoColumnar txtAlgnR";

        for (const [secondary, options] of Object.entries(secondaryObj)) {
            const phraseContainer = document.createElement('div');
            phraseContainer.className = 'phrase-container-bot-border';

            const span = document.createElement('span');
            span.textContent = secondary;
            span.className = "phraseButton";
            span.onclick = function() {
                addToPhEText(this, `\n${secondary}: `);
            };
            phraseContainer.appendChild(span);
            const dot = document.createElement('span');
            dot.textContent = ": "
            phraseContainer.appendChild(dot);

            options.forEach(option => {
                const optionButton = document.createElement('span');
                optionButton.textContent = option;
                optionButton.className = "optionButton";
                optionButton.onclick = function() {
                    // addToPhEText(this, `${secondary}: ${option}\n`);
                    addToPhEText(this, `${option} `);

                };
                phraseContainer.appendChild(optionButton);
            });

            phraseContAll.appendChild(phraseContainer);
        }

        tabDiv.appendChild(phraseTitle);
        tabDiv.appendChild(phraseContAll);
        container.appendChild(tabDiv);
    }
}

function createPhEButtons(buttonData) {
    const phETab = document.getElementById('PhETab');

    for (const [key, value] of Object.entries(buttonData)) {
        const button = document.createElement('span');
        button.className = 'tablinks';
        button.innerHTML = value;
        button.setAttribute('onclick', `openPhE(event, '${key+"_PhE"}')`);
        phETab.appendChild(button);
    }
    const divider = document.createElement('span');
    divider.className = 'tablinks';
    divider.innerHTML = "---"
    divider.setAttribute('onclick', "addToPhEText(this, `\n------------`)");
    phETab.appendChild(divider);
}

function addToPhEText(element, text) {
    const textarea = document.getElementById('id_phe');
    textarea.value += (textarea.value ? '' : '') + text;
}

function openPhE(evt, sectionName) {
    const tabcontents = document.getElementsByClassName('tabcontent');
    for (let i = 0; i < tabcontents.length; i++) {
        tabcontents[i].style.display = 'none';
    }

    const tablinks = document.getElementsByClassName('tablinks');
    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(' active', '');
    }

    document.getElementById(sectionName).style.display = 'block';
    evt.currentTarget.className += ' active';
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
    "Limbs": "Limbs &#128170; &#129461;",
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
    "Anus": ["خون‌ریزی از مقعد", "درد هنگام مدفوع کردن", "مدفوع قیری‌رنگ"],
    "Nerves": ["گزگز انتهاها", "درد تیرکشنده به پا", "درد تیرکشنده به دست", "عدم احساس گرما و سرما"],
    "Limbs": ["سیانوز محیطی", "ادم انتهاها", ],
    "Muscuoskletal": ["درد دست", "درد پا", "درد کمر", "درد شانه", "ضعف عضلات", ],

};

const PhEData = {
    'VS': {
        'فشار سیستولی': ['110', '115', '120', '125', '130', '135', '140', '145', '150', '155', '160'],
        'فشار دیاستولی': ['60', '65', '70', '75', '80', '85', '90', '95', '100', '105', '110'],
        'دما': ['36.', '37.', '38.', '39.', '40.'],
        'ضربان قلب': ['40', '50', '60', '70', '80', '90', '100', '110', '120'],
        'نرخ تنفس': ['12', '14', '16', '18', '20', '22', '24', '26', '28'],
        'اشباع اکسیژن': ['80%', '85%', '90%', '95%', '97%', '98%', '99%', '100%'],
        'اشباع اکسیژن با ماسک': ['80%', '85%', '90%', '95%', '97%', '98%', '99%', '100%'],
    },
    'Skin': {
        'تورگور پوستی': ['نرمال', 'کاهش یافته', 'افزایش یافته']
    },
    'Eye': {
        'مردمک‌ها': ['responsive', 'mydriatic', 'miotic'],
        'عنبیه': ['inflamated', 'Kayser-Fleischer ring'],
        'اسکلرا': ['icteric', 'hyperemic', ],
        'ملتحمه': ['pale', 'inflamated', ],
        'شبکیه': ['neovascularization', ],
    },
    'Mouth': {
        'خشکی دهان': ['➕', '➖'],
        'برفک': ['➕', '➖'],
        'وضعیت بهداشت دهان و دندان': ['مناسب', 'نامناسب', ],
    },
    'Neck': {
        'تیروئید': ['nudularity', 'goiter', 'normal'],
        'گره‌های لنفاوی': ['firm', 'tender', 'circular'],
        'ورید ژوگولار': ['prominant', 'not seen', ],
    },

    'Breast': {
        'نگاه': ['inverted nipple', 'infalmation', ],
        'لمس': ['توده', 'لنف نود آگزیلاری', ],
    },

    'Heart': {
        'وجود Wide Pulse Pressure': ['➕', '➖'],
        'سمع S1': ['➕', '➖'],
        'سمع S2': ['➕', '➖'],
        'سمع S3': ['➕', '➖'],
        'سمع S4': ['➕', '➖'],
        'سوفل': ['Early Systolic', 'Midsystolic', 'Late Systolic', 'holosystolic',
            'Early Dyastolic', 'Middyastolic', 'Late Dyastolic', 'holodyastolic',
        ],
        'ارتوستاتیک هایپوتنشن': ['➕', '➖'],
        'ادم': ['➕➕➕', '➕➕', '➕', '➖'],
    },

    'Lungs': {
        'نگاه': ['barrel chest', 'pectus exavactum', 'scar', ],
        'سمع ریه': ['clear', 'wheeze', 'fine rhales', 'coarse rhales', 'کاهش صدا '],
        'دق': ['resonant', 'dull', ],
        'Chest Expansion': ['کافی و قرینه', 'کاهش در چپ', 'کاهش در راست', 'کاهش دو طرفه', ],
        'Tactile Fermitus': ['نرمال', 'افزایش یافته', 'کاهش یافته', ],
    },

    'Abdomen': {
        'نگاه': ['اسکار جراحی', 'دیستانسیون', 'فتق'],
        'سمع': ['کاهش تعداد صداها', 'صداهای نرمال', 'افزایش تعداد صدا'],
        'لمس': ['تندرنس', 'گاردینگ', 'ریباند تندرنس', 'علامت مورفی', 'توده', 'سپلنومگالی'],
        'دق': ['هپاتومگالی', 'آسیت', 'نفخ'],
    },

    'Anus': {
        'هموروئید': ['➕', '➖'],
        'فیشر': ['➕', '➖'],
        'فیستول': ['➕', '➖'],
        'TR': ['blood', 'melena', 'BPH', 'nodularity'],
    },

    'Nerves': {
        'رفلکس پتلا': ['➕', '➖'],
        'رفلکس آرنج': ['➕', '➖'],
        'نوروپاتی محیطی': ['➕', '➖'],
        'رفلکس آشیل': ['➕', '➖'],
        'علامت بابینسکی': ['➕', '➖'],
    },

    'Extremities': {
        'نبض‌ها': ['پر و قرینه', 'نامتقارن', 'ضعیف', 'بدون نبض'],
        'cyanosis': ['➕', '➖'],
        'clubbing': ['➕', '➖'],
        'اختلاف سایز': ['➕', '➖'],
        'اریتم پالمار': ['➕', '➖'],
    },

    'Muscuoskletal': {
        'فورس اندام فوقانی راست': ['5/5', '4/5', '3/5', '2/5', '1/5', '0'],
        'فورس اندام فوقانی چپ': ['5/5', '4/5', '3/5', '2/5', '1/5', '0'],
        'فورس اندام تحتانی راست': ['5/5', '4/5', '3/5', '2/5', '1/5', '0'],
        'فورس اندام تحتانی چپ': ['5/5', '4/5', '3/5', '2/5', '1/5', '0'],
        'علامت پاتریک': ['➕', '➖'],
    },

};

const PhEButtonData = {
    "VS": "Vital Signs &#129658;",
    "Skin": "Skin &#127773;",
    // "Skull": "Skull &#128128;",
    // "Ear": "Ear &#128066;",
    "Eye": "Eye &#128065;",
    // "Nose": "Nose &#128067;",
    "Mouth": "Mouth &#128068; &#129463;",
    // "Throat": "Throat &#127908;",
    "Neck": "Neck",
    // "Lymph": "Lymph Nodes &#129440;",
    // "Chest": "Chest &#129659;",
    "Breast": "Breast &#128089;",
    "Heart": "Heart &#129728;",
    "Lungs": "Lungs &#129729;",
    // "Vesseles": "Vesseles &#129656;",
    "Abdomen": "Abdomen &#129328;",
    // "Genitals": "Genitals &#129650;",
    "Anus": "Anus &#128701;",
    "Nerves": "Nerves &#129504;",
    "Extremities": "Extremities &#128400; &#129462;",
    "Muscuoskletal": "Muscuoskletal &#129470; &#129471;"
};
