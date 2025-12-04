"""
Backend Sistema AutoPrime - Loja de Veículos
Porta: 8080
"""

from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import json
import time

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Configurações
CARROS_FILE = 'carros.json'
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Banco de dados em memória
CARROS = []


def carregar_dados():
    """Carrega os carros do arquivo JSON"""
    global CARROS
    if os.path.exists(CARROS_FILE):
        with open(CARROS_FILE, 'r', encoding='utf-8') as f:
            CARROS = json.load(f)
    else:
        CARROS = []
        salvar_dados()


def salvar_dados():
    """Salva os carros no arquivo JSON"""
    with open(CARROS_FILE, 'w', encoding='utf-8') as f:
        json.dump(CARROS, f, ensure_ascii=False, indent=2)


# ============================================================================
# ENDPOINTS DA API - Sistema AutoPrime
# ============================================================================

@app.route('/getCarro', methods=['POST'])
def get_carro():
    """
    Endpoint: getCarro
    Método: POST
    Entrada: modelo (string)
    Saída: preço do carro
    """
    
    # Aceitar tanto JSON quanto form-data para compatibilidade
    if request.is_json:
        data = request.get_json()
        modelo = data.get('modelo')
    else:
        modelo = request.form.get('modelo')
    
    if not modelo:
        return jsonify({'error': 'Modelo não informado'}), 400
    
    # Buscar o carro pelo modelo
    for carro in CARROS:
        if carro.get('modelo') == modelo:
            return jsonify({'preco': carro.get('preco')}), 200
    
    return jsonify({'error': 'Carro não encontrado'}), 404


@app.route('/saveCarro', methods=['POST'])
def save_carro():
    """
    Endpoint: saveCarro
    Método: POST
    Entrada: modelo, preço (ex: BWM,350000)
    Saída: não tem
    """
    
    # Aceitar tanto JSON quanto form-data
    if request.is_json:
        data = request.get_json()
        modelo = data.get('modelo')
        preco = data.get('preco')
    else:
        modelo = request.form.get('modelo')
        preco = request.form.get('preco')
    
    if not modelo or preco is None:
        return jsonify({'error': 'Modelo e preço são obrigatórios'}), 400
    
    # Converter preço para número
    try:
        preco = float(preco)
    except (ValueError, TypeError):
        return jsonify({'error': 'Preço inválido'}), 400
    
    # Verificar se já existe
    for carro in CARROS:
        if carro.get('modelo') == modelo:
            return jsonify({'error': 'Modelo já existe. Use updateCarro para atualizar'}), 409
    
    # Gerar ID único
    new_id = max([c.get('id', 0) for c in CARROS], default=0) + 1
    
    # Criar novo carro
    novo_carro = {
        'id': new_id,
        'modelo': modelo,
        'preco': preco
    }
    
    CARROS.append(novo_carro)
    save_carros_to_file()
    
    return jsonify({'success': True}), 201


@app.route('/deleteCarro', methods=['POST'])
def delete_carro():
    """
    Endpoint: deleteCarro
    Método: POST
    Entrada: modelo (ex: BWM)
    Saída: não tem
    """
    
    # Aceitar tanto JSON quanto form-data
    if request.is_json:
        data = request.get_json()
        modelo = data.get('modelo')
    else:
        modelo = request.form.get('modelo')
    
    if not modelo:
        return jsonify({'error': 'Modelo não informado'}), 400
    
    # Buscar e remover o carro
    inicial = len(CARROS)
    CARROS[:] = [c for c in CARROS if c.get('modelo') != modelo]
    
    if len(CARROS) < inicial:
        save_carros_to_file()
        return jsonify({'success': True}), 200
    
    return jsonify({'error': 'Carro não encontrado'}), 404


@app.route('/updateCarro', methods=['POST'])
def update_carro():
    """
    Endpoint: updateCarro
    Método: POST
    Entrada: modelo, preço (ex: BWM,375000)
    Saída: não tem
    """
    
    # Aceitar tanto JSON quanto form-data
    if request.is_json:
        data = request.get_json()
        modelo = data.get('modelo')
        preco = data.get('preco')
    else:
        modelo = request.form.get('modelo')
        preco = request.form.get('preco')
    
    if not modelo or preco is None:
        return jsonify({'error': 'Modelo e preço são obrigatórios'}), 400
    
    # Converter preço para número
    try:
        preco = float(preco)
    except (ValueError, TypeError):
        return jsonify({'error': 'Preço inválido'}), 400
    
    # Buscar e atualizar o carro
    for carro in CARROS:
        if carro.get('modelo') == modelo:
            carro['preco'] = preco
            save_carros_to_file()
            return jsonify({'success': True}), 200
    
    return jsonify({'error': 'Carro não encontrado'}), 404


