#!/bin/bash

# Script de inicialização para produção

echo "🚗 AutoPrime - Iniciando aplicação..."

# Carregar variáveis de ambiente
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Verificar se o MySQL está acessível
echo "📊 Verificando conexão com MySQL..."
python3 << EOF
import mysql.connector
import sys
import os

try:
    conn = mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=int(os.environ.get('DB_PORT', 3306)),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'root')
    )
    
    # Criar banco de dados se não existir
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS carros CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("✓ Banco de dados 'carros' verificado/criado")
    cursor.close()
    conn.close()
    sys.exit(0)
except Exception as e:
    print(f"✗ Erro ao conectar ao MySQL: {e}")
    print("Verifique se o MySQL está rodando e as credenciais estão corretas")
    sys.exit(1)
EOF

if [ $? -ne 0 ]; then
    echo "❌ Falha na verificação do banco de dados"
    exit 1
fi

echo "✓ Conexão com MySQL estabelecida"

# Iniciar aplicação com Gunicorn
echo "🚀 Iniciando servidor Gunicorn..."
gunicorn -c gunicorn.conf.py app:app
