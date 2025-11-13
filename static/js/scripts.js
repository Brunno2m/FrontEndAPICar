const API_URL = '';// local proxy (/api)

// dados em memória para renderização e filtro
let carrosData = [];

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('carros-container');
    if (container) container.textContent = 'Clique em "Listar Carros" para carregar a lista.';
    // ligar submit do form add para usar nossa função saveCarro
    const addForm = document.getElementById('add-carro-form');
    if(addForm){
        addForm.addEventListener('submit', function(e){ e.preventDefault(); const modelo = document.getElementById('modelo').value; const preco = document.getElementById('preco').value; saveCarro(modelo, preco); });
    }
    const updateForm = document.getElementById('update-carro-form');
    if(updateForm){
        updateForm.addEventListener('submit', function(e){ e.preventDefault(); const modelo = document.getElementById('update-modelo').value; const preco = document.getElementById('update-preco').value; updateCarro(modelo, preco); });
    }
    const deleteForm = document.getElementById('delete-carro-form');
    if(deleteForm){
        deleteForm.addEventListener('submit', function(e){ e.preventDefault(); const modelo = document.getElementById('delete-modelo').value; deleteCarro(modelo); });
    }
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
            carrosData = Array.isArray(data) ? data : [];
            renderCards(carrosData);
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
            carrosData = Array.isArray(data) ? data : [];
            renderCards(carrosData);
        })
        .catch(error => console.error('Erro ao buscar carro:', error));
}

function saveCarro(modelo, preco) {
    // validação básica
    if(!modelo || String(modelo).trim().length === 0){ showToast('error','Preencha o modelo'); return; }
    const precoNum = Number(preco);
    if(!preco || isNaN(precoNum) || precoNum <= 0){ showToast('error','Preço deve ser maior que zero'); return; }

    // checar arquivo de imagem (opcional)
    const fileInput = document.getElementById('image');
    const file = fileInput && fileInput.files && fileInput.files[0];

    const doSave = (imageFilename) => {
        showSpinner();
        fetch(`/api/saveCarro`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ modelo, preco: precoNum, image: imageFilename })
        })
        .then(response => { hideSpinner(); if(!response.ok) throw new Error('Falha ao salvar'); return response.json(); })
        .then(data => { console.log('Carro salvo:', data); showToast('success','Carro salvo'); listarCarros(); if(fileInput) fileInput.value=''; })
        .catch(error => { hideSpinner(); console.error('Erro ao salvar carro:', error); showToast('error','Erro ao salvar'); });
    };

    if(file){
        // upload primeiro
        const fd = new FormData(); fd.append('file', file);
        showSpinner();
        fetch('/api/uploadImage', { method: 'POST', body: fd })
            .then(r=>{ hideSpinner(); if(!r.ok) throw new Error('Falha no upload'); return r.json(); })
            .then(res=>{ doSave(res.filename); })
            .catch(err=>{ hideSpinner(); console.error('Erro upload:', err); showToast('error','Falha no upload de imagem'); });
    } else {
        doSave(null);
    }
}

function deleteCarro(modelo) {
    if(!modelo || String(modelo).trim().length === 0){ showToast('error','Informe o modelo a deletar'); return; }
    if(!confirm(`Confirma exclusão do modelo "${modelo}" ?`)) return;
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
    if(!modelo || String(modelo).trim().length === 0){ showToast('error','Preencha o modelo'); return; }
    const precoNum = Number(preco);
    if(!preco || isNaN(precoNum) || precoNum <= 0){ showToast('error','Preço deve ser maior que zero'); return; }
    showSpinner();
    fetch(`/api/updateCarro`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ modelo, preco: precoNum })
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

/* renderização e utilitários */
function formatPrice(value){
    const num = Number(value) || 0;
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(num);
}

function renderCards(list){
    const container = document.getElementById('carros-container');
    if(!container) return;
    container.innerHTML = '';
    if(!list || list.length === 0){
        container.innerHTML = '<div class="empty">Nenhum carro encontrado.</div>';
        return;
    }
    list.forEach(carro => {
        const div = document.createElement('div');
        div.className = 'carro-item';
        const initials = (carro.modelo || '—').split(' ').map(s => s[0]).filter(Boolean).slice(0,2).join('').toUpperCase();
        div.innerHTML = `
            <div class="carro-thumb" aria-hidden="true"><span>${escapeHtml(initials)}</span></div>
            <div class="carro-details">
                <div class="carro-title"><strong>${escapeHtml(carro.modelo || '—')}</strong></div>
                <div class="carro-meta">ID: ${carro.id ?? '—'}</div>
                <div class="carro-price">${formatPrice(carro.preco)}</div>
            </div>
        `;
        container.appendChild(div);
    });
}

function escapeHtml(str){
    return String(str).replace(/[&<>"']/g, function(m){ return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[m]; });
}

// busca client-side: filtra carro por modelo ou id
function filterByQuery(q){
    const ql = (q || '').toLowerCase().trim();
    if(!ql) return carrosData;
    return carrosData.filter(c => {
        const modelo = String(c.modelo || '').toLowerCase();
        const id = String(c.id || '');
        return modelo.includes(ql) || id.includes(ql);
    });
}

// debounce util
function debounce(fn, wait=200){
    let t;
    return function(...args){ clearTimeout(t); t = setTimeout(()=> fn.apply(this,args), wait); };
}

// connect search input
document.addEventListener('DOMContentLoaded', () => {
    const search = document.getElementById('search');
    if(search){
        search.addEventListener('input', debounce(function(e){
            const q = e.target.value;
            const filtered = filterByQuery(q);
            renderCards(filtered);
        }, 180));
    }
});