# FrontEndAPICar

Projeto de front-end + API proxy para uma "Loja de Carros".

Este repositório contém um servidor Flask que atua como proxy/adapter para um backend remoto (http://18.231.156.122:8080) e também fornece uma UI simples em HTML/CSS/JS para gerenciamento de carros (listar, buscar, salvar, atualizar, deletar).

## Estrutura principal

- `app.py` - servidor Flask com endpoints em `/api/*` e fallback em memória (`CARROS`) para operações de escrita.
- `templates/index.html` - front-end principal (Jinja) servido pelo Flask.
- `static/css/styles.css` - estilos e layout.
- `static/js/scripts.js` - lógica do cliente (fetch para `/api/*`, toggle de listagem, spinner, toasts).
- `test_api_ops.py` - script de teste rápido que executa uma sequência de requisições à API local.
- `requirements.txt` - dependências Python (Flask, requests, flask-cors).

## Pré-requisitos

- Python 3.8+ (recomendado 3.10+)
- Windows (instruções abaixo usam PowerShell)

## Setup (Windows PowerShell)

1. Criar e ativar venv:

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

2. Instalar dependências:

```powershell
pip install -r requirements.txt
```

3. Rodar a aplicação Flask:

```powershell
.\.venv\Scripts\python.exe -u app.py
```

A aplicação irá rodar em http://127.0.0.1:3000 por padrão.

## Endpoints principais (expostos pela proxy local)

- `GET /` - página principal (UI)
- `GET /api/listarCarros` - retorna o array atual `CARROS` (in-memory, seed do remoto se disponível)
- `POST /api/getCarro` - busca carro por `modelo` (JSON body: `{ "modelo": "..." }`) — devolve itens que batem localmente ou faz fallback ao backend remoto
- `POST /api/saveCarro` - salva um carro localmente (JSON: `{ "modelo": "...", "preco": 12345 }`)
- `POST /api/updateCarro` - atualiza o preço de um `modelo` localmente (JSON: `{ "modelo": "...", "preco": 54321 }`)
- `POST /api/deleteCarro` - deleta carro(s) por `modelo` (JSON: `{ "modelo": "..." }`)
- `GET /health` - retorna status simples `{ "status": "ok" }`
- `GET /debug/backend_status` - tenta consultar o backend remoto e reporta status

> Observação: o backend remoto original permite apenas operações de leitura (listar). Para tornar a UI funcional mesmo quando o remoto bloqueia verbos de escrita, o app utiliza um armazenamento em memória (`CARROS`) para salvar/atualizar/deletar localmente.

## Como usar a UI

1. Abra o navegador em http://127.0.0.1:3000
2. Clique em "Listar Carros" para carregar a lista (botão alterna para "Ocultar Lista")
3. Use os formulários à direita para adicionar, atualizar ou remover carros. A lista é atualizada automaticamente.

## Testes rápidos

Executar o script de integração:

```powershell
.\.venv\Scripts\python.exe test_api_ops.py
```

Ele executa: listar -> salvar TEST-XYZ -> listar -> atualizar TEST-XYZ -> deletar TEST-XYZ -> listar.

## Próximos passos sugeridos

- Persistir `CARROS` em arquivo JSON para sobreviver reinícios.
- Adicionar validação de entrada mais robusta e tratamento de erros no front.
- Melhorar UX (confirmação no delete, paginação na listagem, filtros).

## Time / Integrantes

- Brunno de Melo Marques
- Emanuel Correia Tavares
- Maria Clara Nunes Linhaes
- Paulo Ricardo Estevam Batalha