@app.route('/listarCarros', methods=['GET'])
def listar_carros():
    """
    Endpoint: listarCarros
    Método: GET
    Entrada: não tem
    Saída: lista de carros com preços
    """
    return jsonify(CARROS), 200


@app.route('/teste', methods=['GET'])
def teste():
    """
    Endpoint: teste
    Método: GET
    Retorna status do sistema
    """
    return jsonify({
        'status': 'ok',
        'message': 'Backend AutoPrime funcionando',
        'total_carros': len(CARROS),
        'timestamp': time.time()
    }), 200


# ============================================================================
# ENDPOINTS PARA COMPATIBILIDADE COM FRONTEND EXISTENTE
# ============================================================================

@app.route('/')
def index():
    """Serve a página principal do frontend"""
    return render_template('index.html')


@app.route('/api/getCarro', methods=['POST'])
def api_get_carro():
    """Wrapper para compatibilidade com frontend - retorna objeto completo"""
    
    data = request.get_json()
    modelo = data.get('modelo') if data else None
    
    if not modelo:
        return jsonify([]), 200
    
    # Retornar lista de carros que correspondem (frontend espera array)
    matches = [c for c in CARROS if c.get('modelo') == modelo]
    return jsonify(matches), 200


@app.route('/api/saveCarro', methods=['POST'])
def api_save_carro():
    """Wrapper para compatibilidade com frontend"""
    
    payload = request.get_json()
    modelo = payload.get('modelo')
    preco = payload.get('preco')
    
    if not modelo or preco is None:
        return jsonify({'error': 'Modelo e preço são obrigatórios'}), 400
    
    # Verificar se já existe (evitar duplicação)
    for carro in CARROS:
        if carro.get('modelo') == modelo:
            return jsonify({'error': 'Modelo já existe. Use updateCarro para atualizar'}), 409
    
    # Gerar ID único
    new_id = max([c.get('id', 0) for c in CARROS], default=0) + 1
    
    novo_carro = {
        'id': new_id,
        'modelo': modelo,
        'preco': preco
    }
    
    # Adicionar imagem se fornecida
    if payload.get('image'):
        novo_carro['image'] = payload.get('image')
    
    CARROS.append(novo_carro)
    save_carros_to_file()
    
    return jsonify(novo_carro), 201


@app.route('/api/updateCarro', methods=['POST'])
def api_update_carro():
    """Wrapper para compatibilidade com frontend"""
    
    payload = request.get_json()
    modelo = payload.get('modelo')
    novo_preco = payload.get('preco')
    
    if not modelo or novo_preco is None:
        return jsonify({'error': 'Modelo e preço são obrigatórios'}), 400
    
    for carro in CARROS:
        if carro.get('modelo') == modelo:
            carro['preco'] = novo_preco
            if payload.get('image'):
                carro['image'] = payload.get('image')
            save_carros_to_file()
            return jsonify(carro), 200
    
    return jsonify({'error': 'Carro não encontrado'}), 404


@app.route('/api/deleteCarro', methods=['POST'])
def api_delete_carro():
    """Wrapper para compatibilidade com frontend"""
    
    data = request.get_json(silent=True)
    modelo = data.get('modelo') if data else request.args.get('modelo')
    
    if not modelo:
        return jsonify({'error': 'Modelo não informado'}), 400
    
    inicial = len(CARROS)
    CARROS[:] = [c for c in CARROS if c.get('modelo') != modelo]
    
    if len(CARROS) < inicial:
        save_carros_to_file()
        return jsonify({'deleted': True}), 200
    
    return jsonify({'deleted': False, 'message': 'Carro não encontrado'}), 404


@app.route('/api/listarCarros', methods=['GET'])
def api_listar_carros():
    """Wrapper para compatibilidade com frontend"""
    return jsonify(CARROS), 200


@app.route('/api/uploadImage', methods=['POST'])
def api_upload_image():
    """Endpoint para upload de imagens dos carros"""
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Arquivo sem nome'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Adicionar timestamp para evitar conflitos
        filename = f"{int(time.time())}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return jsonify({
            'filename': filename,
            'url': f"/static/uploads/{filename}"
        }), 200
    
    return jsonify({'error': 'Tipo de arquivo não permitido'}), 400


@app.route('/health')
def health():
    """Endpoint de health check"""
    return jsonify({'status': 'ok', 'carros': len(CARROS)}), 200


if __name__ == '__main__':
    carregar_dados()
    port = int(os.environ.get('PORT', 8080))
    print(f"\n🚗 Backend AutoPrime iniciado na porta {port}")
    print(f"📍 Acesse: http://localhost:{port}")
    print(f"📊 Carros cadastrados: {len(CARROS)}\n")
    app.run(host='0.0.0.0', port=port, debug=False)