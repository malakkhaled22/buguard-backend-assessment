from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

HEADERS = {
    "api-key": "buguard-internship-key"
}

unique = str(uuid.uuid4())

def test_relationship_flow():

    a1 = client.post("/assets", json={
        "type": "domain",
        "value": f"example-{unique}.com",
        "tags": [],
        "source": "scan",
        "metadata": {}
    }, headers=HEADERS)

    a2 = client.post("/assets", json={
        "type": "subdomain",
        "value": f"api.{unique}.com",
        "tags": [],
        "source": "scan",
        "metadata": {}
    }, headers=HEADERS)

    id1 = a1.json()["id"]
    id2 = a2.json()["id"]

    rel = client.post("/relationships/", json={
        "source_asset_id": id2,
        "target_asset_id": id1,
        "relationship_type": "belongs_to"
    }, headers=HEADERS)

    assert rel.status_code == 200

    graph = client.get(f"/assets/{id2}/related")

    assert graph.status_code == 200
    assert len(graph.json()["related_assets"]) > 0