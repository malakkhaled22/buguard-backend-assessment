from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_filter_by_type():
    res = client.get("/assets?type=domain")
    
    assert res.status_code == 200
    data = res.json()

    assert isinstance(data, list)