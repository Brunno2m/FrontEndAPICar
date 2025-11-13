from flask import Flask, request, jsonify, render_template, send_from_directory, session, redirect, url_for, flash
from flask_cors import CORS
import requests
import os
from functools import wraps

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# secret para sessões: configure via env `SECRET_KEY` em produção
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-me')

BACKEND_BASE = 'http://18.231.156.122:8080'

# armazenamento em memória para permitir operações de escrita locais
CARROS = []
CARROS_INITIALIZED = False

def seed_carros_from_remote():
    global CARROS, CARROS_INITIALIZED
    try:
        resp = requests.get(f"{BACKEND_BASE}/listarCarros", timeout=5)
        if resp.status_code == 200:
            CARROS = resp.json() if isinstance(resp.json(), list) else []
            CARROS_INITIALIZED = True
            app.logger.info(f"Carros inicializados a partir do backend remoto: {len(CARROS)} itens")
            return True
    except Exception:
        app.logger.exception('Não foi possível inicializar CARROS a partir do remoto')
    return False


def proxy_request(method, path, params=None, json_data=None):
    url = f"{BACKEND_BASE}{path}"
    try:
        resp = requests.request(method, url, params=params, json=json_data, timeout=10)
        headers = {}
        if 'content-type' in resp.headers:
            headers['Content-Type'] = resp.headers['content-type']
        # If successful (2xx/3xx/4xx handled by caller), return
        if resp.status_code < 400:
            return (resp.content, resp.status_code, headers)
        # If server returned error, attempt fallback for JSON bodies: send as form data
        if json_data is not None:
            try:
                form_resp = requests.post(url, data=json_data, timeout=10)
                form_headers = {}
                if 'content-type' in form_resp.headers:
                    form_headers['Content-Type'] = form_resp.headers['content-type']
                return (form_resp.content, form_resp.status_code, form_headers)
            except Exception:
                pass
        return (resp.content, resp.status_code, headers)
    except Exception as e:
        app.logger.exception('Erro ao conectar no backend remoto')
        return (jsonify({'error': 'Falha ao conectar no backend remoto', 'details': str(e)}), 502, {'Content-Type': 'application/json'})


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('user'):
            # preserve next
            return redirect(url_for('login', next=request.path))
        return fn(*args, **kwargs)
    return wrapper


@app.route('/')
@login_required
def index():
    return render_template('index.html', user=session.get('user'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # credenciais podem vir de variáveis de ambiente
    AUTH_USER = os.environ.get('AUTH_USER', 'admin')
    AUTH_PASS = os.environ.get('AUTH_PASS', 'secret')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == AUTH_USER and password == AUTH_PASS:
            session['user'] = username
            next_url = request.args.get('next') or url_for('index')
            return redirect(next_url)
        flash('Usuário ou senha inválidos')
        return render_template('login.html')
    # GET
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/api/getCarro')
def api_get_carro():
    # manter compatibilidade com GET (query param) e aceitar POST com JSON { modelo }
    if request.method == 'POST' or request.get_json(silent=True) is not None:
        data = request.get_json(silent=True) or {}
        modelo = data.get('modelo')
    else:
        modelo = request.args.get('modelo')

    # garantir que CARROS esteja inicializado
    if not CARROS_INITIALIZED:
        seed_carros_from_remote()

    # procurar no armazenamento local
    matches = [c for c in CARROS if c.get('modelo') == modelo]
    if matches:
        return jsonify(matches)

    # fallback para backend remoto (GET)
    params = {'modelo': modelo} if modelo else None
    body, status, headers = proxy_request('GET', '/getCarro', params=params)
    return (body, status, headers)


@app.route('/api/getCarro', methods=['POST'])
def api_get_carro_post():
    # roteia para a mesma lógica acima
    return api_get_carro()


@app.route('/api/listarCarros')
def api_listar_carros():
    # retornar a lista a partir do armazenamento local se possível
    if not CARROS_INITIALIZED:
        seed_carros_from_remote()
    return jsonify(CARROS)


@app.route('/api/saveCarro', methods=['POST'])
def api_save_carro():
    payload = request.get_json(force=True)
    # operações de escrita locais: atribuir novo id
    if not CARROS_INITIALIZED:
        seed_carros_from_remote()
    new_id = max([c.get('id', 0) for c in CARROS] or [0]) + 1
    novo = {'id': new_id, 'modelo': payload.get('modelo'), 'preco': payload.get('preco')}
    CARROS.append(novo)
    return jsonify(novo), 201


@app.route('/api/updateCarro', methods=['POST'])
def api_update_carro():
    payload = request.get_json(force=True)
    if not CARROS_INITIALIZED:
        seed_carros_from_remote()
    modelo = payload.get('modelo')
    novo_preco = payload.get('preco')
    for c in CARROS:
        if c.get('modelo') == modelo:
            c['preco'] = novo_preco
            return jsonify(c)
    return jsonify({'error': 'modelo não encontrado'}), 404


@app.route('/api/deleteCarro', methods=['POST'])
def api_delete_carro():
    # Accept JSON body or query param
    data = request.get_json(silent=True)
    if data and 'modelo' in data:
        modelo = data['modelo']
    else:
        modelo = request.args.get('modelo')
    if not CARROS_INITIALIZED:
        seed_carros_from_remote()
    before = len(CARROS)
    CARROS[:] = [c for c in CARROS if c.get('modelo') != modelo]
    after = len(CARROS)
    if after < before:
        return jsonify({'deleted': True})
    return jsonify({'deleted': False, 'message': 'modelo não encontrado'}), 404


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/debug/backend_status')
def backend_status():
    try:
        resp = requests.get(f"{BACKEND_BASE}/listarCarros", timeout=5)
        return jsonify({'ok': True, 'status_code': resp.status_code, 'content_length': len(resp.content)})
    except Exception as e:
        app.logger.exception('Erro ao contatar backend remoto')
        return jsonify({'ok': False, 'error': str(e)}), 502


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.logger.info(f"Iniciando Flask na porta {port} (binding 0.0.0.0)...")
    app.run(host='0.0.0.0', port=port, debug=False)