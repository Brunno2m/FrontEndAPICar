# 🚀 Instruções Ultra Simples - EC2 já está rodando

## Professor, a EC2 já está configurada. Siga apenas 2 passos:

---

## 🎯 PASSO A PASSO

### 1️⃣ Extraia o ZIP na EC2

**Cole este comando único (ajuste o caminho do ZIP):**
```bash
cd ~ && \
unzip FrontEndAPICar.zip && \
cd FrontEndAPICar && \
python3 -m venv .venv && \
source .venv/bin/activate && \
pip install -r requirements.txt && \
chmod +x setup_and_run.sh && \
./setup_and_run.sh
```

**Se precisar instalar MySQL antes:**
```bash
sudo apt-get update && sudo apt-get install -y mysql-server python3-venv unzip && \
sudo service mysql start && \
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root'; FLUSH PRIVILEGES;"
```

### 2️⃣ Acesse no navegador

Abra o navegador no seu Windows e acesse:
```
http://IP-DA-SUA-EC2:8080
```

**Pronto! ✅**

---

## 🔄 Para executar novamente depois

Se precisar rodar o projeto novamente (depois de parar):

```bash
cd ~/FrontEndAPICar
source .venv/bin/activate
python app.py
```

**Ou com o script:**
```bash
cd ~/FrontEndAPICar
./setup_and_run.sh
```

---

## ⚠️ IMPORTANTE

**Porta 8080 deve estar liberada no Security Group da EC2**

**Credenciais do MySQL:**
- Usuário: root
- Senha: root
- Banco: carros (criado automaticamente)

---

## ✅ O QUE VOCÊ VAI VER

**No navegador:**
- Interface web moderna
- 5 carros já cadastrados
- Formulários funcionando
- Upload de imagens

**Endpoints:**
- `http://IP-EC2:8080` → Interface web
- `http://IP-EC2:8080/health` → Status do sistema
- `http://IP-EC2:8080/api/listarCarros` → Lista carros (API)

---

## 🚨 SE DER ERRO

**Erro de MySQL:**
```bash
sudo service mysql start
```

**Porta ocupada:**
```bash
sudo lsof -ti:8080 | xargs sudo kill -9
cd ~/FrontEndAPICar && source .venv/bin/activate && python app.py
```

**Ver logs:**
```bash
cd ~/FrontEndAPICar && tail -f app.log
```
