# tests/test_ocr_api.py

import io
import pytest
from fastapi.testclient import TestClient
from apis.ia_api.ocr_api import app

client = TestClient(app)

def test_root():
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

def test_favicon():
    """
    Test de l'endpoint "/favicon.ico"
    """
    response = client.get("/favicon.ico")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_process_document_txt():
    """
    Test de l'endpoint "/process_document" avec un fichier TXT simulé
    """
    file_content = b"Ceci est un test de contenu de fichier."
    files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    response = client.post("/process_document", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "summary" in data
    assert isinstance(data["summary"], str)

def test_process_document_empty_file():
    """
    Test avec un fichier vide
    """
    files = {"file": ("empty.txt", io.BytesIO(b""), "text/plain")}
    response = client.post("/process_document", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "summary" in data
