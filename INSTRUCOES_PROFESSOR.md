# 🚀 Instruções para Windows - Executar Localmente

## Professor, execute o projeto direto no seu Windows:

---

## 📋 PRÉ-REQUISITOS (instale antes)

1. **Python 3.11+** → https://www.python.org/downloads/
   - ✅ Marque "Add Python to PATH" na instalação

2. **MySQL 8.0** → https://dev.mysql.com/downloads/installer/
   - ✅ Durante instalação, configure: User=root, Password=root

---

## 🎯 PASSO A PASSO

### 1️⃣ Extraia o ZIP

Clique com botão direito no `FrontEndAPICar.zip` → **Extrair Tudo**

### 2️⃣ Abra o PowerShell na pasta do projeto

Navegue até a pasta extraída e abra o PowerShell:
- Clique com **Shift + Botão Direito** na pasta → **Abrir janela do PowerShell aqui**

Ou digite no PowerShell:
```powershell
cd C:\Users\SeuUsuario\Downloads\FrontEndAPICar
```

### 3️⃣ Execute estes comandos no PowerShell

**Instalar dependências:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Iniciar o servidor:**
```powershell
python app.py
```

### 4️⃣ Acesse no navegador

Abra o navegador e acesse:
```
http://localhost:8080
```

**Pronto! ✅**

---

## 🔄 Para executar novamente depois

```powershell
cd C:\Users\SeuUsuario\Downloads\FrontEndAPICar
.\.venv\Scripts\Activate.ps1
python app.py
```

---

## ⚠️ SE DER ERRO "execution of scripts is disabled"

Execute este comando uma vez (como Administrador):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois tente novamente ativar o ambiente:
```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 🗄️ CONFIGURAÇÃO DO MYSQL

**Credenciais (devem estar configuradas):**
- Host: localhost
- Porta: 3306
- Usuário: root
- Senha: root

**O sistema cria automaticamente:**
- ✅ Banco de dados `carros`
- ✅ Tabela `carros` com estrutura completa
- ✅ Insere 5 carros de exemplo

---

## ✅ O QUE VOCÊ VAI VER

**No navegador (http://localhost:8080):**
- Interface web moderna
- 5 carros já cadastrados
- Formulários para adicionar/editar
- Upload de imagens
- Busca por modelo

**Endpoints da API:**
- `http://localhost:8080/health` → Status do sistema
- `http://localhost:8080/api/listarCarros` → Lista todos os carros
- `http://localhost:8080/` → Interface web completa

---

## 🚨 PROBLEMAS COMUNS

### MySQL não está rodando
**Solução:**
- Abra "Serviços" do Windows (Win + R → `services.msc`)
- Procure "MySQL80" → Botão direito → Iniciar

### Porta 8080 ocupada
**Solução no PowerShell:**
```powershell
netstat -ano | findstr :8080
taskkill /PID <numero_do_pid> /F
python app.py
```

### Python não reconhecido
**Solução:**
- Reinstale Python marcando "Add Python to PATH"
- Ou use: `py app.py` ao invés de `python app.py`

### Erro ao ativar .venv
**Solução (PowerShell como Admin):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📝 RESUMO RÁPIDO

```powershell
# 1. Abrir PowerShell na pasta do projeto
cd C:\caminho\para\FrontEndAPICar

# 2. Criar ambiente virtual e instalar
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Executar
python app.py

# 4. Acessar
# http://localhost:8080
```

**Tudo funciona automaticamente! MySQL já deve estar rodando no Windows.**
