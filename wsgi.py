"""
WSGI entry point para servidores de produção como Gunicorn
"""
from app import app

if __name__ == "__main__":
    app.run()
