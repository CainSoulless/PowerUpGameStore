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
    .then(response => response.json()) // Asegúrate de que el backend retorne JSON
    .then(data => {
        // Abre el modal después de añadir el producto
        var modal = new bootstrap.Modal(document.getElementById('cartModal'));
        modal.show();
    })
    .catch(error => console.error('Error:', error));
});