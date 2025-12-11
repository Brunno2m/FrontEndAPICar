#!/usr/bin/env python3
"""
Script para testar conexão com MySQL e configurar o ambiente
"""
import mysql.connector
from mysql.connector import Error
import os
import sys

# Configurações do banco de dados
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'root'),
}

DB_NAME = os.environ.get('DB_NAME', 'carros')

def test_connection():
    """Testa a conexão com o MySQL"""
    print("🔍 Testando conexão com MySQL...")
    print(f"   Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"   User: {DB_CONFIG['user']}")
    print(f"   Database: {DB_NAME}")
    print()
    
    try:
        # Tentar conectar sem especificar o banco
        print("1️⃣  Conectando ao servidor MySQL...")
        conn = mysql.connector.connect(**DB_CONFIG)
        print("   ✓ Conexão estabelecida com sucesso!")
        
        # Criar banco de dados se não existir
        print(f"\n2️⃣  Criando banco de dados '{DB_NAME}'...")
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"   ✓ Banco de dados '{DB_NAME}' pronto")
        
        # Selecionar o banco
        cursor.execute(f"USE {DB_NAME}")
        
        # Criar tabela
        print("\n3️⃣  Criando tabela 'carro'...")
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
        print("   ✓ Tabela 'carro' pronta")
        
        # Verificar quantos registros existem
        print("\n4️⃣  Verificando dados...")
        cursor.execute("SELECT COUNT(*) FROM carro")
        count = cursor.fetchone()[0]
        print(f"   ✓ Total de carros cadastrados: {count}")
        
        # Inserir dados de exemplo se a tabela estiver vazia
        if count == 0:
            print("\n5️⃣  Inserindo dados de exemplo...")
            sample_data = [
                ('Toyota Corolla', 125000.00),
                ('Honda Civic', 135000.00),
                ('Volkswagen Golf', 115000.00),
                ('Ford Focus', 95000.00),
                ('Chevrolet Onix', 75000.00),
            ]
            for modelo, preco in sample_data:
                try:
                    cursor.execute("INSERT INTO carro (modelo, preco) VALUES (%s, %s)", (modelo, preco))
                except mysql.connector.IntegrityError:
                    pass  # Já existe
            
            conn.commit()
            cursor.execute("SELECT COUNT(*) FROM carro")
            count = cursor.fetchone()[0]
            print(f"   ✓ {count} carros inseridos")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✅ CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*60)
        print("\n🚀 A aplicação está pronta para ser iniciada!")
        print("   Execute: python app.py")
        print("   Ou com Gunicorn: ./start.sh\n")
        
        return True
        
    except Error as e:
        print(f"\n❌ ERRO: {e}")
        print("\n💡 Verifique:")
        print("   1. MySQL está instalado e rodando")
        print("   2. Credenciais estão corretas (user: root, password: root)")
        print("   3. Usuário tem permissões necessárias")
        print("\n🔧 Para instalar MySQL:")
        print("   Ubuntu/Debian: sudo apt-get install mysql-server")
        print("   CentOS/RHEL: sudo yum install mysql-server")
        print("   macOS: brew install mysql")
        print("\n🔧 Para iniciar MySQL:")
        print("   Linux: sudo service mysql start")
        print("   macOS: brew services start mysql\n")
        
        return False

if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)
