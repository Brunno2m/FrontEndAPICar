# Configurações para Deploy em Produção

## Variáveis de Ambiente

Configure estas variáveis de ambiente antes de fazer deploy:

### Banco de Dados MySQL
```bash
DB_HOST=localhost          # Host do MySQL (padrão: localhost)
DB_PORT=3306              # Porta do MySQL (padrão: 3306)
DB_NAME=carros            # Nome do banco de dados (padrão: carros)
DB_USER=root              # Usuário do MySQL (padrão: root)
DB_PASSWORD=root          # Senha do MySQL (padrão: root)
```

### Aplicação
```bash
PORT=8080                 # Porta da aplicação (padrão: 8080)
FLASK_ENV=production      # Ambiente Flask
```

## Deploy em Nuvem

### AWS EC2 / DigitalOcean / Linode

1. **Instalar dependências do sistema:**
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv mysql-server git
```

2. **Configurar MySQL:**
```bash
sudo service mysql start
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';"
sudo mysql -e "CREATE DATABASE carros CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

3. **Clonar repositório e configurar:**
```bash
git clone https://github.com/seu-usuario/FrontEndAPICar.git
cd FrontEndAPICar
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. **Configurar variáveis de ambiente:**
```bash
# Editar .env com suas configurações
nano .env
```

5. **Iniciar aplicação:**
```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

### Heroku

1. **Criar Procfile:**
```
web: gunicorn -c gunicorn.conf.py app:app
```

2. **Adicionar add-on MySQL:**
```bash
heroku addons:create jawsdb:kitefin
```

3. **Configurar variáveis de ambiente:**
```bash
# Heroku configura automaticamente JAWSDB_URL
# Adicione outras variáveis se necessário
heroku config:set FLASK_ENV=production
```

4. **Deploy:**
```bash
git push heroku main
```

### Google Cloud Run

1. **Criar Dockerfile (já existe no projeto)**

2. **Build e deploy:**
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/autoprime
gcloud run deploy autoprime --image gcr.io/PROJECT-ID/autoprime \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DB_HOST=MYSQL_HOST,DB_PORT=3306,DB_NAME=carros,DB_USER=root,DB_PASSWORD=root
```

### Azure App Service

1. **Criar App Service e MySQL:**
```bash
az mysql server create --resource-group myResourceGroup \
  --name autoprime-mysql --location eastus \
  --admin-user root --admin-password root \
  --sku-name B_Gen5_1

az mysql db create --resource-group myResourceGroup \
  --server-name autoprime-mysql --name carros
```

2. **Deploy da aplicação:**
```bash
az webapp up --runtime PYTHON:3.11 --name autoprime-app
```

3. **Configurar variáveis:**
```bash
az webapp config appsettings set --name autoprime-app \
  --settings DB_HOST=autoprime-mysql.mysql.database.azure.com \
  DB_PORT=3306 DB_NAME=carros DB_USER=root DB_PASSWORD=root
```

### Railway

1. **Adicionar arquivo railway.json:**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "./setup_and_run.sh",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

2. **Adicionar MySQL plugin no Railway dashboard**

3. **Configurar variáveis de ambiente automaticamente vinculadas**

### Render

1. **Criar render.yaml:**
```yaml
services:
  - type: web
    name: autoprime
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: ./setup_and_run.sh
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DB_HOST
        fromDatabase:
          name: autoprime-db
          property: host
      - key: DB_PORT
        fromDatabase:
          name: autoprime-db
          property: port
      - key: DB_USER
        fromDatabase:
          name: autoprime-db
          property: user
      - key: DB_PASSWORD
        fromDatabase:
          name: autoprime-db
          property: password
      - key: DB_NAME
        value: carros

databases:
  - name: autoprime-db
    databaseName: carros
    user: root
```

## Deploy Docker

### Build da imagem:
```bash
docker build -t autoprime:latest .
```

### Executar com Docker Compose:
```bash
docker-compose up -d
```

### Ou executar manualmente:
```bash
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

## Systemd Service (Linux)

Criar `/etc/systemd/system/autoprime.service`:

```ini
[Unit]
Description=AutoPrime Flask Application
After=network.target mysql.service
Requires=mysql.service

[Service]
Type=notify
User=www-data
WorkingDirectory=/opt/autoprime
Environment="PATH=/opt/autoprime/.venv/bin"
EnvironmentFile=/opt/autoprime/.env
ExecStart=/opt/autoprime/setup_and_run.sh
Restart=always
RestartSec=10

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

## Verificação Pós-Deploy

### Health Check:
```bash
curl http://seu-dominio:8080/health
```

Resposta esperada:
```json
{
  "status": "ok",
  "database": "connected",
  "carros": 0
}
```

### Testar API:
```bash
# Listar carros
curl http://seu-dominio:8080/api/listarCarros

# Adicionar carro
curl -X POST http://seu-dominio:8080/api/saveCarro \
  -H "Content-Type: application/json" \
  -d '{"modelo": "Tesla Model 3", "preco": 250000}'
```

## Logs e Monitoramento

### Ver logs em tempo real:
```bash
tail -f /var/log/autoprime/app.log
```

### Com systemd:
```bash
journalctl -u autoprime -f
```

### Com Docker:
```bash
docker logs -f autoprime
```

## Troubleshooting

### Erro de conexão com MySQL:
```bash
# Verificar se MySQL está rodando
sudo service mysql status

# Testar conexão manualmente
mysql -h localhost -u root -proot -e "SHOW DATABASES;"

# Verificar se o banco existe
mysql -h localhost -u root -proot -e "USE carros; SHOW TABLES;"
```

### Aplicação não inicia:
```bash
# Verificar logs
tail -50 /var/log/autoprime/error.log

# Testar configuração Python
python3 test_mysql_connection.py

# Verificar variáveis de ambiente
env | grep DB_
```

## Segurança em Produção

⚠️ **IMPORTANTE:** Em produção, **NÃO use root/root**!

1. **Criar usuário MySQL dedicado:**
```sql
CREATE USER 'autoprime'@'%' IDENTIFIED BY 'senha_forte_aqui';
GRANT ALL PRIVILEGES ON carros.* TO 'autoprime'@'%';
FLUSH PRIVILEGES;
```

2. **Atualizar .env:**
```bash
DB_USER=autoprime
DB_PASSWORD=senha_forte_aqui
```

3. **Configurar HTTPS com certificado SSL**

4. **Implementar rate limiting e autenticação**

5. **Fazer backup regular do banco de dados:**
```bash
mysqldump -u root -p carros > backup_$(date +%Y%m%d).sql
```
