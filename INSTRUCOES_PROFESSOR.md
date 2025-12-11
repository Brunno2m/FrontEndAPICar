# 🚀 Instruções para Deploy e Teste na AWS

## Professor, siga estes passos simples para testar o projeto:

---

## 📋 PRÉ-REQUISITOS

Você vai precisar de:
- ✅ Instância EC2 Ubuntu (ou qualquer Linux)
- ✅ MySQL instalado (ou RDS MySQL da AWS)
- ✅ Python 3.11 ou superior
- ✅ Porta 8080 liberada no Security Group

---

## 🎯 PASSO A PASSO RÁPIDO (5 minutos)

### 1️⃣ Extrair o arquivo ZIP
```bash
unzip FrontEndAPICar.zip
cd FrontEndAPICar
```

### 2️⃣ Instalar MySQL (se não tiver)
```bash
sudo apt-get update
sudo apt-get install -y mysql-server
sudo service mysql start
```

### 3️⃣ Configurar senha do MySQL
```bash
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root'; FLUSH PRIVILEGES;"
```

### 4️⃣ Instalar Python e dependências
```bash
sudo apt-get install -y python3 python3-pip python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 5️⃣ EXECUTAR O PROJETO (escolha uma opção)

**OPÇÃO A - Script Automático (RECOMENDADO):**
```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

**OPÇÃO B - Python Direto:**
```bash
python app.py
```

**OPÇÃO C - Docker (se tiver Docker instalado):**
```bash
docker-compose up -d
```

### 6️⃣ Testar a aplicação

Acesse no navegador:
```
http://IP-DA-INSTANCIA:8080
```

Ou teste via comando:
```bash
curl http://localhost:8080/health
```

**Resposta esperada:**
```json
{
  "status": "ok",
  "database": "connected",
  "carros": 5
}
```

---

## ⚙️ O QUE O SISTEMA FAZ AUTOMATICAMENTE

Ao executar `./setup_and_run.sh` ou `python app.py`, o sistema **AUTOMATICAMENTE**:

✅ Conecta ao MySQL (localhost:3306)
✅ Cria o banco de dados `carros` (se não existir)
✅ Cria a tabela `carros` com toda estrutura (se não existir)
✅ Insere 5 carros de exemplo (se a tabela estiver vazia)
✅ Inicia o servidor na porta 8080

**Não precisa criar NADA manualmente no banco de dados!**

---

## 🗄️ CREDENCIAIS DO BANCO DE DADOS

O projeto está configurado para usar:
- **Host:** localhost
- **Porta:** 3306
- **Banco:** carros
- **Usuário:** root
- **Senha:** root

Se quiser usar outras credenciais, edite o arquivo `.env`:
```bash
nano .env
```

E altere:
```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=carros
DB_USER=root
DB_PASSWORD=root
```

---

## 🧪 TESTES DA API REST

Depois que o servidor estiver rodando:

**1. Health Check:**
```bash
curl http://localhost:8080/health
```

**2. Listar todos os carros:**
```bash
curl http://localhost:8080/api/listarCarros
```

**3. Adicionar um carro:**
```bash
curl -X POST http://localhost:8080/api/saveCarro \
  -H "Content-Type: application/json" \
  -d '{"modelo": "Tesla Model 3", "preco": 250000}'
```

**4. Buscar carro específico:**
```bash
curl "http://localhost:8080/api/getCarro?modelo=Tesla%20Model%203"
```

**5. Atualizar preço:**
```bash
curl -X PUT http://localhost:8080/api/updateCarro \
  -H "Content-Type: application/json" \
  -d '{"modelo": "Tesla Model 3", "preco": 240000}'
```

**6. Deletar carro:**
```bash
curl -X DELETE "http://localhost:8080/api/deleteCarro?modelo=Tesla%20Model%203"
```

---

## 🌐 ACESSAR A INTERFACE WEB

Abra o navegador e acesse:
```
http://IP-DA-INSTANCIA-EC2:8080
```

