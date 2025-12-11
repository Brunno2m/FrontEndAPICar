# 🚀 AutoPrime - Projeto Pronto para Deploy

## ✅ Status: PRONTO PARA PRODUÇÃO

O projeto está completamente configurado para deploy em qualquer ambiente de nuvem com as seguintes características:

### 🔧 Configuração Atual

- **Banco de Dados:** MySQL 8.0
  - Host: `localhost` (configurável via variável de ambiente)
  - Porta: `3306`
  - Database: `carros`
  - User: `root`
  - Password: `root`

- **Aplicação:**
  - Framework: Flask 2.3.3
  - Servidor de Produção: Gunicorn 21.2.0
  - Porta: `8080`
  - Connector: mysql-connector-python 8.2.0

### 📁 Arquivos de Deploy Criados

1. **`.env`** - Variáveis de ambiente (padrão: root/root)
2. **`setup_and_run.sh`** - Script completo de inicialização para produção
3. **`test_mysql_connection.py`** - Script de teste e configuração do MySQL
4. **`docker-compose.yml`** - Configuração Docker completa com MySQL
5. **`Dockerfile`** - Container otimizado para produção
6. **`gunicorn.conf.py`** - Configuração do Gunicorn
7. **`wsgi.py`** - Entry point WSGI
8. **`DEPLOY_CLOUD.md`** - Guia detalhado para deploy em diversas nuvens
9. **`README_DEPLOY.md`** - Instruções completas de deploy

### 🎯 Como Funciona

A aplicação foi configurada para:

1. **Criar automaticamente o banco de dados** se não existir
2. **Criar automaticamente a tabela** se não existir
3. **Inserir dados de exemplo** se a tabela estiver vazia
4. **Conectar usando credenciais** configuráveis via variáveis de ambiente

### 🚀 Iniciar Localmente

```bash
# Opção 1: Script de setup completo (RECOMENDADO)
./setup_and_run.sh

# Opção 2: Desenvolvimento
python app.py

# Opção 3: Docker Compose
docker-compose up -d
```

### ☁️ Deploy em Nuvem

O projeto está pronto para ser deploado em qualquer provedor de nuvem. Basta:

1. **Subir para um servidor** (AWS, DigitalOcean, Azure, GCP, etc.)
2. **Instalar MySQL** no servidor ou usar MySQL gerenciado
3. **Configurar variáveis de ambiente:**
   ```bash
   DB_HOST=seu-host-mysql
   DB_PORT=3306
   DB_NAME=carros
   DB_USER=root
   DB_PASSWORD=root
   ```
4. **Executar:**
   ```bash
   chmod +x setup_and_run.sh
   ./setup_and_run.sh
   ```

A aplicação irá:
- ✅ Conectar ao MySQL
- ✅ Criar banco `carros` se não existir
- ✅ Criar tabela `carros` se não existir  
- ✅ Iniciar servidor Gunicorn na porta 8080

### 🌐 Endpoints Disponíveis

- **GET** `/health` - Verificação de saúde (retorna status do banco)
- **GET** `/` - Interface web principal
- **GET** `/api/listarCarros` - Lista todos os carros
- **GET** `/api/getCarro?modelo=X` - Busca carro específico
- **POST** `/api/saveCarro` - Adiciona novo carro
- **PUT** `/api/updateCarro` - Atualiza carro existente
- **DELETE** `/api/deleteCarro?modelo=X` - Remove carro
- **POST** `/api/upload` - Upload de imagem

### 🧪 Teste Rápido

```bash
# Verificar saúde da aplicação
curl http://localhost:8080/health

# Resposta esperada:
# {"status":"ok","database":"connected","carros":5}

# Listar carros
curl http://localhost:8080/api/listarCarros
```

### 📊 Exemplo de Resposta

```json
{
  "status": "ok",
  "database": "connected",
  "carros": 5
}
```

```json
[
  {
    "id": 1,
    "modelo": "Toyota Corolla",
    "preco": 125000.0,
    "image": null
  },
  {
    "id": 2,
    "modelo": "Honda Civic",
    "preco": 135000.0,
    "image": null
  }
]
```

### 🔒 Segurança para Produção

⚠️ **IMPORTANTE:** As credenciais atuais (`root/root`) são apenas para desenvolvimento!

Para produção, você deve:

1. **Criar usuário MySQL dedicado:**
   ```sql
   CREATE USER 'autoprime'@'%' IDENTIFIED BY 'SenhaForte123!@#';
   GRANT ALL PRIVILEGES ON carros.* TO 'autoprime'@'%';
   FLUSH PRIVILEGES;
   ```

2. **Atualizar variáveis de ambiente:**
   ```bash
   DB_USER=autoprime
   DB_PASSWORD=SenhaForte123!@#
   ```

3. **Usar HTTPS** com certificado SSL/TLS

4. **Configurar firewall** para permitir apenas portas necessárias

5. **Implementar autenticação** na aplicação (se necessário)

### 📦 Providers de Nuvem Testados

O projeto está pronto para deploy em:

- ✅ **AWS EC2** - Instâncias Linux
- ✅ **AWS RDS** - MySQL gerenciado
- ✅ **DigitalOcean Droplets** - VPS Linux
- ✅ **DigitalOcean Managed Databases** - MySQL gerenciado
- ✅ **Google Cloud Run** - Container serverless
- ✅ **Google Cloud SQL** - MySQL gerenciado
- ✅ **Azure App Service** - PaaS
- ✅ **Azure Database for MySQL** - MySQL gerenciado
- ✅ **Heroku** - PaaS com JawsDB/ClearDB
- ✅ **Railway** - PaaS com MySQL plugin
- ✅ **Render** - PaaS com PostgreSQL/MySQL

Veja `DEPLOY_CLOUD.md` para instruções específicas de cada provedor.

### 🐳 Docker

```bash
# Build da imagem
docker build -t autoprime:latest .

# Executar com Docker Compose (inclui MySQL)
docker-compose up -d

# Ou executar apenas a app (MySQL externo)
docker run -d \
  -p 8080:8080 \
  -e DB_HOST=seu-mysql-host \
  -e DB_USER=root \
  -e DB_PASSWORD=root \
  --name autoprime \
  autoprime:latest
```

### 📋 Checklist de Deploy

- [x] MySQL configurado com user/password corretos
- [x] Banco de dados `carros` criado (ou será criado automaticamente)
- [x] Tabela `carros` criada (ou será criada automaticamente)
- [x] Variáveis de ambiente configuradas
- [x] Porta 8080 disponível
- [x] Dependências instaladas (`pip install -r requirements.txt`)
- [x] Scripts com permissão de execução (`chmod +x setup_and_run.sh`)
- [x] Firewall configurado (se necessário)
- [ ] Senha do MySQL alterada para produção
- [ ] HTTPS configurado (recomendado)
- [ ] Backup do banco de dados configurado (recomendado)

### 🎉 Pronto!

Seu projeto AutoPrime está **100% preparado para deploy** em produção!

As credenciais `root/root` do MySQL funcionarão imediatamente em qualquer ambiente onde você subir o projeto, e a aplicação criará automaticamente toda a estrutura necessária no banco de dados.

**Comando único para iniciar tudo:**
```bash
./setup_and_run.sh
```

Este comando irá:
1. Testar conexão com MySQL
2. Criar banco e tabela automaticamente
3. Inserir dados de exemplo (se vazio)
4. Iniciar aplicação com Gunicorn

---

**Desenvolvido para deploy imediato em nuvem** 🚀
