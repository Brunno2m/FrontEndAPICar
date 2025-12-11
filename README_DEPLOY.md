# AutoPrime - Guia de Deploy

## 📋 Pré-requisitos

1. **MySQL Server 8.0+** instalado e rodando
2. **Python 3.11+** instalado
3. Usuário MySQL com as seguintes credenciais:
   - Host: `localhost`
   - Porta: `3306`
   - Banco: `carros`
   - Usuário: `root`
   - Senha: `root`

## 🔧 Configuração do Banco de Dados

### Opção 1: Via MySQL CLI
```bash
mysql -u root -p < setup_database.sql
```

### Opção 2: Via MySQL Workbench
1. Abra o MySQL Workbench
2. Conecte-se ao servidor MySQL
3. Abra o arquivo `setup_database.sql`
4. Execute o script completo

### Opção 3: Criação Manual
```sql
CREATE DATABASE carros CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE carros;

CREATE TABLE carros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    modelo VARCHAR(255) NOT NULL UNIQUE,
    preco DECIMAL(12, 2) NOT NULL,
    image VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 🚀 Deploy - Opção 1: Servidor Python

### Instalação
```bash
# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### Execução com Gunicorn (Produção)
```bash
# Dar permissão de execução ao script
chmod +x start.sh

# Iniciar aplicação
./start.sh
```

### Execução Direta (Desenvolvimento)
```bash
python app.py
```

### Configuração de Variáveis de Ambiente
Edite o arquivo `.env` se necessário:
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=carros
DB_USER=root
DB_PASSWORD=root
PORT=8080
FLASK_ENV=production
```

## 📦 Deploy - Opção 2: Executável Standalone

### Criar Executável
```bash
# Instalar PyInstaller
pip install pyinstaller

# Criar executável
python build_executable.py
```

O executável será criado em: `dist/AutoPrime`

### Executar
```bash
./dist/AutoPrime
```

**Observação:** O executável deve estar na mesma pasta onde estão as pastas `templates/` e `static/`

## 🐳 Deploy - Opção 3: Docker

### Atualizar Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicação
COPY . .

# Criar diretório de uploads
RUN mkdir -p static/uploads

# Expor porta
EXPOSE 8080

# Comando de inicialização
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
```

### Build e Execução
```bash
# Build da imagem
docker build -t autoprime:latest .

# Executar container
docker run -d \
  -p 8080:8080 \
  -e DB_HOST=host.docker.internal \
  -e DB_PORT=3306 \
  -e DB_NAME=carros \
  -e DB_USER=root \
  -e DB_PASSWORD=root \
  --name autoprime \
  autoprime:latest
```

**Nota:** Use `host.docker.internal` no Docker Desktop (Windows/Mac) para acessar o MySQL do host.

## 🔍 Verificação

### Health Check
```bash
curl http://localhost:8080/health
```

Resposta esperada:
```json
{
  "status": "ok",
  "database": "connected",
  "carros": 5
}
```

### Testar API
```bash
# Listar carros
curl http://localhost:8080/api/listarCarros

# Adicionar carro
curl -X POST http://localhost:8080/api/saveCarro \
  -H "Content-Type: application/json" \
  -d '{"modelo": "Tesla Model 3", "preco": 250000}'

# Buscar carro
curl http://localhost:8080/api/getCarro?modelo=Tesla%20Model%203

# Atualizar preço
curl -X PUT http://localhost:8080/api/updateCarro \
  -H "Content-Type: application/json" \
  -d '{"modelo": "Tesla Model 3", "preco": 245000}'

# Deletar carro
curl -X DELETE http://localhost:8080/api/deleteCarro?modelo=Tesla%20Model%203
```

## 🌐 Acesso à Aplicação

Após iniciar, acesse:
- **Interface Web:** http://localhost:8080
- **API:** http://localhost:8080/api/*
- **Health:** http://localhost:8080/health

## ⚙️ Configuração de Produção

### Nginx como Proxy Reverso (Opcional)
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /caminho/para/autoprime/static/;
    }
}
```

### Systemd Service (Linux)
Crie `/etc/systemd/system/autoprime.service`:
```ini
[Unit]
Description=AutoPrime Flask Application
After=network.target mysql.service

[Service]
Type=notify
User=www-data
WorkingDirectory=/caminho/para/autoprime
Environment="PATH=/caminho/para/autoprime/.venv/bin"
ExecStart=/caminho/para/autoprime/.venv/bin/gunicorn -c gunicorn.conf.py app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Ativar:
```bash
sudo systemctl daemon-reload
sudo systemctl enable autoprime
sudo systemctl start autoprime
sudo systemctl status autoprime
```

## 🛠️ Troubleshooting

### Erro de conexão com MySQL
```
✗ Erro ao conectar ao MySQL: Can't connect to MySQL server
```
**Solução:**
- Verificar se MySQL está rodando: `sudo systemctl status mysql`
- Verificar credenciais no arquivo `.env`
- Verificar firewall: `sudo ufw allow 3306`

### Erro de permissão no diretório uploads
```
PermissionError: [Errno 13] Permission denied: 'static/uploads'
```
**Solução:**
```bash
mkdir -p static/uploads
chmod 755 static/uploads
```

### Tabela não existe
```
mysql.connector.errors.ProgrammingError: Table 'carros.carros' doesn't exist
```
**Solução:**
- Executar `setup_database.sql`
- Ou iniciar a aplicação (ela cria automaticamente)

## 📊 Monitoramento

### Logs
```bash
# Logs do Gunicorn (stdout/stderr)
journalctl -u autoprime -f

# Logs do MySQL
tail -f /var/log/mysql/error.log
```

### Métricas
- Número de carros: `curl -s http://localhost:8080/health | jq .carros`
- Status do banco: `curl -s http://localhost:8080/health | jq .database`

## 🔒 Segurança

✅ Implementado:
- CORS configurado
- SQL Injection protegido (prepared statements)
- Validação de extensões de arquivo

⚠️ Recomendações adicionais:
1. Mudar senha do MySQL de 'root'
2. Criar usuário específico para a aplicação
3. Configurar SSL/TLS (HTTPS)
4. Implementar rate limiting
5. Adicionar autenticação/autorização
6. Backup regular do banco de dados

## 📝 Notas

- O banco de dados é criado automaticamente na primeira execução
- Imagens são armazenadas em `static/uploads/`
- A aplicação usa Gunicorn com workers múltiplos para melhor performance
- Certifique-se de que a porta 8080 está disponível
