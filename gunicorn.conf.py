"""Configuração do Gunicorn para produção"""
import os
import multiprocessing

# Endereço e porta
bind = f"0.0.0.0:{os.environ.get('PORT', 8080)}"

# Número de workers (2-4 x número de CPU cores)
workers = multiprocessing.cpu_count() * 2 + 1

# Tipo de worker
worker_class = 'sync'

# Timeout para requisições (em segundos)
timeout = 120

# Timeout para workers inativos
graceful_timeout = 30

# Manter conexões ativas
keepalive = 5

# Log
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Preload da aplicação
preload_app = True

# Nome do processo
proc_name = 'autoprime'

# Número máximo de requisições por worker antes de reiniciar
max_requests = 1000
max_requests_jitter = 50
