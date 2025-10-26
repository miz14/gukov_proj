import { phoneInput, getPhoneValue, setPhoneRequired } from './phone-input.js';
import { emailInput, getEmailValue, seteEmailRequired } from './email-input.js';

const form = document.getElementById('contact-form');

const nameInput = document.createElement('input');
nameInput.type = 'name';
nameInput.id = 'form-name';
nameInput.placeholder = 'Ваше имя';
nameInput.required = true;
nameInput.maxlength = 50;
form.appendChild(nameInput);


const radioBlock = document.createElement('div');
radioBlock.id = 'radio-block';
form.appendChild(radioBlock);

const radioData = [
    {
        value: 'phone',
        label: 'Телефон'
    },
    {
        value: 'email',
        label: 'Email'
    }
]
radioData.forEach((item, idx) => {
    const radioItem = document.createElement('div');
    radioItem.className = 'radio-item';
    radioBlock.appendChild(radioItem);

    const radio = document.createElement('input');
    radio.type = 'radio';
    radio.id = item.value + '-radio';
    radio.name = 'phone_or_email';
    radio.value = item.value;
    if (idx === 0) {
        radio.checked = true;
    }
    radio.addEventListener('change', () => {
        if (radio.value === 'phone') {
            phoneBlock.classList.remove('hidden');
            emailBlock.classList.add('hidden');
            emailBlock.children[0].value = '';
            setPhoneRequired(true);
            seteEmailRequired(false);
        } else {
            emailBlock.classList.remove('hidden');
            phoneBlock.classList.add('hidden');
            phoneBlock.children[2].value = '';
            setPhoneRequired(false);
            seteEmailRequired(true);
        }
    })

    const label = document.createElement('label');
    label.htmlFor = item.value + '-radio';
    label.textContent = item.label;

    radioItem.appendChild(radio);
    radioItem.appendChild(label);
})

const phoneBlock = document.createElement('div');
phoneBlock.id = 'phone-block';

phoneInput(phoneBlock);
form.appendChild(phoneBlock);

const emailBlock = document.createElement('div');
emailBlock.id = 'email-block';
emailBlock.className = 'hidden';

emailInput(emailBlock);
form.appendChild(emailBlock);

const textArea = document.createElement('textarea');
textArea.id = 'text-area';
textArea.placeholder = 'Ваше сообщение';
textArea.required = true;
form.appendChild(textArea);

const button = document.createElement('button');
button.id = 'form-button';
button.textContent = 'Отправить заявку';
button.type = 'submit';
form.appendChild(button);

form.onsubmit = async (e) => {
    if (!form.checkVisibility()) {
        alert('Заполните обязательные поля');
        return
    }
    e.preventDefault();
    const send_data = {
        service: 'Юридические услуги в сфере пенсионного права',
        sent_from: window.location.hostname,
        name: nameInput.value,
        phone_or_email: document.querySelector('input[name="phone_or_email"]:checked').value,
        phone: getPhoneValue(),
        email: getEmailValue(),
        message: textArea.value
    }
    button.disabled = true;
    button.textContent = 'Отправка...';
    try {
        const response = await fetch('/api/send_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(send_data)
        });
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.detail?.message || 'Произошла ошибка отправки данных');
        }
        button.disabled = false;
        button.textContent = 'Отправить заявку';
        alert('Данные успешно отправлены');
    } catch (e) {
        button.disabled = false;
        button.textContent = 'Отправить заявку';
        alert('Не удалось отправить заявку')
    }
}