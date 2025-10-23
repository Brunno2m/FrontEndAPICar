import requests

try:
    r = requests.get('http://127.0.0.1:3000/debug/backend_status', timeout=5)
    print('local /debug/backend_status ->', r.status_code, r.text)
except Exception as e:
    print('erro ao acessar /debug/backend_status:', e)

try:
    r2 = requests.get('http://18.231.156.122:8080/listarCarros', timeout=5)
    print('remote /listarCarros ->', r2.status_code, r2.text[:200])
except Exception as e:
    print('erro ao acessar backend remoto:', e)
