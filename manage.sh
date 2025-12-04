#!/bin/bash

# Script de Gerenciamento - Backend AutoPrime
# Autor: Sistema AutoPrime
# Descrição: Script para facilitar operações comuns

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções de utilidade
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_header() {
    echo ""
    echo "═══════════════════════════════════════════════════════"
    echo -e "  ${BLUE}$1${NC}"
    echo "═══════════════════════════════════════════════════════"
    echo ""
}

# Verificar se Python está instalado
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 não encontrado. Por favor, instale o Python 3.8+"
        exit 1
    fi
    print_success "Python $(python3 --version) encontrado"
}

# Instalar dependências
install_deps() {
    print_header "INSTALANDO DEPENDÊNCIAS"
    check_python
    
    if [ -f "requirements.txt" ]; then
        print_info "Instalando pacotes do requirements.txt..."
        pip3 install -r requirements.txt
        print_success "Dependências instaladas com sucesso"
    else
        print_error "Arquivo requirements.txt não encontrado"
        exit 1
    fi
}

# Iniciar servidor
start_server() {
    print_header "INICIANDO SERVIDOR"
    check_python
    
    # Verificar se a porta 8080 está em uso
    if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        print_warning "Porta 8080 já está em uso"
        read -p "Deseja parar o processo existente? (s/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Ss]$ ]]; then
            stop_server
        else
            exit 1
        fi
    fi
    
    print_info "Iniciando servidor na porta 8080..."
    python3 app.py
}

# Iniciar servidor em background
start_background() {
    print_header "INICIANDO SERVIDOR EM BACKGROUND"
    
    if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        print_warning "Servidor já está rodando na porta 8080"
        exit 0
    fi
    
    print_info "Iniciando servidor em background..."
    nohup python3 app.py > autoprime.log 2>&1 &
    echo $! > autoprime.pid
    sleep 2
    
    if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        print_success "Servidor iniciado com sucesso (PID: $(cat autoprime.pid))"
        print_info "Logs em: autoprime.log"
    else
        print_error "Falha ao iniciar servidor"
        exit 1
    fi
}

# Parar servidor
stop_server() {
    print_header "PARANDO SERVIDOR"
    
    if [ -f "autoprime.pid" ]; then
        PID=$(cat autoprime.pid)
        if ps -p $PID > /dev/null 2>&1; then
            print_info "Parando servidor (PID: $PID)..."
            kill $PID
            rm autoprime.pid
            print_success "Servidor parado"
        else
            print_warning "Processo não encontrado"
            rm autoprime.pid
        fi
    else
        # Tentar encontrar o processo pela porta
        PID=$(lsof -ti:8080)
        if [ ! -z "$PID" ]; then
            print_info "Encontrado processo na porta 8080 (PID: $PID)"
            kill $PID
            print_success "Servidor parado"
        else
            print_warning "Nenhum servidor rodando"
        fi
    fi
}

# Status do servidor
status_server() {
    print_header "STATUS DO SERVIDOR"
    
    if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        PID=$(lsof -ti:8080)
        print_success "Servidor RODANDO (PID: $PID)"
        
        # Testar endpoint
        if curl -s http://localhost:8080/teste > /dev/null 2>&1; then
            print_success "Endpoint /teste respondendo"
        else
            print_warning "Porta 8080 ocupada mas endpoint não responde"
        fi
    else
        print_info "Servidor NÃO está rodando"
    fi
}

# Executar testes
run_tests() {
    print_header "EXECUTANDO TESTES"
    
    # Verificar se servidor está rodando
    if ! lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        print_warning "Servidor não está rodando. Iniciando..."
        start_background
        sleep 3
    fi
    
    print_info "Executando testes automatizados..."
    python3 test_backend.py
}

# Build Docker
docker_build() {
    print_header "BUILD DOCKER IMAGE"
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker não encontrado"
        exit 1
    fi
    
    print_info "Construindo imagem Docker..."
    docker build -t autoprime-backend .
    print_success "Imagem criada: autoprime-backend"
}

# Run Docker
docker_run() {
    print_header "RUN DOCKER CONTAINER"
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker não encontrado"
        exit 1
    fi
    
    # Parar container existente
    if docker ps -a | grep -q autoprime; then
        print_info "Removendo container existente..."
        docker rm -f autoprime
    fi
    
    print_info "Iniciando container..."
    docker run -d -p 8080:8080 --name autoprime autoprime-backend
    print_success "Container rodando em http://localhost:8080"
}

