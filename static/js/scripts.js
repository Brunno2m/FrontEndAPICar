const API_URL = '';// local proxy (/api)

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('carros-container');
    if (container) container.textContent = 'Clique em "Listar Carros" para carregar a lista.';
});

// estado do painel de listagem
let listaVisivel = false;

function toggleListarCarros() {
    const btn = document.getElementById('listar-carros-btn');
    const container = document.getElementById('carros-container');
    if (!listaVisivel) {
        // mostrar e carregar
        btn.textContent = 'Ocultar Lista';
        container.classList.remove('collapsed');
        listarCarros();
        listaVisivel = true;
    } else {
        // ocultar
        btn.textContent = 'Listar Carros';
        container.classList.add('collapsed');
        listaVisivel = false;
    }
}

function listarCarros() {
    console.log('Iniciando a função listarCarros...');
    showSpinner();
    fetch(`/api/listarCarros`)
        .then(response => {
            hideSpinner();
            console.log('Resposta recebida:', response);
            if (!response.ok) {
                throw new Error(`Erro ao listar carros: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Dados recebidos da API:', data);
            const container = document.getElementById('carros-container');
            container.innerHTML = '';
            if (data.length === 0) {
                container.textContent = 'Nenhum carro encontrado.';
                return;
            }
            data.forEach(carro => {
                const div = document.createElement('div');
                div.className = 'carro-item';
                div.innerHTML = `<strong>ID:</strong> ${carro.id} <br> <strong>Modelo:</strong> ${carro.modelo} <br> <strong>Preço:</strong> R$ ${carro.preco}`;
                container.appendChild(div);
            });
            showToast('success', 'Lista atualizada');
        })
        .catch(error => {
            hideSpinner();
            console.error('Erro capturado na função listarCarros:', error);
            const container = document.getElementById('carros-container');
            container.textContent = 'Erro ao carregar a lista de carros.';
            showToast('error', 'Falha ao listar carros');
        });
}

function getCarro(modelo) {
    fetch(`/api/getCarro`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ modelo })
    })
        .then(response => {
            if (!response.ok) throw new Error(`Erro ao buscar carro: ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log('Carro encontrado:', data);
            const container = document.getElementById('carros-container');
            container.innerHTML = '';
            if (!data || data.length === 0) {
                container.textContent = 'Carro não encontrado.';
                return;
            }
            data.forEach(carro => {
                const div = document.createElement('div');
                div.className = 'carro-item';
                div.innerHTML = `<strong>ID:</strong> ${carro.id} <br> <strong>Modelo:</strong> ${carro.modelo} <br> <strong>Preço:</strong> R$ ${carro.preco}`;
                container.appendChild(div);
            });
        })
        .catch(error => console.error('Erro ao buscar carro:', error));
}

function saveCarro(modelo, preco) {
    showSpinner();
    fetch(`/api/saveCarro`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ modelo, preco })
    })
        .then(response => {
            hideSpinner();
            if (!response.ok) throw new Error('Falha ao salvar');
            return response.json();
        })
        .then(data => {
            console.log('Carro salvo:', data);
            showToast('success', 'Carro salvo');
            listarCarros();
        })
        .catch(error => { hideSpinner(); console.error('Erro ao salvar carro:', error); showToast('error','Erro ao salvar'); });
}

function deleteCarro(modelo) {
    showSpinner();
    fetch(`/api/deleteCarro`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ modelo })
    })
        .then(response => {
            hideSpinner();
            if (!response.ok) throw new Error('Falha ao deletar');
            return response.json();
        })
        .then(data => {
            console.log('Carro deletado:', data);
            showToast('success','Carro deletado');
            listarCarros();
        })
        .catch(error => { hideSpinner(); console.error('Erro ao deletar carro:', error); showToast('error','Erro ao deletar'); });
}

function updateCarro(modelo, preco) {
    showSpinner();
    fetch(`/api/updateCarro`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ modelo, preco })
    })
        .then(response => {
            hideSpinner();
            if (!response.ok) throw new Error('Falha ao atualizar');
            return response.json();
        })
        .then(data => {
            console.log('Carro atualizado:', data);
            showToast('success','Carro atualizado');
            listarCarros();
        })
        .catch(error => { hideSpinner(); console.error('Erro ao atualizar carro:', error); showToast('error','Erro ao atualizar'); });
}

/* spinner and toast helpers */
function showSpinner(){
    const s = document.getElementById('spinner'); if(s) s.classList.remove('hidden');
}
function hideSpinner(){
    const s = document.getElementById('spinner'); if(s) s.classList.add('hidden');
}

function showToast(type, message, timeout=3500){
    const container = document.getElementById('toast-container');
    if(!container) return;
    const t = document.createElement('div');
    t.className = `toast ${type}`;
    t.textContent = message;
    container.appendChild(t);
    setTimeout(()=>{ t.style.opacity = '0'; setTimeout(()=> t.remove(), 400); }, timeout);
}