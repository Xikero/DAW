// Espera a que el documento esté completamente cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', function() {

    // Función para obtener las incidencias desde el servidor
    const fetchIncidents = () => {
        fetch('/incidents') // Realiza una solicitud GET a la ruta /incidents
        .then(response => response.json()) // Convierte la respuesta a formato JSON
        .then(data => {
            const tableBody = document.getElementById('incidents-table').getElementsByTagName('tbody')[0];
            tableBody.innerHTML = ''; // Limpia las filas existentes en la tabla
            data.forEach(incident => {
                // Crea una nueva fila para cada incidencia
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${incident.id}</td>
                    <td>${incident.description}</td>
                    <td>${incident.status}</td>
                    <td>${incident.created_at}</td>
                `;
                tableBody.appendChild(row); // Añade la fila a la tabla
            });
        })
        .catch(error => console.error('Error fetching incidents:', error)); // Maneja errores de la solicitud
    };

    // Llama a la función para obtener las incidencias al cargar la página
    fetchIncidents();

    // Añade un evento al formulario de incidencias para manejar el envío de datos
    document.getElementById('incident-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Evita el comportamiento por defecto del formulario
        const description = document.getElementById('description').value; // Obtiene el valor de la descripción

        // Realiza una solicitud POST a la ruta /incidents para crear una nueva incidencia
        fetch('/incidents', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' // Especifica el tipo de contenido
            },
            body: JSON.stringify({ description: description }) // Envía los datos en formato JSON
        })
        .then(response => response.json()) // Convierte la respuesta a formato JSON
        .then(data => {
            console.log('Incident created:', data); // Imprime la respuesta en la consola
            fetchIncidents(); // Vuelve a obtener las incidencias para actualizar la tabla
        })
        .catch(error => console.error('Error creating incident:', error)); // Maneja errores de la solicitud
    });
});