Você verá a interface web com:
- Listagem de carros
- Formulário para adicionar/editar
- Upload de imagens
- Busca por modelo

---

## 🔥 CONFIGURAÇÃO DA AWS EC2

### Security Group (Firewall):
Libere as seguintes portas:
- **22** - SSH (para acessar o servidor)
- **8080** - Aplicação Flask
- **3306** - MySQL (se usar RDS externo)

### Usando RDS MySQL (opcional):
Se usar RDS ao invés de MySQL local, edite o arquivo `.env`:
```
DB_HOST=seu-rds-endpoint.rds.amazonaws.com
DB_PORT=3306
DB_NAME=carros
DB_USER=admin
DB_PASSWORD=sua-senha-rds
```

---

## ❓ TROUBLESHOOTING

### Erro: "Can't connect to MySQL server"
**Solução:**
```bash
sudo service mysql start
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root'; FLUSH PRIVILEGES;"
```

### Erro: "Port 8080 is already in use"
**Solução:**
```bash
sudo lsof -ti:8080 | xargs sudo kill -9
python app.py
```

### Erro: "ModuleNotFoundError"
**Solução:**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Ver logs de erro:
```bash
tail -f app.log
```

---

## 📊 ESTRUTURA DO BANCO DE DADOS

O sistema cria automaticamente:

**Banco:** `carros`

**Tabela:** `carros`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INT AUTO_INCREMENT | ID único |
| modelo | VARCHAR(255) UNIQUE | Modelo do carro |
| preco | DECIMAL(12,2) | Preço |
| image | VARCHAR(500) | URL da imagem |
| created_at | TIMESTAMP | Data de criação |
| updated_at | TIMESTAMP | Última atualização |

---

## ✅ CHECKLIST DE VALIDAÇÃO

Marque conforme testa:

- [ ] MySQL instalado e rodando
- [ ] Senha do root configurada como 'root'
- [ ] Dependências Python instaladas
- [ ] Aplicação iniciada sem erros
- [ ] Health check retorna {"status":"ok"}
- [ ] API /api/listarCarros retorna 5 carros
- [ ] Interface web carrega no navegador
- [ ] Consegue adicionar um novo carro
- [ ] Consegue buscar/editar/deletar carros
- [ ] Upload de imagem funciona

---

## 📱 CONTATO

Se tiver alguma dúvida ou problema, os arquivos de documentação completa estão em:
- `PRONTO_PARA_DEPLOY.md` - Visão geral
- `DEPLOY_CLOUD.md` - Deploy detalhado na AWS
- `README_DEPLOY.md` - Guia completo

---

## 🎓 INFORMAÇÕES TÉCNICAS

**Stack:**
- Backend: Flask 2.3.3 (Python)
- Banco de Dados: MySQL 8.0
- Servidor de Produção: Gunicorn
- API: REST com JSON
- Frontend: HTML5, CSS3, JavaScript

**Arquitetura:**
- MVC (Model-View-Controller)
- CRUD completo
- Persistência em MySQL
- Upload de arquivos
- Prepared Statements (proteção contra SQL Injection)

**Portas:**
- 8080 - Aplicação web e API REST
- 3306 - MySQL (se local)

---

## 🚀 RESUMO PARA TESTE RÁPIDO

Se quiser testar o mais rápido possível:

```bash
# 1. Instalar MySQL
sudo apt-get update && sudo apt-get install -y mysql-server python3-venv
sudo service mysql start
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root'; FLUSH PRIVILEGES;"

# 2. Extrair projeto
unzip FrontEndAPICar.zip && cd FrontEndAPICar

# 3. Instalar dependências
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

# 4. Executar
chmod +x setup_and_run.sh && ./setup_and_run.sh
```

**Acesse:** http://IP-EC2:8080

**Pronto!** 🎉

---

**Nota:** O sistema foi desenvolvido para funcionar "out of the box". 
Basta ter MySQL rodando com as credenciais root/root e executar!
