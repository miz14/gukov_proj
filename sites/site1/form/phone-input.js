export function phoneInput(phoneBlock) {

    const phoneInput = document.createElement('input');
    phoneInput.type = 'tel';
    phoneInput.id = 'phone-input';
    phoneInput.placeholder = `Телефон`;
    phoneInput.required = true;
    phoneInput.autocomplete = 'tel';
    phoneInput.pattern = "[+]?[0-9]+";
    phoneInput.title = '+79999999999 или 89999999999';


    phoneBlock.appendChild(phoneInput);
}
export function setPhoneRequired(required) {
    const phoneInput = document.getElementById('phone-input');
    phoneInput.required = required;
}


export function setShowPhone(show) {
    if (show) {
        document.getElementById('phone-block').classList.remove('hidden');
    } else {
        document.getElementById('phone-block').classList.add('hidden');
    }

}
export function getPhoneValue() {
    return document.getElementById('phone-input').value;
}