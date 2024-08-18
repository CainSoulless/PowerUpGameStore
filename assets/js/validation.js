document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector('.needs-validation');

    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }

        // Se le agrega la clase was-validated según la documentación de Bootstrap
        form.classList.add('was-validated');

        if (!policyPasswordValidation() || !validateBirthday()) {
            event.preventDefault();
            event.stopPropagation();
        }
    }, false);

    var passwordInputs = document.querySelectorAll(".password-input");

    passwordInputs.forEach(function(input) {
        input.addEventListener("input", function(event) {
            var otherInput = [...passwordInputs].find(element => element !== input);

            if (isEqualPassword(input.value, otherInput.value)) {
                validatePassword();
            }
        });
    });
});

function validateBirthday() {
    var birthdayInput = document.getElementById("birthdayInput");
    var birthdayValue = birthdayInput.value;
    var birthDate = new Date(birthdayValue);
    var today = new Date();
    var age = today.getFullYear() - birthDate.getFullYear();
    var monthDiff = today.getMonth() - birthDate.getMonth();

    if (birthDate > today) {
        birthdayInput.setCustomValidity("La fecha no puede ser en el futuro.");
        return false;
    } else if (age < 13 || (age === 13 && monthDiff < 0)) {
        birthdayInput.setCustomValidity("Debes tener al menos 18D años.");
        return false;
    } else {
        birthdayInput.setCustomValidity("");
        return true;
    }
}

function validatePassword() {
    // Revisar la coincidencia de las contraseñas al cambiar el valor en ambos campos
    document.getElementById('passwordInput').addEventListener('input', validatePassword);
    document.getElementById('passwordConfirmationInput').addEventListener('input', validatePassword);

    var password = document.getElementById('passwordInput').value;
    var confirmPassword = document.getElementById('passwordConfirmationInput').value;

    if (password === confirmPassword) {
        document.getElementById('passwordConfirmationInput').setCustomValidity('');
    } else {
        document.getElementById('passwordConfirmationInput').setCustomValidity('Las contraseñas no coinciden.');
    }
}

function policyPasswordValidation() {
    var passwordInput = document.getElementById('passwordInput').value;

    // Se usa regex para deteminar si posee un numero y una letra mayuscula.

    var containsNumer = /\d/.test(passwordInput);
    var containsUpper = /[A-Z]/.test(passwordInput);

    if (containsNumer && containsUpper) {
        if (passwordInput.length >= 6 || passwordInput <= 18) {
            return true;
        } else {
            alert("La contraseña debe tener entre 6 y 18 caracteres.")
            return false;
        }
    } else {
        alert("La contraseña debe de tener al menos un numero y letra mayuscula.")
        return false;
    }
}

function isEqualPassword(password, confirmPassword) {
    if (password !== confirmPassword) {
        document.getElementById('passwordConfirmationInput').classList.add('is-invalid');
        document.getElementById('passwordConfirmationInput').classList.remove('is-valid');
        document.getElementById('passwordInput').classList.add('is-invalid');
        document.getElementById('passwordInput').classList.remove('is-valid');
        return false;
    } else {
        document.getElementById('passwordConfirmationInput').classList.remove('is-invalid');
        document.getElementById('passwordConfirmationInput').classList.add('is-valid');
        document.getElementById('passwordInput').classList.remove('is-invalid');
        document.getElementById('passwordInput').classList.add('is-valid');
        return true;
    }
}
