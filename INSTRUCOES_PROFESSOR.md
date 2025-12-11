# 🚀 Instruções Simples - Deploy na AWS

## Professor, siga estes 4 passos:

---

## 📋 O QUE VOCÊ PRECISA

- Instância EC2 com Ubuntu (qualquer tamanho)
- Porta **8080** liberada no Security Group da EC2
- Acesso SSH à instância

---

## 🎯 PASSO A PASSO (copie e cole os comandos)

### 1️⃣ Envie o arquivo ZIP para a EC2 (do seu Windows)

**Abra o PowerShell onde está o arquivo ZIP e execute:**
```powershell
scp -i sua-chave.pem FrontEndAPICar.zip ubuntu@IP-DA-EC2:~
```

**Substitua:**
- `sua-chave.pem` → pela chave que você baixou da AWS (ex: `autoprime-key.pem`)
- `IP-DA-EC2` → pelo IP público da sua instância EC2

**Exemplo real:**
```powershell
scp -i C:\Users\Professor\autoprime-key.pem FrontEndAPICar.zip ubuntu@18.232.145.67:~
```

### 2️⃣ Conecte na EC2 via SSH

**No PowerShell:**
```bash
ssh -i sua-chave.pem ubuntu@IP-DA-EC2
```

**Exemplo real:**
```bash
ssh -i C:\Users\Professor\autoprime-key.pem ubuntu@18.232.145.67
```

### 3️⃣ Na EC2, execute este comando único

**Cole este comando completo no terminal da EC2:**
```bash
sudo apt-get update && sudo apt-get install -y mysql-server python3-venv unzip && \
sudo service mysql start && \
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root'; FLUSH PRIVILEGES;" && \
unzip FrontEndAPICar.zip && cd FrontEndAPICar && \
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && \
chmod +x setup_and_run.sh && ./setup_and_run.sh
```

**Isso vai:**
- ✅ Instalar MySQL e Python
- ✅ Configurar senha do MySQL (root/root)
- ✅ Extrair o projeto
- ✅ Instalar dependências
- ✅ Criar banco de dados e tabela automaticamente
- ✅ Inserir 5 carros de exemplo
- ✅ Iniciar servidor na porta 8080

### 4️⃣ Teste no seu navegador Windows

Abra o navegador e acesse:
```
http://IP-DA-SUA-EC2:8080
```

**Ou teste via PowerShell:**
```powershell
curl http://IP-DA-SUA-EC2:8080/health
```

---

## ⚠️ IMPORTANTE - Security Group da EC2

No console da AWS, libere a porta **8080**:
1. Vá em EC2 → Security Groups
2. Edite as regras de entrada (Inbound Rules)
3. Adicione: **Custom TCP | Port 8080 | Source 0.0.0.0/0**

---

## 🎯 CREDENCIAIS DO BANCO

- **Host:** localhost
- **Usuário:** root
- **Senha:** root
- **Banco:** carros (criado automaticamente)

---

## ✅ RESULTADO ESPERADO

**No navegador você verá:**
- Interface web moderna
- 5 carros já cadastrados
- Formulário para adicionar/editar carros
- Upload de imagens
- Busca por modelo

**Endpoints da API:**
- `http://IP-EC2:8080/health` → Status do sistema
- `http://IP-EC2:8080/api/listarCarros` → Lista todos os carros
- `http://IP-EC2:8080/` → Interface web completa

---

## 🚨 SE DER ALGUM ERRO

### Erro de conexão MySQL:
```bash
sudo service mysql restart
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root'; FLUSH PRIVILEGES;"
cd FrontEndAPICar
source .venv/bin/activate
python app.py
```

### Porta 8080 ocupada:
```bash
sudo lsof -ti:8080 | xargs sudo kill -9
cd FrontEndAPICar
source .venv/bin/activate
python app.py
```

### Ver o que está acontecendo:
```bash
cd FrontEndAPICar
tail -f app.log
```

---

## 📝 RESUMO ULTRA RÁPIDO

1. **Envie o ZIP:** `scp -i chave.pem FrontEndAPICar.zip ubuntu@IP-EC2:~`
2. **SSH na EC2:** `ssh -i chave.pem ubuntu@IP-EC2`
3. **Execute:** Cole o comando único do passo 3
4. **Acesse:** `http://IP-EC2:8080`
5. **Pronto!** ✅

**O sistema configura tudo automaticamente. Não precisa criar banco ou tabelas manualmente!**
