import os
import json
import tempfile
import pytest
from app import app, CARROS_FILE


@pytest.fixture
def client(tmp_path, monkeypatch):
    # use temp file for CARROS_FILE to avoid touching real file
    tmp_file = tmp_path / "carros_test.json"
    monkeypatch.setenv('AUTH_USER', 'admin')
    monkeypatch.setenv('AUTH_PASS', 'secret')
    monkeypatch.setattr('app.CARROS_FILE', str(tmp_file))
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


def test_save_update_delete_flow(client):
    # ensure starting empty
    rv = client.get('/api/listarCarros')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)

    # save a carro
    rv = client.post('/api/saveCarro', json={'modelo':'TEST-X','preco':123})
    assert rv.status_code == 201
    saved = rv.get_json()
    assert saved['modelo']=='TEST-X'

    # list now contains it
    rv = client.get('/api/listarCarros')
    assert rv.status_code == 200
    data = rv.get_json()
    assert any(c['modelo']=='TEST-X' for c in data)

    # update
    rv = client.post('/api/updateCarro', json={'modelo':'TEST-X','preco':321})
    assert rv.status_code == 200
    updated = rv.get_json()
    assert updated['preco']==321

    # delete
    rv = client.post('/api/deleteCarro', json={'modelo':'TEST-X'})
    assert rv.status_code == 200
    d = rv.get_json()
    assert d.get('deleted') is True
