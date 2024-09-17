document.getElementById('carritoForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita la recarga de la página

    var form = this;

    fetch(form.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: new FormData(form)
    })
    .then(response => {
        // Verificar si la respuesta es exitosa y devolver JSON, de lo contrario, devolver un error
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Si el backend responde correctamente, mostrar el modal
        var modal = new bootstrap.Modal(document.getElementById('cartModal'));
        modal.show();
    })
    .catch(error => {
        // Mostrar el modal incluso si ocurre un error en la llamada
        var modal = new bootstrap.Modal(document.getElementById('cartModal'));
        modal.show();
        console.error('Error:', error);
    });
});
