# Dockerfile para Backend AutoPrime
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para uploads
RUN mkdir -p static/uploads

# Expor porta 8080
EXPOSE 8080

# Definir variável de ambiente
ENV PORT=8080

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
