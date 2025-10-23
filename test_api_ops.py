import requests
import json

BASE = 'http://127.0.0.1:3000'

def pretty(r):
    try:
        return json.dumps(r.json(), indent=2, ensure_ascii=False)
    except Exception:
        return r.text

def main():
    print('1) Listar carros (antes)')
    r = requests.get(f'{BASE}/api/listarCarros', timeout=5)
    print(r.status_code, pretty(r))

    print('\n2) Salvar carro (modelo TEST-XYZ)')
    payload = {'modelo': 'TEST-XYZ', 'preco': 12345}
    r = requests.post(f'{BASE}/api/saveCarro', json=payload, timeout=5)
    print(r.status_code, pretty(r))

    print('\n3) Listar carros (depois de salvar)')
    r = requests.get(f'{BASE}/api/listarCarros', timeout=5)
    print(r.status_code, pretty(r))

    print('\n4) Atualizar carro (modelo TEST-XYZ -> preco 54321)')
    payload = {'modelo': 'TEST-XYZ', 'preco': 54321}
    # proxy usa POST para update
    r = requests.post(f'{BASE}/api/updateCarro', json=payload, timeout=5)
    print(r.status_code, pretty(r))

    print('\n5) Deletar carro (modelo TEST-XYZ)')
    # proxy aceita POST para delete com JSON
    r = requests.post(f'{BASE}/api/deleteCarro', json={'modelo': 'TEST-XYZ'}, timeout=5)
    print(r.status_code, pretty(r))

    print('\n6) Listar carros (depois de deletar)')
    r = requests.get(f'{BASE}/api/listarCarros', timeout=5)
    print(r.status_code, pretty(r))

if __name__ == '__main__':
    main()
