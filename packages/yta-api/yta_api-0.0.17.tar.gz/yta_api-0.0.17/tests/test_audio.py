from fastapi.testclient import TestClient
from yta_api import app


client = TestClient(app)

VALID_TEST_API_KEY = 'XX33XX'

def test_narrate_text_returns_200():
    response = client.get('/audio/narrate?api_key=' + VALID_TEST_API_KEY + '&text=Ejemplo de prueba')
    assert response.status_code == 200

# def test_narration_cortana_without_api_key_returns_422():
#     response = client.get('/audio/transcribe')
#     assert response.status_code == 422

# def test_narration_cortana_returns_200():
#     response = client.get('/audio/transcribe?api_key=' + VALID_TEST_API_KEY + '&text=Ejemplo de prueba')
#     assert response.status_code == 200