# Backup do banco de dados
backup_db() {
    print_header "BACKUP DO BANCO DE DADOS"
    
    if [ ! -f "carros.json" ]; then
        print_warning "Arquivo carros.json não encontrado"
        exit 1
    fi
    
    BACKUP_DIR="backups"
    mkdir -p $BACKUP_DIR
    
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_FILE="$BACKUP_DIR/carros_$TIMESTAMP.json"
    
    cp carros.json $BACKUP_FILE
    print_success "Backup criado: $BACKUP_FILE"
}

# Restaurar backup
restore_db() {
    print_header "RESTAURAR BACKUP"
    
    BACKUP_DIR="backups"
    if [ ! -d "$BACKUP_DIR" ]; then
        print_error "Nenhum backup encontrado"
        exit 1
    fi
    
    echo "Backups disponíveis:"
    ls -1 $BACKUP_DIR/carros_*.json | nl
    echo ""
    
    read -p "Digite o número do backup para restaurar (ou 'c' para cancelar): " choice
    
    if [ "$choice" = "c" ] || [ "$choice" = "C" ]; then
        print_info "Operação cancelada"
        exit 0
    fi
    
    BACKUP_FILE=$(ls -1 $BACKUP_DIR/carros_*.json | sed -n "${choice}p")
    
    if [ -z "$BACKUP_FILE" ]; then
        print_error "Backup inválido"
        exit 1
    fi
    
    # Fazer backup do arquivo atual antes de restaurar
    if [ -f "carros.json" ]; then
        cp carros.json "carros.json.bak"
    fi
    
    cp "$BACKUP_FILE" carros.json
    print_success "Backup restaurado: $BACKUP_FILE"
}

# Limpar dados
clean_db() {
    print_header "LIMPAR BANCO DE DADOS"
    
    print_warning "Esta ação irá APAGAR TODOS os dados!"
    read -p "Tem certeza? (s/n) " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        print_info "Operação cancelada"
        exit 0
    fi
    
    # Fazer backup antes de limpar
    if [ -f "carros.json" ]; then
        backup_db
    fi
    
    echo "[]" > carros.json
    print_success "Banco de dados limpo"
}

# Logs
show_logs() {
    print_header "LOGS DO SERVIDOR"
    
    if [ -f "autoprime.log" ]; then
        tail -f autoprime.log
    else
        print_warning "Arquivo de log não encontrado"
        print_info "Execute o servidor em background primeiro: ./manage.sh start-bg"
    fi
}

# Menu de ajuda
show_help() {
    cat << EOF

🚗 Backend AutoPrime - Script de Gerenciamento

USO: ./manage.sh [comando]

COMANDOS:
  install          Instala as dependências do projeto
  start            Inicia o servidor (foreground)
  start-bg         Inicia o servidor em background
  stop             Para o servidor
  restart          Reinicia o servidor
  status           Verifica status do servidor
  test             Executa os testes automatizados
  
  docker-build     Constrói a imagem Docker
  docker-run       Executa o container Docker
  
  backup           Cria backup do banco de dados
  restore          Restaura backup do banco de dados
  clean            Limpa o banco de dados
  logs             Mostra os logs do servidor
  
  help             Mostra esta mensagem

EXEMPLOS:
  ./manage.sh install           # Instalar dependências
  ./manage.sh start-bg          # Iniciar servidor em background
  ./manage.sh test              # Executar testes
  ./manage.sh backup            # Fazer backup dos dados

EOF
}

# Main
main() {
    case "${1:-help}" in
        install)
            install_deps
            ;;
        start)
            start_server
            ;;
        start-bg)
            start_background
            ;;
        stop)
            stop_server
            ;;
        restart)
            stop_server
            sleep 2
            start_background
            ;;
        status)
            status_server
            ;;
        test)
            run_tests
            ;;
        docker-build)
            docker_build
            ;;
        docker-run)
            docker_run
            ;;
        backup)
            backup_db
            ;;
        restore)
            restore_db
            ;;
        clean)
            clean_db
            ;;
        logs)
            show_logs
            ;;
        help|*)
            show_help
            ;;
    esac
}

main "$@"
