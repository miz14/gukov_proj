export function emailInput(emailBlock) {
    const emailInput = document.createElement('input');
    emailInput.type = 'email';
    emailInput.id = 'email-input';
    emailInput.placeholder = 'Email';
    emailInput.maxlength = 50;
    emailInput.required = false;
    emailBlock.appendChild(emailInput);
    emailInput.isValid = () => /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(emailInput.value);
}
export function seteEmailRequired(required) {
    const emailInput = document.getElementById('email-input');
    emailInput.required = required;
}
export function getEmailValue() {
    return document.getElementById('email-input').value;
}