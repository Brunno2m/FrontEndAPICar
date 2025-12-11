#!/bin/bash

echo "🔍 Verificando ambiente MySQL..."

# Verificar se o MySQL está instalado
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL não está instalado"
    echo ""
    echo "📦 Para instalar o MySQL:"
    echo "   Ubuntu/Debian: sudo apt-get update && sudo apt-get install mysql-server"
    echo "   CentOS/RHEL: sudo yum install mysql-server"
    echo "   macOS: brew install mysql"
    exit 1
fi

echo "✓ MySQL está instalado"

# Verificar se o MySQL está rodando
if ! mysqladmin ping -h"localhost" --silent 2>/dev/null; then
    echo "❌ MySQL não está rodando"
    echo ""
    echo "🚀 Para iniciar o MySQL:"
    echo "   Ubuntu/Debian: sudo systemctl start mysql"
    echo "   CentOS/RHEL: sudo systemctl start mysqld"
    echo "   macOS: brew services start mysql"
    exit 1
fi

echo "✓ MySQL está rodando"

# Tentar conectar com as credenciais padrão
DB_USER="${DB_USER:-root}"
DB_PASSWORD="${DB_PASSWORD:-root}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-3306}"
DB_NAME="${DB_NAME:-carros}"

echo ""
echo "📊 Testando conexão com MySQL..."
echo "   Host: $DB_HOST:$DB_PORT"
echo "   User: $DB_USER"

# Testar conexão
if ! mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1;" &> /dev/null; then
    echo ""
    echo "❌ Não foi possível conectar ao MySQL com as credenciais fornecidas"
    echo ""
    echo "🔐 Verifique as credenciais:"
    echo "   Host: $DB_HOST"
    echo "   Porta: $DB_PORT"
    echo "   Usuário: $DB_USER"
    echo "   Senha: $DB_PASSWORD"
    echo ""
    echo "💡 Para configurar a senha do root:"
    echo "   sudo mysql"
    echo "   ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';"
    echo "   FLUSH PRIVILEGES;"
    echo "   exit"
    exit 1
fi

echo "✓ Conexão estabelecida com sucesso"

# Criar banco de dados se não existir
echo ""
echo "🗄️  Configurando banco de dados '$DB_NAME'..."

mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" << EOF
CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE $DB_NAME;

CREATE TABLE IF NOT EXISTS carros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    modelo VARCHAR(255) NOT NULL UNIQUE,
    preco DECIMAL(12, 2) NOT NULL,
    image VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_modelo (modelo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
EOF

if [ $? -eq 0 ]; then
    echo "✓ Banco de dados '$DB_NAME' configurado"
    
    # Verificar se há dados
    COUNT=$(mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" -N -s -e "USE $DB_NAME; SELECT COUNT(*) FROM carros;")
    echo "✓ Tabela 'carros' tem $COUNT registros"
else
    echo "❌ Erro ao configurar banco de dados"
    exit 1
fi

echo ""
echo "✅ Ambiente MySQL pronto para uso!"
echo ""
echo "🚀 Para iniciar a aplicação:"
echo "   ./start.sh"
echo ""
echo "📝 Ou para testar diretamente:"
echo "   python app.py"
