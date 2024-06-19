async function uploadZip() {
    const zipInput = document.getElementById('zipInput');
    const zipFile = zipInput.files[0];

    if (!zipFile) {
        console.error('Nenhum arquivo ZIP selecionado.');
        return;
    }

    const formData = new FormData();
    formData.append('zip_file', zipFile);

    try {
        const response = await fetch('/foldermaster/upload-folder/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // Adicionar token CSRF para Django
            }
        });

        if (response.ok) {
            console.log('Pasta enviada com sucesso!');
            window.location.href = '/foldermaster/foldermanagement/'; // Redirecionar para a página de gerenciamento de pastas
        } else {
            console.error('Erro ao enviar pasta:', response.statusText);
        }
    } catch (error) {
        console.error('Erro ao enviar pasta:', error);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
