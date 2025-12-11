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
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Configurações
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configuração do Banco de Dados MySQL
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'database': os.environ.get('DB_NAME', 'carros'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'root'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}


@contextmanager
def get_db_connection():
    """Context manager para conexões ao banco de dados"""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        yield connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()


def create_database_if_not_exists():
    """Cria o banco de dados se não existir"""
    try:
        # Conectar sem especificar o banco de dados
        config_without_db = DB_CONFIG.copy()
        db_name = config_without_db.pop('database')
        
        conn = mysql.connector.connect(**config_without_db)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.close()
        conn.close()
        print(f"✓ Banco de dados '{db_name}' verificado/criado")
        return True
    except Error as e:
        print(f"✗ Erro ao criar banco de dados: {e}")
        return False


def init_database():
    """Inicializa o banco de dados e cria a tabela se não existir"""
    try:
        # Primeiro garantir que o banco existe
        if not create_database_if_not_exists():
            raise Exception("Não foi possível criar o banco de dados")
        
        # Agora criar a tabela
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS carro (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    modelo VARCHAR(255) NOT NULL UNIQUE,
                    preco DECIMAL(12, 2) NOT NULL,
                    image VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_modelo (modelo)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            conn.commit()
            cursor.close()
            print("✓ Tabela 'carro' verificada/criada com sucesso")
    except Error as e:
        print(f"✗ Erro ao inicializar banco de dados: {e}")
        raise


def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Endpoints principais da API

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
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT preco FROM carro WHERE modelo = %s", (modelo,))
            carro = cursor.fetchone()
            cursor.close()
            
            if carro:
                return jsonify({'preco': float(carro['preco'])}), 200
            return jsonify({'error': 'Carro não encontrado'}), 404
    except Error as e:
        return jsonify({'error': f'Erro no banco de dados: {str(e)}'}), 500


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
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO carro (modelo, preco) VALUES (%s, %s)",
                (modelo, preco)
            )
            conn.commit()
            cursor.close()
            return jsonify({'success': True, 'id': cursor.lastrowid}), 201
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Modelo já existe. Use updateCarro para atualizar'}), 409
    except Error as e:
        return jsonify({'error': f'Erro no banco de dados: {str(e)}'}), 500


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
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM carro WHERE modelo = %s", (modelo,))
            conn.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            
            if rows_affected > 0:
                return jsonify({'success': True}), 200
            return jsonify({'error': 'Carro não encontrado'}), 404
    except Error as e:
        return jsonify({'error': f'Erro no banco de dados: {str(e)}'}), 500


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
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE carro SET preco = %s WHERE modelo = %s",
                (preco, modelo)
            )
            conn.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            
            if rows_affected > 0:
                return jsonify({'success': True}), 200
            return jsonify({'error': 'Carro não encontrado'}), 404
    except Error as e:
        return jsonify({'error': f'Erro no banco de dados: {str(e)}'}), 500


