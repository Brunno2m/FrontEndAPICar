# Autenticação e execução

Esta aplicação tem uma página de login simples para controlar o acesso à UI principal.

Usuário padrão: `admin`
Senha padrão: `secret`

Você pode sobrescrever essas credenciais com variáveis de ambiente antes de iniciar o app:

```bash
export AUTH_USER=meuusuario
export AUTH_PASS=minhasenha
export SECRET_KEY=uma-chave-secreta
export PORT=3000
```

No navegador, abra `http://127.0.0.1:3000` e você será redirecionado para `/login` se não estiver autenticado.

## Rodando em Linux / macOS (exemplo)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export AUTH_USER=admin
export AUTH_PASS=secret
export SECRET_KEY=dev-secret-change-me
python3 app.py
```
