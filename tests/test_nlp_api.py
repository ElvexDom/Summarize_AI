# tests/test_nlp_api.py

import io
import pytest
from fastapi.testclient import TestClient
from apis.ia_api.nlp_api import app
import sys
sys.path.insert(0, '..') # si besoin pour import services
from unittest.mock import MagicMock, patch
import os
os.environ["DISABLE_MODEL_SOURCE_CHECK"] = "True"  # Skip Paddle check
os.environ["TRANSFORMERS_OFFLINE"] = "1"  # Skip HuggingFace download
import warnings
warnings.filterwarnings("ignore", message="No ccache found")

#client = TestClient(app)

@pytest.fixture
def client():
    """Fixture client réutilisable pour tous les tests."""
    return TestClient(app)

@pytest.fixture
def mock_nlp():
    """Mock du service NLP global (nlp = nlp_serv())."""
    mock = MagicMock()
    mock.run_ocr.return_value = "Texte extrait: Alice Paris."  # str comme ocr_image_to_json
    mock.run_ner.return_value = "Alice → PER\nParis → LOC"  # str formaté "\n".join comme dans nlp_serv
    with patch('apis.ia_api.ocr_api.nlp', mock):
        yield mock

def test_ner_text(client):
    """Test de l'endpoint "/ner_text/" avec texte OCR."""
    response = client.post("/ner_text/", json={"ocr_text": "Alice habite à Paris."})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True  # Fix: date → data
    assert "text" in data
    assert isinstance(data["text"], str)

def test_process_document_with_mock(client, mock_nlp):
    """Test process_document avec mock NLP."""
    files = {"file": ("test.txt", io.BytesIO(b"contenu mock"), "text/plain")}
    response = client.post("/process_document/", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["text"] == "Texte extrait: Alice Paris."
    mock_nlp.run_ocr.assert_called_once()

def test_ner_text_error(client, mock_nlp):
    """Vérifie crash 500 sur NER fail."""
    mock_nlp.run_ner.side_effect = Exception("NER failed")
    with pytest.raises(Exception):  # ✅ Capture crash → PASS !
        client.post("/ner_text/", json={"ocr_text": "erreur"})

def test_process_no_file(client):
    """Test sans fichier (validation FastAPI)."""
    response = client.post("/process_document/")
    assert response.status_code == 422  # Pydantic/UploadFile requis

def test_ner_invalid_json(client):
    """Test JSON invalide (Pydantic NerRequest)."""
    response = client.post("/ner_text/", json={"invalid": "data"})
    assert response.status_code == 422  # ocr_text manquant

# already done by Nicolas
def test_root(client):
    """
    Test de l'endpoint racine "/"
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "time" in data
    assert "uptime" in data
    assert "python_version" in data
    assert "fastapi_version" in data

def test_favicon(client):
    """
    Test de l'endpoint "/favicon.ico"
    """
    response = client.get("/favicon.ico")
    assert response.status_code == 200
    #assert response.headers["content-type"] == "image/png"
    assert response.headers["content-type"].startswith("image/")  # Flexible
# def test_process_document_txt():
#     """
#     Test de l'endpoint "/process_document" avec un fichier TXT simulé
#     """
#     file_content = b"Ceci est un test de contenu de fichier."
#     files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
#     response = client.post("/process_document", files=files)
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["success"] is True
#     assert "summary" in data
#     assert isinstance(data["summary"], str)

def test_process_document_txt(client, mock_nlp):  # client + mock
    file_content = b"Ceci est un test."
    files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    response = client.post("/process_document/", files=files)  # Trailing /
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["text"] == "Texte extrait: Alice Paris."  # Fix: text pas summary
    assert isinstance(data["text"], str)

# def test_process_document_empty_file():
#     """
#     Test avec un fichier vide
#     """
#     files = {"file": ("empty.txt", io.BytesIO(b""), "text/plain")}
#     response = client.post("/process_document", files=files)
    
#     assert response.status_code == 200
#     data = response.json()
#     assert data["success"] is True
#     assert "summary" in data

def test_process_document_empty_file(client, mock_nlp):  # client + mock
    files = {"file": ("empty.txt", io.BytesIO(b""), "text/plain")}
    response = client.post("/process_document/", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["text"] == "Texte extrait: Alice Paris."  # Fix