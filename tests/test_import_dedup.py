from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

HEADERS = {
    "api-key": "buguard-internship-key"
}


def test_deduplication_import():
    
    payload = {
        "assets": [
            {
                "type": "domain",
                "value": "example.com",
                "tags": ["prod"],
                "source": "scan",
                "metadata": {}
            }
        ]
    }

    res1 = client.post("/assets/import", json=payload, headers=HEADERS)
    assert res1.status_code == 200
    assert res1.json()["imported"] >= 1

    res2 = client.post("/assets/import", json=payload, headers=HEADERS)
    assert res2.status_code == 200

    data = res2.json()
    assert data["updated"] >= 1