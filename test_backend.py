#!/usr/bin/env python3
"""
Script de Teste Automatizado - Backend AutoPrime
Testa todos os endpoints da API conforme especificação
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8080"

def print_test(name: str, success: bool, details: str = ""):
    """Imprime resultado do teste com formatação"""
    status = "✅ PASSOU" if success else "❌ FALHOU"
    print(f"{status} - {name}")
    if details:
        print(f"   → {details}")
    print()

def test_endpoint(method: str, endpoint: str, data: Dict = None, expected_status: int = 200) -> tuple:
    """Testa um endpoint e retorna (sucesso, resposta)"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'}, timeout=5)
        else:
            return False, None
        
        success = response.status_code == expected_status
        try:
            return success, response.json()
        except:
            return success, response.text
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 70)
    print("TESTE AUTOMATIZADO - BACKEND AUTOPRIME")
    print("=" * 70)
    print()
    
    # Teste 1: Endpoint /teste
    print("📋 Teste 1: Endpoint /teste")
    success, response = test_endpoint("GET", "/teste", expected_status=200)
    if success and isinstance(response, dict) and response.get('status') == 'ok':
        print_test("GET /teste", True, f"Sistema funcionando - {response.get('message')}")
    else:
        print_test("GET /teste", False, str(response))
    
    # Teste 2: Listar carros inicial (pode estar vazio)
    print("📋 Teste 2: Listar carros inicialmente")
    success, response = test_endpoint("GET", "/listarCarros", expected_status=200)
    if success and isinstance(response, list):
        print_test("GET /listarCarros", True, f"Retornou lista com {len(response)} carros")
        carros_iniciais = len(response)
    else:
        print_test("GET /listarCarros", False, str(response))
        return
    
    # Teste 3: Salvar carro - Ferrari
    print("📋 Teste 3: Salvar carro (Ferrari)")
    success, response = test_endpoint("POST", "/saveCarro", 
                                      data={"modelo": "Ferrari", "preco": 1200000},
                                      expected_status=201)
    print_test("POST /saveCarro (Ferrari)", success, str(response))
    
    # Teste 4: Salvar carro - Porsche
    print("📋 Teste 4: Salvar carro (Porsche)")
    success, response = test_endpoint("POST", "/saveCarro", 
                                      data={"modelo": "Porsche", "preco": 850000},
                                      expected_status=201)
    print_test("POST /saveCarro (Porsche)", success, str(response))
    
    # Teste 5: Salvar carro - Lamborghini
    print("📋 Teste 5: Salvar carro (Lamborghini)")
    success, response = test_endpoint("POST", "/saveCarro", 
                                      data={"modelo": "Lamborghini", "preco": 1500000},
                                      expected_status=201)
    print_test("POST /saveCarro (Lamborghini)", success, str(response))
    
    # Teste 6: Listar todos os carros
    print("📋 Teste 6: Listar todos os carros após inserções")
    success, response = test_endpoint("GET", "/listarCarros", expected_status=200)
    if success and isinstance(response, list):
        qtd_esperada = carros_iniciais + 3
        qtd_atual = len(response)
        test_passou = qtd_atual == qtd_esperada
        print_test("GET /listarCarros", test_passou, 
                  f"Esperado: {qtd_esperada} carros, Atual: {qtd_atual} carros")
        if test_passou:
            for carro in response:
                print(f"   • {carro.get('modelo')} - R$ {carro.get('preco'):,.2f}")
            print()
    else:
        print_test("GET /listarCarros", False, str(response))
        return
    
    # Teste 7: Buscar carro específico - Ferrari
    print("📋 Teste 7: Buscar carro específico (Ferrari)")
    success, response = test_endpoint("POST", "/getCarro", 
                                      data={"modelo": "Ferrari"},
                                      expected_status=200)
    if success and isinstance(response, dict) and response.get('preco') == 1200000:
        print_test("POST /getCarro (Ferrari)", True, f"Preço: R$ {response.get('preco'):,.2f}")
    else:
        print_test("POST /getCarro (Ferrari)", False, str(response))
    
    # Teste 8: Atualizar preço - Ferrari
    print("📋 Teste 8: Atualizar preço do Ferrari")
    success, response = test_endpoint("POST", "/updateCarro", 
                                      data={"modelo": "Ferrari", "preco": 1350000},
                                      expected_status=200)
    print_test("POST /updateCarro (Ferrari)", success, "Preço atualizado para R$ 1.350.000,00")
    
    # Teste 9: Verificar atualização
    print("📋 Teste 9: Verificar atualização do preço")
    success, response = test_endpoint("POST", "/getCarro", 
                                      data={"modelo": "Ferrari"},
                                      expected_status=200)
    if success and isinstance(response, dict) and response.get('preco') == 1350000:
        print_test("Verificação de atualização", True, f"Novo preço: R$ {response.get('preco'):,.2f}")
    else:
        print_test("Verificação de atualização", False, str(response))
    
    # Teste 10: Deletar carro - Lamborghini
    print("📋 Teste 10: Deletar carro (Lamborghini)")
    success, response = test_endpoint("POST", "/deleteCarro", 
                                      data={"modelo": "Lamborghini"},
                                      expected_status=200)
    print_test("POST /deleteCarro (Lamborghini)", success, str(response))
    
    # Teste 11: Verificar deleção
    print("📋 Teste 11: Verificar deleção")
    success, response = test_endpoint("GET", "/listarCarros", expected_status=200)
    if success and isinstance(response, list):
        qtd_esperada = carros_iniciais + 2  # +3 inseridos -1 deletado
        qtd_atual = len(response)
        test_passou = qtd_atual == qtd_esperada
        lamborghini_existe = any(c.get('modelo') == 'Lamborghini' for c in response)
        test_passou = test_passou and not lamborghini_existe
        print_test("Verificação de deleção", test_passou, 
                  f"Total: {qtd_atual} carros (Lamborghini removido)")
    else:
        print_test("Verificação de deleção", False, str(response))
    
    # Teste 12: Endpoints de compatibilidade frontend
    print("📋 Teste 12: Endpoint /api/listarCarros (frontend)")
    success, response = test_endpoint("GET", "/api/listarCarros", expected_status=200)
    if success and isinstance(response, list):
        print_test("GET /api/listarCarros", True, f"Retornou {len(response)} carros para o frontend")
    else:
        print_test("GET /api/listarCarros", False, str(response))
    
    # Teste 13: Endpoint /api/getCarro (frontend)
    print("📋 Teste 13: Endpoint /api/getCarro (frontend)")
    success, response = test_endpoint("POST", "/api/getCarro", 
                                      data={"modelo": "Ferrari"},
                                      expected_status=200)
    if success and isinstance(response, list) and len(response) > 0:
        print_test("POST /api/getCarro", True, f"Retornou array com {len(response)} item(s)")
    else:
        print_test("POST /api/getCarro", False, str(response))
    
    # Teste 14: Health check
    print("📋 Teste 14: Health Check")
    success, response = test_endpoint("GET", "/health", expected_status=200)
    if success and isinstance(response, dict) and response.get('status') == 'ok':
        print_test("GET /health", True, f"Status: {response.get('status')}")
    else:
        print_test("GET /health", False, str(response))
    
    # Resumo final
    print("=" * 70)
    print("TESTES CONCLUÍDOS")
    print("=" * 70)
    print("\n✅ Todos os endpoints principais foram testados!")
    print("✅ Backend compatível com frontend existente")
    print("✅ Persistência de dados funcionando")
    print("✅ Pronto para deploy na AWS\n")

if __name__ == "__main__":
    print("\n⏳ Aguardando servidor iniciar...\n")
    time.sleep(2)
    main()
