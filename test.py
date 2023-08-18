from main import test_case_app
from fastapi.testclient import TestClient
import time

client = TestClient(test_case_app)  


def test_generate_secret():
    response = client.post('/generate', json={
        'secret': 'test_secret',
        'pass_phrase': 'test_pass_phrase'
    })

    assert response.status_code == 200
    data = response.json()
    assert 'secret_key' in data

    
def test_reveal_secret():
    response = client.post('/generate', json={
        'secret': 'test_secret',
        'pass_phrase': 'test_pass_phrase'
    })
    secret_key = response.json()['secret_key']

    response = client.post(f"/secrets/{secret_key}", json={
        "pass_phrase": "test_pass_phrase"
    })
    assert response.status_code == 200
    data = response.json()
    assert "secret" in data


def test_invalid_secret_key():
    response = client.post("/secrets/invalid_key", json={
        "pass_phrase": "test_passphrase"
    })
    assert response.status_code == 403

def test_expired_secret():
    response = client.post("/generate", json={
        "secret": "test_secret",
        "pass_phrase": "test_passphrase"
        }
    )
    secret_key = response.json()["secret_key"]

    time.sleep(2)

    response = client.post(f"/secrets/{secret_key}", json={
        "pass_phrase": "test_pass_phrase"

    })
    assert response.status_code == 403