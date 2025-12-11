"""
Script para criar executável standalone da aplicação AutoPrime
Usa PyInstaller para empacotar a aplicação Flask
"""

import os
import sys
import subprocess

def main():
    print("🔨 Construindo executável AutoPrime...")
    
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
    except ImportError:
        print("📦 Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Comando do PyInstaller
    cmd = [
        'pyinstaller',
        '--onefile',                    # Criar um único arquivo executável
        '--name=AutoPrime',             # Nome do executável
        '--add-data=templates:templates',  # Incluir pasta templates
        '--add-data=static:static',     # Incluir pasta static
        '--hidden-import=mysql.connector',
        '--hidden-import=flask',
        '--hidden-import=flask_cors',
        '--hidden-import=werkzeug',
        '--clean',                      # Limpar cache
        '--noconfirm',                  # Sobrescrever sem perguntar
        'app.py'
    ]
    
    print(f"📦 Executando: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("\n✅ Executável criado com sucesso!")
        print("📁 Localização: dist/AutoPrime")
        print("\n📝 Para executar:")
        print("   ./dist/AutoPrime")
        print("\n⚙️  Certifique-se de que:")
        print("   1. MySQL está rodando em localhost:3306")
        print("   2. Banco de dados 'carros' existe")
        print("   3. Usuário 'root' tem acesso com senha 'root'")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao criar executável: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
