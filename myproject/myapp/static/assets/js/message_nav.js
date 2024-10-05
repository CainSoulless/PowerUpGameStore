window.onload = function() {
    var alertMessages = document.querySelectorAll('.alert');

    alertMessages.forEach(function(message) {
        setTimeout(function() {
            message.classList.remove('show'); // Oculta el mensaje con la clase Bootstrap
        }, 2000); // 3 segundos (3000 milisegundos)
    });
};
