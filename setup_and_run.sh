#!/bin/bash

# Script de setup completo para deploy em produção
# Este script prepara o ambiente MySQL e inicia a aplicação

echo "=========================================="
echo "🚀 AutoPrime - Setup de Produção"
echo "=========================================="
echo ""

# Carregar variáveis de ambiente do arquivo .env se existir
if [ -f .env ]; then
    echo "📄 Carregando variáveis de ambiente do .env"
    export $(grep -v '^#' .env | xargs)
fi

# Definir valores padrão
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-3306}"
DB_NAME="${DB_NAME:-carros}"
DB_USER="${DB_USER:-root}"
DB_PASSWORD="${DB_PASSWORD:-root}"
PORT="${PORT:-8080}"

echo "📊 Configuração do Banco de Dados:"
echo "   Host: $DB_HOST:$DB_PORT"
echo "   Database: $DB_NAME"
echo "   User: $DB_USER"
echo ""

# Testar conexão e configurar banco de dados usando Python
echo "🔍 Testando conexão e configurando banco de dados..."
python3 test_mysql_connection.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Falha ao configurar o banco de dados"
    echo "   O servidor continuará tentando conectar ao iniciar..."
    echo ""
fi

echo ""
echo "=========================================="
echo "🌐 Iniciando Servidor de Produção"
echo "=========================================="
echo ""
echo "🔧 Servidor: Gunicorn"
echo "🔌 Porta: $PORT"
echo "👷 Workers: $(python3 -c 'import multiprocessing; print(multiprocessing.cpu_count() * 2 + 1)')"
echo ""

# Iniciar aplicação com Gunicorn
exec gunicorn -c gunicorn.conf.py app:app
