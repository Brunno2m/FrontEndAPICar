# 🚗 Backend AutoPrime - Sistema de Loja de Veículos

Backend modernizado para gerenciamento de carros com API REST.

## 🚀 Início Rápido (3 passos)

### 1. Instalar
```bash
pip install -r requirements.txt
```

### 2. Executar
```bash
python app.py
```

### 3. Testar
Abra o navegador em: **http://localhost:8080**

## 📡 API - Endpoints Principais

| Endpoint | Método | Descrição | Exemplo |
|----------|--------|-----------|---------|
| `/getCarro` | POST | Busca por modelo | `{"modelo":"Ferrari"}` |
| `/saveCarro` | POST | Salva novo carro | `{"modelo":"Ferrari","preco":1200000}` |
| `/updateCarro` | POST | Atualiza preço | `{"modelo":"Ferrari","preco":1350000}` |
| `/deleteCarro` | POST | Remove carro | `{"modelo":"Ferrari"}` |
| `/listarCarros` | GET | Lista todos | - |
| `/teste` | GET | Status | - |

## 💡 Exemplos Rápidos

### Salvar um carro
```bash
curl -X POST http://localhost:8080/saveCarro \
  -H "Content-Type: application/json" \
  -d '{"modelo":"Ferrari","preco":1200000}'
```

### Listar todos
```bash
curl http://localhost:8080/listarCarros
```

### Buscar específico
```bash
curl -X POST http://localhost:8080/getCarro \
  -H "Content-Type: application/json" \
  -d '{"modelo":"Ferrari"}'
```

## 🧪 Executar Testes

```bash
python test_backend.py
```

Resultado: ✅ 14 testes automatizados

## 📁 Estrutura Simples

```
app.py              → Backend principal (código limpo)
carros.json         → Banco de dados JSON
requirements.txt    → Dependências (Flask, CORS)
templates/          → Interface web
test_backend.py     → Testes automatizados
```

## 🔧 Tecnologias

- Python 3.8+
- Flask (framework web)
- JSON (persistência)

## ⚙️ Como Funciona

1. O backend carrega os dados de `carros.json`
2. Expõe API REST na porta 8080
3. Toda alteração é salva automaticamente no arquivo
4. Interface web em `/` para testar visualmente

## 🐳 Docker (Opcional)

```bash
docker build -t autoprime .
docker run -p 8080:8080 autoprime
```

## 📝 Requisitos

Apenas 3 dependências:
```
Flask==2.3.3
flask-cors==3.0.10
requests==2.31.0
```

## ✅ Checklist

- [x] 6 endpoints funcionando
- [x] Persistência em JSON
- [x] Frontend integrado
- [x] Testes automatizados
- [x] Código limpo e simples
- [x] Documentação clara

## 🎯 Pronto para Produção

O código está otimizado e pronto para:
- Deploy local
- Deploy na nuvem (AWS, Azure, etc)
- Containerização Docker
- Integração com outros sistemas

---

**Porta:** 8080  
**Status:** ✅ Funcionando
