# Dockerfile para Backend AutoPrime
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias para MySQL
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para uploads
RUN mkdir -p static/uploads

# Tornar scripts executáveis
RUN chmod +x setup_and_run.sh test_mysql_connection.py

# Expor porta 8080
EXPOSE 8080

# Definir variáveis de ambiente padrão
ENV PORT=8080
ENV DB_HOST=localhost
ENV DB_PORT=3306
ENV DB_NAME=carros
ENV DB_USER=root
ENV DB_PASSWORD=root
ENV FLASK_ENV=production

# Comando para iniciar a aplicação com Gunicorn
CMD ["./setup_and_run.sh"]