@app.route('/listarCarros', methods=['GET'])
def listar_carros():
    """
    Endpoint: listarCarros
    Método: GET
    Entrada: não tem
    Saída: lista de carros com preços
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, modelo, preco, image FROM carro ORDER BY id")
            carros = cursor.fetchall()
            cursor.close()
            
            # Converter Decimal para float
            for carro in carros:
                if carro.get('preco'):
                    carro['preco'] = float(carro['preco'])
            
            return jsonify(carros), 200
    except Error as e:
        return jsonify({'error': f'Erro no banco de dados: {str(e)}'}), 500





# Endpoints do frontend

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
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, modelo, preco, image FROM carro WHERE modelo = %s", (modelo,))
            matches = cursor.fetchall()
            cursor.close()
            
            for carro in matches:
                if carro.get('preco'):
                    carro['preco'] = float(carro['preco'])
            
            return jsonify(matches), 200
    except Error as e:
        return jsonify({'error': f'Erro no banco de dados: {str(e)}'}), 500


@app.route('/api/saveCarro', methods=['POST'])
def api_save_carro():
    """Wrapper para compatibilidade com frontend"""
    
    payload = request.get_json()
    modelo = payload.get('modelo')
    preco = payload.get('preco')
    
    if not modelo or preco is None:
        return jsonify({'error': 'Modelo e preço são obrigatórios'}), 400
    
    image = payload.get('image')
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "INSERT INTO carro (modelo, preco, image) VALUES (%s, %s, %s)",
                (modelo, preco, image)
            )
            conn.commit()
            new_id = cursor.lastrowid
            cursor.close()
            
            novo_carro = {'id': new_id, 'modelo': modelo, 'preco': preco}
            if image:
                novo_carro['image'] = image
            
            return jsonify(novo_carro), 201
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Modelo já existe. Use updateCarro para atualizar'}), 409
    except Error as e:
        return jsonify({'error': f'Erro no banco de dados: {str(e)}'}), 500


@app.route('/api/updateCarro', methods=['POST'])
def api_update_carro():
    """Wrapper para compatibilidade com frontend"""
    
    payload = request.get_json()
    modelo = payload.get('modelo')
    novo_preco = payload.get('preco')
    
    if not modelo or novo_preco is None:
        return jsonify({'error': 'Modelo e preço são obrigatórios'}), 400
    
    image = payload.get('image')
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            
            if image:
                cursor.execute(
                    "UPDATE carro SET preco = %s, image = %s WHERE modelo = %s",
                    (novo_preco, image, modelo)
                )
            else:
                cursor.execute(
                    "UPDATE carro SET preco = %s WHERE modelo = %s",
                    (novo_preco, modelo)
                )
            
            conn.commit()
            
            if cursor.rowcount > 0:
                cursor.execute("SELECT id, modelo, preco, image FROM carro WHERE modelo = %s", (modelo,))
                carro = cursor.fetchone()
                cursor.close()
                
                if carro and carro.get('preco'):
                    carro['preco'] = float(carro['preco'])
                
                return jsonify(carro), 200
            
            cursor.close()
            return jsonify({'error': 'Carro não encontrado'}), 404
    except Error as e:
        return jsonify({'error': f'Erro no banco de dados: {str(e)}'}), 500


@app.route('/api/deleteCarro', methods=['POST'])
def api_delete_carro():
    """Wrapper para compatibilidade com frontend"""
    
    data = request.get_json(silent=True)
    modelo = data.get('modelo') if data else request.args.get('modelo')
    
    if not modelo:
        return jsonify({'error': 'Modelo não informado'}), 400
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM carro WHERE modelo = %s", (modelo,))
            conn.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            
            if rows_affected > 0:
                return jsonify({'deleted': True}), 200
            return jsonify({'deleted': False, 'message': 'Carro não encontrado'}), 404
    except Error as e:
        return jsonify({'error': f'Erro no banco de dados: {str(e)}'}), 500


@app.route('/api/listarCarros', methods=['GET'])
def api_listar_carros():
    """Wrapper para compatibilidade com frontend"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, modelo, preco, image FROM carro ORDER BY id")
            carros = cursor.fetchall()
            cursor.close()
            
            for carro in carros:
                if carro.get('preco'):
                    carro['preco'] = float(carro['preco'])
            
            return jsonify(carros), 200
    except Error as e:
        return jsonify({'error': f'Erro no banco de dados: {str(e)}'}), 500


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
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM carro")
            result = cursor.fetchone()
            cursor.close()
            total = result[0] if result else 0
            
            return jsonify({
                'status': 'ok',
                'database': 'connected',
                'carros': total
            }), 200
    except Error as e:
        return jsonify({
            'status': 'error',
            'database': 'disconnected',
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("\n🚗 Backend AutoPrime - Iniciando...")
    print(f"📊 Conectando ao banco MySQL: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    
    try:
        init_database()
        port = int(os.environ.get('PORT', 8080))
        print(f"\n✓ Backend AutoPrime iniciado na porta {port}")
        print(f"📍 Acesse: http://localhost:{port}\n")
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"\n✗ Erro ao iniciar aplicação: {e}")
        print("Verifique se o MySQL está rodando e as credenciais estão corretas.\n")
        exit(1)